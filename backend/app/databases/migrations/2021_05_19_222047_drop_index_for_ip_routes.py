"""DropIndexForIpRoutes Migration."""

from masoniteorm.migrations import Migration


class DropIndexForIpRoutes(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("ip_routes") as table:
            table.drop_index('ip_routes_created_at_primary')

    def down(self):
        """
        Revert the migrations.
        """
        pass
