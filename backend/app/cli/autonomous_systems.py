import typer
from config.database import DB
from masoniteorm.query import QueryBuilder
import yaml

app = typer.Typer()


@app.command()
def list():
    """
    Prints registered autonomous system list.
    """
    output = {}
    autonomous_systems = QueryBuilder().table("autonomous_systems").all()
    for asn in autonomous_systems:
        output[asn["number"]] = [{"name": asn["name"]}, {"country": asn["country"]}]
    print(yaml.dump(output))


if __name__ == "__main__":
    app()
