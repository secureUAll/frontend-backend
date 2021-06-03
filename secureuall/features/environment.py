from behave import fixture, use_fixture
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
import os


@fixture
def browser_firefox(context, timeout=30, **kwargs):
    # Set up selenium
    # If env variable is set, run on headless mode (because of GitHub actions)
    opts = Options()
    print("HEADLESS?", os.environ.get('behaveHeadless', False))
    if os.environ.get('behaveHeadless', False):
        opts.headless = True
    context.browser = WebDriver(options=opts)
    context.browser.implicitly_wait(10)
    # Schedule clean up for when tests end
    context.add_cleanup(context.browser.quit)


def before_all(context):
    use_fixture(browser_firefox, context)
