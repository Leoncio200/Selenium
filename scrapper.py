from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from acciones import seleccionar, click, extract_table, send_keys, exctract_info
import json

class Scrapper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.driver = None
        self.wait = None
        options = Options()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        self.config = self.load_config()

    def load_config(self):
            with open(self.config_file, 'r') as file:
                return json.load(file)

    def setup_driver(self):
            service = Service('C:/Users/Leoncio Pimentel/Documents/chromeDriver/chromedriver-win64/chromedriver-win64/chromedriver.exe')
            self.driver = webdriver.Chrome(service=service, options=Options())
            self.wait = WebDriverWait(self.driver, 20)

    def ejecutar(self):
        for page in self.config['pages']:
            self.driver.get(page['url'])
            for action in page['actions']:
                if action['type_action'] == "seleccionar":
                    seleccionar(self.driver, self.wait, action, page['name_page'])
                elif action['type_action'] == "click":
                    click(self.driver, self.wait, action, page['name_page'])
                elif action['type_action'] == "extraer_tabla":
                    extract_table(self.driver, self.wait, action, page['name_page'])
                elif action['type_action'] == "buscar":
                    send_keys(self.driver, self.wait, action, page['name_page'])
                elif action['type_action'] == "extraer_info":
                    exctract_info(self.driver, self.wait, action, page['name_page'])    
                

    def close(self):
        if self.driver:
            self.driver.quit()
