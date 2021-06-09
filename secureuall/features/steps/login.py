from behave import *

from login.models import User, UserAccessRequest


@given(u'user "{username}" admin "{admin}" logged in')
def step_impl(context, username, admin):
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
    else:
        u = User.objects.create_user(username=username, email=username)
        u.first_name = username
    # Set admin attribute
    u.is_admin = (admin == 'true')
    u.save()
    context.user = u
    # Log user in
    email_field = context.browser.find_element_by_id('loginEmailAddres')
    email_field.send_keys(context.user.email)
    context.browser.find_element_by_css_selector('form button.btn').click()


@given(u'user has access request "{state}"')
def step_impl(context, state):
    request = UserAccessRequest.objects.create(
        user=context.user,
        role='S',
        motive='Loren ipsum',
        notes='Loren ipsum',
        machines='abc.pt'
    )
    if state == 'denied':
        request.pending = False
    elif state == 'accepted':
        request.pending = False
        request.approved = True
    request.save()
    print("Building request", request)
    print("Pending?", request.pending)
    print("Approved?", request.approved)
    print("User", context.user.username)
    print("User", context.user.accessRequest.all())