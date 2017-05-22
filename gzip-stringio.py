import gzip
import StringIO

stringio = StringIO.StringIO()
gzip_file = gzip.GzipFile(fileobj=stringio, mode='w')
gzip_file.write('Hello World')
gzip_file.close()

stringio.getvalue()
