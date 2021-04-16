"""MigrationForRouteCollectors Migration."""

from masoniteorm.migrations import Migration


class MigrationForRouteCollectors(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("route_collectors") as table:
            table.increments("id")
            table.string("name")
            table.string("organization_name")

            # foreign keys
            table.integer("ixp_id").unsigned()
            table.foreign("ixp_id").references('id').on('internet_exchange_points')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("route_collectors")
