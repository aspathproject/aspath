"""MigrationForIpRoutesTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForIpRoutesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("ip_routes") as table:
            table.inet("block").nullable()
            table.jsonb("path").nullable()

            # foreign key
            table.integer("snapshot_id").unsigned()
            table.foreign("snapshot_id").references('id').on('routing_snapshots').on_delete("cascade")

            table.timestamps()
            table.primary("created_at")

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("ip_routes")
