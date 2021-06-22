from parsers.quagga import QuaggaParser
from io import BytesIO, TextIOWrapper
import gzip


class PCHv4Parser:
    def __init__(self, store_inactive_routes=False):
        self.store_inactive_routes = store_inactive_routes

    def get_routes(self, data):
        # PCH snapshots are stored in GZip format
        compressed_content = BytesIO()
        compressed_content.write(data)
        compressed_content.seek(0)

        uncompressed_content = TextIOWrapper(
            gzip.GzipFile(fileobj=compressed_content, mode="rb")
        )

        # Initialize and use quagga parser on uncompressed
        parser = QuaggaParser(store_inactive_routes=self.store_inactive_routes)
        return parser.get_routes(uncompressed_content)
