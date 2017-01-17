from pykafka import KafkaClient
import avro.schema
import io, random
from avro.io import DatumWriter

schema_path="user.avsc"
schema = avro.schema.parse(open(schema_path).read())

client = KafkaClient(hosts="127.0.0.1:9092")
topic = client.topics['avro']

with topic.get_sync_producer() as producer:
	for i in xrange(10):
	    writer = avro.io.DatumWriter(schema)
	    bytes_writer = io.BytesIO()
	    encoder = avro.io.BinaryEncoder(bytes_writer)
	    writer.write({"name": "123", "favorite_color": "111", "favorite_number": random.randint(0,10)}, encoder)
	    raw_bytes = bytes_writer.getvalue()
	    producer.produce(raw_bytes)
