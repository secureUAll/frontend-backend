from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from kafka import KafkaProducer
from django.http import HttpResponse, Http404
import logging
import json
from django.core import serializers
import machines.dataContext as dataContext
from login.models import User

from .models import Machine, MachineUser, Subscription, Scan, MachineService, MachinePort, Vulnerability, VulnerabilityComment

logging.basicConfig(level=logging.DEBUG)
# Create your views here.


@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def MachinesView(request, id):
    try:
        machine = Machine.objects.get(id=id)
        context = {
            'machine': machine
        }
    except Machine.DoesNotExist:
        raise Http404('Machine does not exist')
    return render(request, "machines/machines.html", context)


@login_required
@user_passes_test(User.has_access, login_url="/welcome")
def RequestsView(request, *args, **kwargs):
    context = dataContext.machineContext
    return render(request, "machines/requests.html", context)


@login_required
@user_passes_test(User.has_access, login_url="/welcome")
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

    producer.send('FRONTEND', key=b'SCAN', value={"MACHINE":"127.0.1.3"})
    producer.flush()
    return HttpResponse(200)