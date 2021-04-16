"""MigrationForInternetExchangePointsTable Migration."""

from masoniteorm.migrations import Migration


class MigrationForInternetExchangePointsTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("internet_exchange_points") as table:
            table.increments("id")
            table.string("name")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("internet_exchange_points")
