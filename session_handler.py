import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from institutions.TD import TD
from institutions.AMEX import AMEX

SUPPORTED_BANKS = ["TD","AMEX"]

class SessionHandler():
    
    def __init__(self,bank_name):
        if (bank_name not in SUPPORTED_BANKS):
            raise Exception(f'The bank {bank_name} is currently not supported.')

        self.bank_name = bank_name

        if (bank_name=='TD'):
            self.bank = TD()
        elif (bank_name=='AMEX'):
            self.bank = AMEX()

    def set_browser_options(self):
        self.options = Options()
        self.options.set_preference("browser.download.folderList",2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir",os.path.join(os.path.dirname(os.path.realpath(__file__)),"data"))
        self.options.set_preference("browser.download.useDownloadDir", True)
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,text/x-csv,application/csv,application/x-csv,text/plain,text/comma-separated-values,text/x-comma-separated-values,application/octet-stream,application/vnd.ms-excel,text/tab-separated-values")
    
    def start_session(self):
        self.set_browser_options()
        self.driver = webdriver.Firefox(firefox_options=self.options)
        print("Session Started")

    def close_session(self):
        self.driver.close()
        print("Session Closed")

    def establish_session(self,user_name=None,password=None,service_name=None):
        self.driver = self.bank.login(self.driver, selection_params=service_name, user_name=user_name, password=password)

    def retrieve_transactions_for(self,key_word=None,cycle_to_retrieve=None,format_to_retrieve="CSV"):
        self.driver = self.bank.navigate_to_downloads(self.driver,account_selector=key_word,data_format=format_to_retrieve)
        self.driver = self.bank.select_cycle_to_download(self.driver,cycle_index=cycle_to_retrieve)
        self.close_session()
        