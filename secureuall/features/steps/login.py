from behave import *

from login.models import User


@given(u'user "{username}" admin "{admin}" logged in')
def step_impl(context, username, admin):
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
    else:
        u = User.objects.create_user(username=username, email=username)
    # Set admin attribute
    u.is_admin = (admin == 'true')
    u.save()
    # Log user in
    email_field = context.browser.find_element_by_id('loginEmailAddres')
    email_field.send_keys(u.email)
    context.browser.find_element_by_css_selector('form button.btn').click()

