"""AddSlugToInternetExchangePoints Migration."""

from masoniteorm.migrations import Migration


class AddSlugToInternetExchangePoints(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table("internet_exchange_points") as table:
            table.string('slug').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        pass
