import json
from kafka import KafkaProducer

"""
This class provides a service to communicate with Kakfa
"""


class KafkaService:

    def __init__(self):
        self.producer = KafkaProducer(
                            bootstrap_servers='kafka:9092',
                            security_protocol='SASL_SSL',
                            ssl_cafile='certs/CARoot.pem',
                            ssl_certfile='certs/certificate.pem',
                            ssl_keyfile='certs/key.pem',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username='django',
                            sasl_plain_password='django',
                            ssl_check_hostname=False,
                            api_version=(2, 7, 0),
                            value_serializer=lambda m: json.dumps(m).encode('latin')
                        )

    def send(self, topic, key, value):
        self.producer.send(topic=topic, key=key, value=value)
        self.producer.flush()

