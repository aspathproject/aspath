import typer
from config.database import DB
from masoniteorm.query import QueryBuilder
from ingester_run import ingest_pending_snapshots
from grabber_run import grab_new_datasets
import yaml
import toml


app = typer.Typer()
with open("configuration/aspath.toml") as fh:
    aspath_config = toml.load(fh)


@app.command()
def ingest(route_collector_name: str):
    """
    Parse and ingest pending snapshots of a given route collector.
    """
    route_collector = (
        QueryBuilder()
        .table("route_collectors")
        .where("name", route_collector_name)
        .first()
    )
    if not route_collector:
        return typer.echo("route collector not found on database.")
    ingest_pending_snapshots(route_collector_name)


@app.command()
def grab(route_collector_name: str):
    """
    Execute grabber for a given route collector.
    """
    route_collector = (
        QueryBuilder()
        .table("route_collectors")
        .where("name", route_collector_name)
        .first()
    )
    if not route_collector:
        return typer.echo("route collector not found on database.")
    grab_new_datasets(route_collector_name)


@app.command()
def wipe_routes(route_collector_name: str, delete_datasets: bool = False):
    """
    Delete all parsed routes and put snapshots into pending parse status
    """
    route_collector = (
        QueryBuilder()
        .table("route_collectors")
        .where("name", route_collector_name)
        .first()
    )
    snapshots = (
        QueryBuilder()
        .table("routing_snapshots")
        .where({"route_collector_id": route_collector["id"], "status": "parsed"})
        .get()
    )

    with DB.transaction():
        for snapshot in snapshots:
            dataset_id = snapshot["dataset_id"]
            snapshot_id = snapshot["id"]
            created_at = str(snapshot["created_at"])
            print(f"wiping snapshot {snapshot_id} - {created_at}")
            # mark dataset as pending
            QueryBuilder().table("datasets").where("id", dataset_id).update(
                {"status": "pending"}
            )
            # mark routing snapshot as pending
            QueryBuilder().table("routing_snapshots").where("id", snapshot_id).update(
                {"status": "pending"}
            )
            # delete all routes from snapshot
            QueryBuilder().table("ip_routes").where(
                {"snapshot_id": snapshot_id, "created_at": created_at}
            ).delete()
    print(yaml.dump("finished wiping routing snapshots"))


@app.command()
def list_snapshots(route_collector_name: str, status: str = "all"):
    """
    Show saved snapshots of a given route collector
    """
    route_collector = (
        QueryBuilder()
        .table("route_collectors")
        .where("name", route_collector_name)
        .first()
    )
    if status == "all":
        snapshots = (
            QueryBuilder()
            .table("routing_snapshots")
            .where("route_collector_id", route_collector["id"])
            .get()
        )
    else:
        snapshots = (
            QueryBuilder()
            .table("routing_snapshots")
            .where({"route_collector_id": route_collector["id"], "status": status})
            .get()
        )
    if len(snapshots) == 0:
        return typer.echo("no snapshots found.")

    snapshots_output = [
        *map(
            lambda snapshot: {
                snapshot["created_at"]: {
                    "id": snapshot["id"],
                    "updated_at": snapshot["updated_at"],
                    "status": snapshot["status"],
                }
            },
            snapshots,
        )
    ]
    typer.echo(yaml.dump(snapshots_output))


@app.command()
def delete_snapshot(route_collector_name: str, snapshot_id: int):
    """
    Delete a given snapshot from a route collector.
    """
    route_collector = (
        QueryBuilder()
        .table("route_collectors")
        .where("name", route_collector_name)
        .first()
    )
    with DB.transaction():
        snapshot = (
            QueryBuilder()
            .table("routing_snapshots")
            .where({"route_collector_id": route_collector["id"], "id": snapshot_id})
        )
        snapshot_data = snapshot.first()
        if not snapshot_data:
            return typer.echo(f"snapshot not found...")
        snapshot_id = snapshot_data["id"]
        dataset_id = snapshot_data["dataset_id"]
        created_at = str(snapshot_data["created_at"])

        # delete dataset
        print(f"deleting dataset {dataset_id}...")
        QueryBuilder().table("datasets").where("id", dataset_id).delete()
        print("dataset deletion complete")

        # delete routes
        print(f"deleting parsed routes from snapshot {snapshot_id} - {created_at}")
        QueryBuilder().table("ip_routes").where("snapshot_id", snapshot_id).where(
            "created_at", created_at
        ).delete()
        print(f"deleting snapshot {snapshot_id}")

        # delete snapshot
        snapshot = (
            QueryBuilder()
            .table("routing_snapshots")
            .where({"route_collector_id": route_collector["id"], "id": snapshot_id})
        )
        snapshot.delete()
        print(f"deleted snapshot {snapshot_id}.")


@app.command()
def list():
    """
    List available route collectors in database.
    """
    output = {}
    route_collectors_results = QueryBuilder().table("route_collectors").all()
    for route_collector in route_collectors_results:
        output[route_collector["name"]] = [
            {"id": route_collector["id"]},
            {"driver": route_collector["driver"]},
        ]
    print(yaml.dump(output))


if __name__ == "__main__":
    app()
