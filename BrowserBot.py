import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.firefox.options import Options as OptionsFF
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from Robot import Robot

class SeleRobot(Robot):

    def __init__(self, reports=None, driver_name=None, mode=None, driverDirectory=None):
        if reports is None:
            reports = []
        Robot.__init__(self, reports)
        if driver_name is None:
            driver_name = self.config.robot['driverName']
        env = self.config.robot["env"]
        if mode is None:
            mode = self.get_mode_from_config()
        service_args_value = ""

        if driver_name == 'Firefox':
            ff_profile = webdriver.FirefoxProfile()

            ff_profile.set_preference("network.proxy.type", 1)
            ff_profile.set_preference("network.proxy.http_port", 8080)
            ff_profile.set_preference("network.proxy.http", "surf-sccc.pasi.log.intra.laposte.fr")
            ff_profile.set_preference("network.proxy.ssl_port", 8080)
            ff_profile.set_preference("network.proxy.ssl", "surf-sccc.pasi.log.intra.laposte.fr")
            ff_profile.set_preference("network.proxy.socks_port", 8080)
            ff_profile.set_preference("network.proxy.socks", "surf-sccc.pasi.log.intra.laposte.fr")
            ff_profile.set_preference("network.proxy.ftp_port", 8080)
            ff_profile.set_preference("network.proxy.ftp", "surf-sccc.pasi.log.intra.laposte.fr")
            ff_profile.set_preference("network.proxy.socks_username", "PPDJ824")
            ff_profile.set_preference("network.proxy.socks_password", "Lilalou07PANDORE")

            ff_profile.set_preference('browser.cache.disk.enable', False)
            ff_profile.set_preference('browser.cache.memory.enable', False)
            ff_profile.set_preference('browser.cache.offline.enable', False)
            ff_profile.set_preference('network.cookie.cookieBehavior', 2)

            ff_profile.update_preferences()

            options_ff = OptionsFF()
            if mode == "headless":
                options_ff.add_argument("--no-sandbox")
                # optionsFF.add_argument("--window-size=1900,1080")
                options_ff.add_argument("--width=1920")
                options_ff.add_argument("--height=1080")
                options_ff.add_argument("--disable-extensions")
                options_ff.add_argument("--disable-dev-shm-usage")
                options_ff.add_argument("--ignore-certificate-errors")
                options_ff.add_argument("--disable-gpu")
                options_ff.add_argument("--headless")

            self.driver = webdriver.Firefox(
                firefox_profile=ff_profile,
                options=options_ff
            )

        elif driver_name == 'IE':
            if driverDirectory is None:
                self.driver = webdriver.Ie(self.config.robot["repertoireDriver"])
            else:
                self.driver = webdriver.Ie(driverDirectory)
        else:  # Chrome
            options = OptionsChrome()
            options.add_argument("--incognito")
            # if env != 'dev':
            #     # options.add_argument('--proxy-server=http://localhost:3128')
            #     service_args_value = ['--verbose', '--log-path=/tmp/chromedriver.log']

            if mode == "headless":
                options.add_argument("--no-sandbox")
                options.add_argument("--headless")
                options.add_argument("--window-size=1900,1080")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--ignore-certificate-errors")
                options.add_argument("--disable-gpu")

            options.add_argument("--start-maximized")
            if "download_directory" in self.config.robot:
                prefs = {'download.default_directory': self.config.robot["download_directory"]}
                options.add_experimental_option('prefs', prefs)

            driver_path = self.config.robot["repertoireDriver"]

            self.driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)

    def main(self):
        return

    def run(self):
        try:
            self.main()
        except Exception:

            self.save_screenshot()
            self.driver.close()
            raise
        self.driver.close()

    def save_screenshot(self):
        logs = self.config.robot["log"]["dir"]
        timestamp = str(time.time())
        self.driver.save_screenshot("%s/ss_%s.png" % (logs, timestamp))
        title = self.driver.title
        source = self.driver.page_source
        url = self.driver.current_url
        file_path = "%s/html_%s.log" % (logs, timestamp)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(url)
            file.write(title)
            file.write(source)
            file.close()
        return timestamp

    def get_mode_from_config(self):
        if "selenium_mode" in self.config.robot:
            return self.config.robot["selenium_mode"]
        return "headful"

    def launch_chrome(self, url, timeout=10):
        self.driver.set_page_load_timeout(timeout)

        self.driver.get(url)

    def scroll(self, amount):
        self.driver.execute_script("window.scroll(0, %d)" % amount)

    def wait_for_element(self, method, argument, name, timeout=10, condition="visible"):
        try:
            if condition == "clickable":
                cond = ec.element_to_be_clickable((getattr(By, method), argument))
            elif condition == "invisible":
                cond = ec.invisibility_of_element_located((getattr(By, method), argument))
            else:
                cond = ec.presence_of_element_located((getattr(By, method), argument))
            WebDriverWait(self.driver, timeout).until(cond)
        except TimeoutException as e:
            raise e
        else:          
            if condition != "invisible":
                return self.driver.find_element(getattr(By, method), argument)
            else:
                return

    def switch_to_window(self, title):
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            if self.driver.title == title:
                break

    def hover(self, method, argument):
        builder = ActionChains(self.driver)
        element = self.driver.find_element(getattr(By, method), argument)
        builder.move_to_element(element).perform()

    def close(self):
        self.driver.close()

    def refresh(self):
        self.driver.refresh()



selenium = SeleRobot()