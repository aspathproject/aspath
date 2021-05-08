from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from masoniteorm.query import QueryBuilder
from brotli_asgi import BrotliMiddleware
from redisbeat.scheduler import RedisScheduler
from config.database import DB
from datetime import timezone

import worker

app = FastAPI()
app.add_middleware(BrotliMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = RedisScheduler(app=worker.app)

@app.get("/")
def read_root():
    return {"Hello": "from ASPATH project"}

@app.get("/scheduler/")
def get_scheduler_list():
    return scheduler.list()

@app.delete("/scheduler/")
def wipe_scheduler():
    removed_tasks = []
    for task in scheduler.list():
      removed_tasks.append(task.name)
      scheduler.remove(task.name)
    return removed_tasks

@app.get("/exchange-points/")
def exchange_points_index():
    exchange_points = {}
    ixp_results = QueryBuilder().table("internet_exchange_points").get()

    for ixp in ixp_results:
      exchange_points[ixp['id']] = ixp
      route_collectors = QueryBuilder().table("route_collectors").select('id', 'name').where('ixp_id', ixp['id']).get()
      route_collectors_dict = {}

      for collector in route_collectors:
        route_collectors_dict[collector['id']] = collector['name']
      collector_ids = [collector['id'] for collector in route_collectors ]

      # identify the route collector that has the last saved snapshot
      last_update = QueryBuilder().table("routing_snapshots").select('route_collector_id', 'id, created_at').where_in('route_collector_id', collector_ids) \
                      .order_by('created_at', 'desc') \
                      .limit(1).first()

      exchange_points[ixp['id']]['route_collectors'] = len(collector_ids)
      exchange_points[ixp['id']]['last_snapshot_date'] = last_update['created_at'].strftime('%Y-%m-%d')
      exchange_points[ixp['id']]['last_snapshot_id'] = last_update['id']
      exchange_points[ixp['id']]['last_snapshot_collector_name'] = route_collectors_dict[last_update['route_collector_id']]
    return exchange_points

@app.get("/route-collectors/")
def route_collectors_index():
    builder = QueryBuilder().table("route_collectors")
    return builder.all()

@app.get("/route-collectors/{collector_name}/snapshots/")
def get_route_collector_snapshots(collector_name: str):
    route_collector = QueryBuilder().table("route_collectors").where('name', collector_name).first()
    if not route_collector:
      raise HTTPException(status_code=404, detail="Route Collector not found")
    route_collector_id = route_collector["id"]

    return QueryBuilder().table("routing_snapshots").select('id, created_at').where({'route_collector_id': route_collector_id, 'status': 'parsed'}).get()

@app.get("/route-collectors/{collector_name}/snapshots/latest/routes")
def get_snapshot_routes(collector_name: str):
    route_collector = QueryBuilder().table("route_collectors").where('name', collector_name).first()
    if not route_collector:
      raise HTTPException(status_code=404, detail="Route Collector not found")
    route_collector_id = route_collector["id"]

    snapshot = QueryBuilder().table("routing_snapshots").where('route_collector_id', route_collector_id).last('id')
    if not snapshot:
      raise HTTPException(status_code=404, detail="Routing snapshot not found")

    query = """SELECT "ip_routes"."block", "ip_routes"."path", path->>-1 origin, "autonomous_systems"."name"
FROM "ip_routes", "autonomous_systems"
WHERE "ip_routes"."created_at" = '?'
AND cast(nullif("ip_routes"."path"->>-1, '') as int) = "autonomous_systems"."number"
AND "ip_routes"."snapshot_id" = '?'
    """
    snapshot_metadata = {}
    snapshot_metadata['created_at'] = snapshot['created_at'].replace(tzinfo=timezone.utc)
    snapshot_metadata['snapshot_id'] = snapshot['id']

    routes = QueryBuilder().statement(query, [snapshot['created_at'], snapshot['id']])
    return { "metadata": snapshot_metadata, "routes": routes }

@app.get("/route-collectors/{collector_name}/snapshots/{snapshot_id}/routes")
def get_snapshot_routes(collector_name: str, snapshot_id: int):
    route_collector = QueryBuilder().table("route_collectors").where('name', collector_name).first()
    if not route_collector:
      raise HTTPException(status_code=404, detail="Route Collector not found")
    route_collector_id = route_collector["id"]

    snapshot = QueryBuilder().table("routing_snapshots").where('id', snapshot_id).first()
    if not snapshot:
      raise HTTPException(status_code=404, detail="Routing snapshot not found")

    query = """SELECT "ip_routes"."block", "ip_routes"."path", path->>-1 origin, "autonomous_systems"."name"
FROM "ip_routes", "autonomous_systems"
WHERE "ip_routes"."created_at" = '?'
AND cast(nullif("ip_routes"."path"->>-1, '') as int) = "autonomous_systems"."number"
AND "ip_routes"."snapshot_id" = '?'
    """

    snapshot_metadata = {}
    snapshot_metadata['created_at'] = snapshot['created_at'].replace(tzinfo=timezone.utc)
    snapshot_metadata['snapshot_id'] = snapshot['id']

    routes = QueryBuilder().statement(query, [snapshot['created_at'], snapshot['id']])
    return { "metadata": snapshot_metadata, "routes": routes }

@app.get("/statistics")
def get_database_statistics():
    route_collector_count = QueryBuilder().table("route_collectors").count()
    ixp_count = QueryBuilder().table("internet_exchange_points").count()
    routing_snapshots_count = QueryBuilder().table("routing_snapshots").count()
    autonomous_systems_count = QueryBuilder().table("autonomous_systems").count()
    return {'route_collector_count': route_collector_count,
            'snapshots_count': routing_snapshots_count, 'autonomous_systems': autonomous_systems_count,
            'ixp_count': ixp_count }


