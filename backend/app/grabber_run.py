from config.database import DB
from masoniteorm.query import QueryBuilder

from grabbers.pch_daily_snapshots import get_all_dataset_links, download_dataset_link
import json

# TODO: Refactor to add driver abstraction
def grab_new_datasets(collector_name):
  route_collector = QueryBuilder().table('route_collectors').where("name", collector_name).first()

  for link in get_all_dataset_links(collector_name):
    filename = link.strip().split('/')[-1]

    dataset_exists_on_db = QueryBuilder().table("datasets").where({ "filename": filename }).first()
    if not dataset_exists_on_db:
      print(f"dataset {filename} not found on database, downloading...")
      file_content = download_dataset_link(link)
      file_len = len(file_content)
      print(f"Downloaded dataset. {file_len} bytes found.")

      snapshot_date = '-'.join(filename.split('.')[-4:-1]) + ' 00:00:01'

      with DB.transaction():
        # create dataset entry on database
        dataset = QueryBuilder().table("datasets").create({ "filename":filename,
                                                  "status":"downloaded",
                                                  "filecontent": file_content,
                                                  "created_at": snapshot_date })
        # create routing snapshot entry
        routing_snapshot = QueryBuilder().table('routing_snapshots').create({ "status": "pending",
                                                                              "dataset_id": dataset["id"],
                                                                              "route_collector_id": route_collector["id"],
                                                                              "created_at": snapshot_date })
