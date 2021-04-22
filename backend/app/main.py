from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from masoniteorm.query import QueryBuilder
from brotli_asgi import BrotliMiddleware
from redisbeat.scheduler import RedisScheduler
from config.database import DB
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
    builder = QueryBuilder().table("internet_exchange_points")
    return builder.all()

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

@app.get("/route-collectors/{collector_name}/snapshots/{snapshot_id}/routes")
def get_snapshot_routes(collector_name: str, snapshot_id: int):
    route_collector = QueryBuilder().table("route_collectors").where('name', collector_name).first()
    if not route_collector:
      raise HTTPException(status_code=404, detail="Route Collector not found")
    route_collector_id = route_collector["id"]

    snapshot = QueryBuilder().table("routing_snapshots").where('id', snapshot_id).first()
    if not snapshot:
      raise HTTPException(status_code=404, detail="Routing snapshot not found")

    return QueryBuilder().table("ip_routes").where({'created_at': snapshot['created_at'], 'snapshot_id': snapshot['id']}).get()



@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
