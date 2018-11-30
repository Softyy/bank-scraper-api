import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from TD import TD

SUPPORTED_BANKS = ["TD"]

class SessionHandler():
    
    def __init__(self,bank_name):
        if (bank_name not in SUPPORTED_BANKS):
            raise Exception(f'The bank {bank_name} is currently not supported.')

        self.bank_name = bank_name
        self.bank = TD()

    def set_browser_options(self):
        self.options = Options()
        self.options.set_preference("browser.download.folderList",2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir",os.path.join(os.path.dirname(os.path.realpath(__file__)),"data"))
        self.options.set_preference("browser.download.useDownloadDir", True)
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv,application/csv,text/plan,text/comma-separated-values,application/octet-stream")
    
    def start_session(self):
        self.set_browser_options()
        self.driver = webdriver.Firefox(firefox_options=self.options)
        print("Session Started")

    def close_session(self):
        self.driver.close()
        print("Session Closed")

    def establish_session(self,user_name=None,password=None,service_name=None):

        self.driver.get(self.bank.get_login_page(service_name))

        try:
            login_form_username = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, self.bank.username_html_id)))
            login_form_username.clear()
            login_form_username.send_keys(user_name)

            login_form_password = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, self.bank.password_html_id)))
            login_form_password.clear()
            login_form_password.send_keys(password)

            submit_button = self.driver.find_element_by_xpath(self.bank.login_submit_xpath)
            submit_button.click()

            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, 'error')))
                self.driver.close()
                print("An Error Occurred on the banks end.")
                return 
            except TimeoutException:
                print("You've been logged in.")

        except TimeoutException:
            print("Session could not be established")
            self.driver.close()
            return

    def retrieve_transactions_for(self,key_word=None,cycle_to_retrieve="0",format_to_retrieve="CSV"):
        if (cycle_to_retrieve not in self.bank.cycle_selector_options):
            print(f'Your bank only supports the cycle options {self.bank.cycle_selector_options}')
            return

        if (format_to_retrieve not in self.bank.format_selector_options):
            print(f'Your bank only supports the format options {self.bank.format_selector_options}')
            return

        #select page to view statements
        print("Clicking Account Link")
        WebDriverWait(self.driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,self.bank.account_details_frame_name)))
        anchor_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.bank.account_anchor_xpath % key_word)))
        anchor_link.click()

        #reset the driver context.
        self.driver.switch_to.default_content()

        #select the cycle you'd like to view.
        print('Selecting cycle')
        cycle_selector = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, self.bank.cycle_selector_id)))
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'option[value="{cycle_to_retrieve}"]')))
        Select(cycle_selector).select_by_value(cycle_to_retrieve)
        
        #select the format you'd like to have.
        print('Selecting format of data')
        format_selector = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, self.bank.format_selector_id)))
        Select(format_selector).select_by_value(format_to_retrieve)
        
        #download the file.
        print('Downloading selected data')
        download_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, self.bank.download_transaction_button_xpath)))
        download_button.click()
        