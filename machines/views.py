from django.shortcuts import render
from kafka import KafkaProducer
import logging

logging.basicConfig(level=logging.DEBUG)
# Create your views here.

def kafka_test(request):
   
    producer = KafkaProducer(bootstrap_servers='172.26.0.2:29092',                            
                            security_protocol='SSL',
                            ssl_cafile='../certs/CARoot.pem',
                            ssl_certfile='../certs/certificate.pem',
                            ssl_keyfile='../certs/key.pem',
                            ssl_check_hostname=False,
                            api_version=(2,7,0))
    producer.send('test',b"Hello World")
    producer.flush()
    return ''