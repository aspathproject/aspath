from parsers.quagga import QuaggaParser
from io import BytesIO, TextIOWrapper
import gzip

class PCHv4Parser():

  def get_routes(self, data):
    # PCH snapshots are stored in GZip format
    compressed_content = BytesIO()
    compressed_content.write(data)
    compressed_content.seek(0)

    uncompressed_content = TextIOWrapper(gzip.GzipFile(fileobj=compressed_content, mode='rb'))

    # Initialize and use quagga parser on uncompressed
    parser = QuaggaParser()
    return parser.get_routes(uncompressed_content)
