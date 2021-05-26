import typer
from config.database import DB
from masoniteorm.query import QueryBuilder
import yaml

app = typer.Typer()


@app.command()
def list():
    output = {}
    internet_exchange_results = QueryBuilder().table("internet_exchange_points").all()
    for internet_exchange in internet_exchange_results:
        output[internet_exchange["name"]] = [
            {"id": internet_exchange["id"]},
            {"slug": internet_exchange["slug"]},
        ]
    print(yaml.dump(output))


if __name__ == "__main__":
    app()
