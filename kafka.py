import io
import avro.schema
import avro.io
import lipsum
import random

from kafka.client import KafkaClient
from kafka.producer import SimpleProducer, KeyedProducer

g = lipsum.Generator()
kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)

# Path to user.avsc avro schema
schema_path="/Your/schema/path/user.avsc"

# Kafka topic
topic = "test"

schema = avro.schema.parse(open(schema_path).read())


for i in xrange(2000):

	writer = avro.io.DatumWriter(schema)
	bytes_writer = io.BytesIO()
	encoder = avro.io.BinaryEncoder(bytes_writer)
	writer.write({"name": g.generate_sentence(), "favorite_color": g.generate_sentence(), "favorite_number": random.randint(0,10)}, encoder)
	raw_bytes = bytes_writer.getvalue()
	producer.send_messages(topic, raw_bytes)
