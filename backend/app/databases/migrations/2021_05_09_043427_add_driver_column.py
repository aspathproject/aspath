"""AddDriverColumn Migration."""

from masoniteorm.migrations import Migration


class AddDriverColumn(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("route_collectors") as table:
            table.string('driver').nullable()
            table.jsonb('driver_opts').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table("route_collectors") as table:
            table.drop_column('driver')
            table.drop_column('driver_opts')
