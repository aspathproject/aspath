"""MigrationForRoutingSnapshots Migration."""

from masoniteorm.migrations import Migration


class MigrationForRoutingSnapshots(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("routing_snapshots") as table:
            table.increments("id")
            table.string("status").default("pending")

            # foreign keys
            table.integer("dataset_id").unsigned()
            table.integer("route_collector_id").unsigned()
            table.foreign("dataset_id").references('id').on('datasets').on_delete("cascade")
            table.foreign("route_collector_id").references('id').on('route_collectors').on_delete("cascade")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("routing_snapshots")
