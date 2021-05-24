from config.database import DB
from masoniteorm.query import QueryBuilder
from parsers.pch_v4 import PCHv4Parser
import toml
import json


## This module will search for pending routing snapshots,
## parse them according to their driver and execute
## SQL queries to add the snapshots to the database.


def ingest_pending_snapshots(collector_name):
    for snapshot, dataset, routes in parse_pending_snapshots(collector_name):
        big_query = generate_route_mass_insert(routes, snapshot)

        # we ensure that in case of INSERT error none of these changes are commited
        with DB.transaction():
            print(f"saving {dataset['filename']} routes to database...")
            # mark dataset as parsed
            QueryBuilder().table("datasets").where("id", dataset["id"]).update(
                {"status": "parsed"}
            )
            # mark snapshot as parsed
            QueryBuilder().table("routing_snapshots").where(
                "id", snapshot["id"]
            ).update({"status": "parsed"})
            # add snapshot routes to database
            QueryBuilder().statement(big_query)


def parse_pending_snapshots(collector_name):
    route_collector = (
        QueryBuilder().table("route_collectors").where("name", collector_name).first()
    )
    driver = route_collector["driver"]
    driver_opts = route_collector["driver_opts"]

    with open("configuration/aspath.toml") as fh:
        aspath_config = toml.load(fh)

    if collector_name not in aspath_config["grabbers"]:
        print("grabber configuration not found in aspath.toml")
        exit()

    store_inactive_routes = False
    if "store_inactive_routes" in aspath_config["grabbers"][collector_name]:
        store_inactive_routes = aspath_config["grabbers"][collector_name][
            "store_inactive_routes"
        ]
        print(f"Store inactive routes: {store_inactive_routes}")

    if driver == "pch_v4":
        parser = PCHv4Parser(store_inactive_routes=store_inactive_routes)
        print("[parse_pending_snapshots] PCHv4 Parser loaded")

    pending_snapshots = get_collector_pending_snapshots(collector_name)
    for snapshot in pending_snapshots:
        dataset = (
            QueryBuilder().table("datasets").where("id", snapshot["dataset_id"]).first()
        )

        # Execute parser
        routes = parser.get_routes(dataset["filecontent"])
        yield snapshot, dataset, routes


def get_collector_pending_snapshots(collector_name):
    route_collector = (
        QueryBuilder().table("route_collectors").where("name", collector_name).first()
    )
    pending_snapshots = (
        QueryBuilder()
        .table("routing_snapshots")
        .where({"route_collector_id": route_collector["id"], "status": "pending"})
        .get()
    )
    return pending_snapshots


def generate_route_mass_insert(routes, snapshot):
    SQL_QUERY_START = (
        "INSERT INTO ip_routes(snapshot_id, block, path, created_at) VALUES"
    )
    SQL_QUERY_ROW = ", (%s, $$%s$$, $$%s$$, '%s')"

    query = ""
    query += SQL_QUERY_START
    first_row = True

    snapshot_id = snapshot["id"]
    created_at = str(snapshot["created_at"])

    for route in routes:
        ip_block, aspath = route.split(";")
        aspath_list = json.dumps(aspath.split(" "))
        if first_row:
            first_query_row = SQL_QUERY_ROW[1:]
            query += first_query_row % (snapshot_id, ip_block, aspath_list, created_at)
            first_row = False
        else:
            query += SQL_QUERY_ROW % (snapshot_id, ip_block, aspath_list, created_at)

    query += ";"
    return query
