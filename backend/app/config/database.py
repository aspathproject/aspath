from masoniteorm.connections import ConnectionResolver

DATABASES = {
  "default": "postgres",
  "postgres": {
    "driver": "postgres",
    "host": "postgres",
    "database": "aspath",
    "user": "postgres",
    "password": "",
    "port": 5432,
    "prefix": "",
    "logging_queries": False,
    "options": {
      #
    }
  }
}

DB = ConnectionResolver().set_connection_details(DATABASES)
