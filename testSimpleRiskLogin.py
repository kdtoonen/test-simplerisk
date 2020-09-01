from selenium import webdriver
import pytest
import time
from chromedriver_py import binary_path

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-user-media-security=true")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument("--headless")


@pytest.fixture(scope="function")
def setup(request):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1600, 1200)
    request.cls.driver = driver

    yield driver
    driver.close()


@pytest.mark.usefixtures("setup")
class TestSecuritySimpleRisk:
    def test_login_admin_ok(self):
        self.go_to_login_page()
        self.fill_out_username_and_password_in_login_screen("user", "user")
        self.submit_login_page()
        assert "Governance" in self.driver.page_source

    def test_login_admin_wrong_password(self):
        self.go_to_login_page()
        self.fill_out_username_and_password_in_login_screen("admin", "asfdsafafafd")
        self.submit_login_page()
        assert "Invalid username or password" in self.driver.page_source

    def test_login_unknown_user(self):
        self.go_to_login_page()
        self.fill_out_username_and_password_in_login_screen("pietje", "admin")
        self.submit_login_page()
        assert "Invalid username or password" in self.driver.page_source

    def go_to_login_page(self):
        self.driver.get('https://demo.simplerisk.com/')

    def fill_out_username_and_password_in_login_screen(self, username, password):
        self.driver.find_element_by_id("user").send_keys(username)
        self.driver.find_element_by_id("pass").send_keys(password)

    def submit_login_page(self):
        self.driver.find_element_by_name("submit").click()