from behave import fixture, use_fixture
from selenium.webdriver.firefox.webdriver import WebDriver


@fixture
def browser_firefox(context, timeout=30, **kwargs):
    # Set up selenium
    context.browser = WebDriver()
    context.browser.implicitly_wait(10)
    # Schedule clean up for when tests end
    context.add_cleanup(context.browser.quit)


def before_all(context):
    use_fixture(browser_firefox, context)
