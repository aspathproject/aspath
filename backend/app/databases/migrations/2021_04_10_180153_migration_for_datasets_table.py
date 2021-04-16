"""MigrationForDatasetsTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForDatasetsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("datasets") as table:
            table.increments("id")
            table.string("filename")
            table.binary("filecontent").nullable()
            table.string("status").default("new")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("datasets")
