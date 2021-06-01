from behave import *

from machines.models import Machine, MachineUser


@given(u'user has machine')
def step_impl(context):
    m = Machine.objects.create(dns='abc.pt')
    MachineUser.objects.create(
        user=context.user,
        machine=m,
        userType='S'
    )
