import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

def _make_driver(browser: str, headless: bool, grid_url: str | None):
    browser = browser.lower()
    if browser == "chrome":
        chrome_opts = ChromeOptions()
        if headless:
            # Chrome 115+ 推荐 headless=new
            chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        if grid_url:
            return webdriver.Remote(command_executor=grid_url, options=chrome_opts)
        else:
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_opts)

    if browser == "firefox":
        ff_opts = FirefoxOptions()
        if headless:
            ff_opts.add_argument("-headless")
        if grid_url:
            return webdriver.Remote(command_executor=grid_url, options=ff_opts)
        else:
            from selenium.webdriver.firefox.service import Service
            service = Service(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=ff_opts)

    raise ValueError(f"Unsupported browser: {browser}")

def pytest_addoption(parser):
    parser.addoption("--browsers", action="append", default=None,
                     help="browsers to run, e.g. --browsers chrome --browsers firefox")
    parser.addoption("--base-url", action="store", default=os.getenv("BASE_URL", "https://ems.example.com"))
    parser.addoption("--grid-url", action="store", default=os.getenv("SELENIUM_GRID_URL"))
    parser.addoption("--headless", action="store_true", default=(os.getenv("HEADLESS","1") == "1"))

@pytest.fixture(scope="session")
def cfg(pytestconfig):
    browsers = pytestconfig.getoption("--browsers")
    if not browsers:
        # 默认同时跑 Chrome 与 Firefox
        browsers = (os.getenv("BROWSERS","chrome,firefox")).split(",")
    return {
        "browsers": [b.strip() for b in browsers],
        "base_url": pytestconfig.getoption("--base-url"),
        "grid_url": pytestconfig.getoption("--grid-url"),
        "headless": pytestconfig.getoption("--headless"),
    }

@pytest.fixture(params=lambda cfg: cfg["browsers"], scope="function")
def driver(request, cfg):
    drv = _make_driver(request.param, cfg["headless"], cfg["grid_url"])
    drv.set_window_size(1920, 1080)
    yield drv
    drv.quit()
