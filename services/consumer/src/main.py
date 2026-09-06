from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka import DeserializingConsumer

schema_registry_client = SchemaRegistryClient({"url": "http://schema-registry:8081"})

key_deserializer = AvroDeserializer(schema_registry_client)
value_deserializer = AvroDeserializer(schema_registry_client)

consumer_conf = {
    "bootstrap.servers": "kafka_broker:9092",
    "group.id": "cdc-consumer-group",
    "auto.offset.reset": "earliest",
    "key.deserializer": key_deserializer,
    "value.deserializer": value_deserializer,
}

consumer = DeserializingConsumer(consumer_conf)

consumer.subscribe(["cdc.public.users"])

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(msg.error())
            continue
        print(f"key={msg.key()}  value={msg.value()}")
finally:
    consumer.close()