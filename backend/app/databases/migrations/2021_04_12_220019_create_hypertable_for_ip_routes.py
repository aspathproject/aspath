"""CreateHypertableForIpRoutes Migration."""

from masoniteorm.migrations import Migration
from config.database import DB

class CreateHypertableForIpRoutes(Migration):
    def up(self):
        """
        Run the migrations.
        """
        DB.statement("SELECT create_hypertable('ip_routes', 'created_at', chunk_time_interval => INTERVAL '1 day')")

    def down(self):
        """
        Revert the migrations.
        """
        pass
