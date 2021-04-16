"""MigrationForAutonomousSystemsTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForAutonomousSystemsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("autonomous_systems") as table:
            table.string("name")
            table.integer("number", length="6").unsigned()
            table.increments("id")
            table.string("country")

            # Dataset FK
            table.integer("dataset_id").unsigned()
            table.foreign("dataset_id").references('id').on('datasets').on_delete("cascade")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("autonomous_systems")
