from behave import *

# GIVEN ------------------------------------------------
# view can be url or view name
# https://behave-django.readthedocs.io/en/latest/webbrowser.html
@given(u'browser at "{view}"')
def step_impl(context, view):
    context.browser.get(context.get_url(view))


@given(u'refresh')
def step_impl(context):
    context.browser.refresh()


# WHEN ------------------------------------------------
@when(u'user types "{text}" at element with id "{eid}"')
def step_impl(context, text, eid):
    element = context.browser.find_element_by_id(eid)
    element.send_keys(text)


@when(u'user clicks at element with css "{css}"')
def step_impl(context, css):
    element = context.browser.find_element_by_css_selector(css)
    element.click()


# THEN ------------------------------------------------
@then(u'url without data is "{url}"')
def step_impl(context, url):
    context.test.assertEqual(context.browser.current_url.split("?")[0], context.get_url(url))


@then(u'element with css "{css}" text is "{text}"')
def step_impl(context, css, text):
    element = context.browser.find_element_by_css_selector(css)
    context.test.assertEqual(
        element.text, text,
        msg=f"Element with css '{css}' does not have expected text: '{text}'!"
    )


@then(u'element with css "{css}" text contains "{text}"')
def step_impl(context, css, text):
    element = context.browser.find_element_by_css_selector(css)
    context.test.assertTrue(
        text in element.text,
        msg=f"Element with css '{css}' does not contain expected text!\nExpected:{text}\nGot:{element.text}"
    )


@then(u'element with id "{id}" attribute "{attr}" has value "{value}"')
def step_impl(context, id, attr, value):
    element = context.browser.find_element_by_id(id)
    context.test.assertEqual(
        element.get_attribute(attr), value,
        msg=f"Element with id '{id}' attribute {attr} does not have expected value!"
    )


@then(u'element with css "{css}" is {visible}')
def step_impl(context, css, visible):
    element = context.browser.find_element_by_css_selector(css)
    if visible == 'visible':
        context.test.assertTrue(
            element.is_displayed(),
            msg='Element expected to be visible it not!'
        )
    else:
        context.test.assertFalse(
            element.is_displayed(),
            msg='Element expected to be invisible it not!'
        )


@then(u'element with xpath "{xpath}" text is "{text}"')
def step_impl(context, xpath, text):
    element = context.browser.find_element_by_xpath(xpath)
    context.test.assertEqual(
        element.text, text,
        msg=f"Element with xpath '{xpath}' does not have expected text: '{text}'!"
    )


@then(u'element with xpath "{xpath}" attribute "{attr}" has value "{value}"')
def step_impl(context, xpath, attr, value):
    element = context.browser.find_element_by_xpath(xpath)
    context.test.assertEqual(
        element.get_attribute(attr), value,
        msg=f"Element with xpath '{xpath}' attribute {attr} does not have expected value!"
    )
