import pytest

from selenium import webdriver
from config import STAGE_LK, LOGIN, PASSWORD
from modules.front.box_page import BoxPageHelper
from modules.front.lk_page import LkPageHelpers
from modules.front.reg_page import RegPageHelpers


def func_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('ignore-certificate-errors')
    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.media_stream_mic": 1,  # 1:allow, 2:block
            "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block
            "profile.default_content_setting_values.geolocation": 1,  # 1:allow, 2:block
            "profile.default_content_setting_values.notifications": 1  # 1:allow, 2:block
        })

    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1280,1024")

    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(10)
    driver.maximize_window()

    return driver


@pytest.fixture()
def browser_module():
    driver = func_browser()

    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def browser_module():
    driver = func_browser()

    yield driver
    driver.quit()


@pytest.fixture
def correct_auth(browser_module):
    lk_page = LkPageHelpers(browser_module)
    lk_page.go_to_site(STAGE_LK)
    lk_page.enter_to_email(LOGIN)
    lk_page.enter_to_password(PASSWORD)
    lk_page.press_to_sign_in()
    lk_page.get_logout_name()
    yield browser_module


# Необходимо придумать ожидание активации кнопки "Создать набор", т.к. на момент клика, кнопка неактивна
@pytest.fixture
def get_new_box(correct_auth):
    box = BoxPageHelper(correct_auth)
    box.press_to_create_box()
    yield correct_auth


@pytest.fixture
def sign_in(browser_module):
    lk_page = LkPageHelpers(browser_module)
    lk_page.go_to_site(STAGE_LK)
    yield browser_module


@pytest.fixture
def form_reg(browser_module):
    reg_page = RegPageHelpers(browser_module)
    reg_page.go_to_site(STAGE_LK)
    reg_page.go_to_form_reg()
    yield browser_module


@pytest.fixture
def correct_filling_reg_form(sign_in):
    reg_page = RegPageHelpers(sign_in)
    reg_page.go_to_form_reg()
    reg_page.enter_to_email()
    reg_page.enter_to_pass()
    reg_page.enter_or_select_to_entity()
    reg_page.enter_entity_address()
    reg_page.enter_to_phone()
    reg_page.enter_to_ogrn()
    reg_page.enter_to_kpp()
    reg_page.enter_to_pc()
    reg_page.enter_to_kc()
    reg_page.enter_to_bik()
    reg_page.enter_to_inn()
    reg_page.enter_to_fio_direct()
    yield sign_in