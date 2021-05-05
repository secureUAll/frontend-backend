from django.shortcuts import render
from kafka import KafkaProducer
from django.http import HttpResponse
import logging
import json
import machines.dataContext as dataContext

logging.basicConfig(level=logging.DEBUG)
# Create your views here.
context = dataContext.machineContext

def MachinesView(request, *args, **kwargs):
    return render(request, "machines/machines.html", context)


def RequestsView(request, *args, **kwargs):
    return render(request, "machines/requests.html", context)    


def MachinesView(request, *args, **kwargs):
    context = dataContext.machineContext
    return render(request, "machines/machines.html", context)

def kafka_test(request):
    producer = KafkaProducer(bootstrap_servers='kafka:9092',                            
                            security_protocol='SASL_SSL',
                            ssl_cafile='certs/CARoot.pem',
                            ssl_certfile='certs/certificate.pem',
                            ssl_keyfile='certs/key.pem',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username='django',
                            sasl_plain_password='django',
                            ssl_check_hostname=False,
                            api_version=(2,7,0),
                            value_serializer=lambda m: json.dumps(m).encode('latin'))

    producer.send('SCAN_REQUEST', value={"teste":"teste"})
    producer.flush()
    return HttpResponse(200)