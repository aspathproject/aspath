import typer

from config.database import DB
from masoniteorm.query import QueryBuilder

from cli import route_collectors
from cli import internet_exchanges
from cli import autonomous_systems

app = typer.Typer()
app.add_typer(route_collectors.app, name="route-collectors")
app.add_typer(internet_exchanges.app, name="internet-exchanges")
app.add_typer(autonomous_systems.app, name="autonomous-systems")


if __name__ == "__main__":
    app()
