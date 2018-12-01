from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_SERVICE = 'easyweb'
DEFAULT_URL = 'https://easyweb.td.com'

INVESTMENT_SERVICE = 'webbroker'
INVESTMENT_URL = 'https://webbroker.td.com'

SERVICES = [DEFAULT_SERVICE,INVESTMENT_SERVICE]

class TD():

    username_html_id = 'username'
    password_html_id = 'password'
    login_submit_xpath = "//button[@type='submit']"

    account_details_frame_name = 'tddetails'

    account_anchor_xpath = '//a[contains(.,"%s")]'

    cycle_selector_id = 'cycles' 
    cycle_selector_options = ['0','1','2','3','4','5','6'] # 0 = current, 1 = last cycle, 2 = 2 cycles ago, 3 = etc

    format_selector_id = 'downloadFormats'
    format_selector_options = ['DEF','OFC','OFX','QBO','CSV','ASO']

    download_transaction_button_xpath = '//a[contains(.,"Download")]'

    def get_login_page(self,service_name=DEFAULT_SERVICE,url=None):

        if (service_name is None):
            service_name = DEFAULT_SERVICE

        if (url is not None):
            return url
        elif (service_name==DEFAULT_SERVICE):
            return DEFAULT_URL
        elif (service_name==INVESTMENT_SERVICE):
            return INVESTMENT_URL
        else:
            raise Exception(f'Unknown service: {service_name}, maybe try passing the url via the key arg "url"')

    def login(self,driver,selection_params=None,url=None,user_name=None,password=None):
        if (selection_params is None):
            print(f'You didn\'t select any additional params, just so you know this cli supports {SERVICES}')
        driver.get(self.get_login_page(selection_params,url=url))

        if (user_name is None):
            user_name = input("Please enter your TD username: ")

        if (password is None):
            password = input("Please enter your TD password: ")

        login_form_username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, self.username_html_id)))
        login_form_username.clear()
        login_form_username.send_keys(user_name)

        login_form_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, self.password_html_id)))
        login_form_password.clear()
        login_form_password.send_keys(password)

        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, self.login_submit_xpath)))
        submit_button.click()

        return driver


    def navigate_to_downloads(self,driver,account_selector=None,data_format='CSV'):
        if (data_format not in self.format_selector_options):
            print(f'The data format {data_format} isn\'t supported, TD only takes {self.format_selector_options}')
            return 

        #select page to view statements
        print("Clicking Account Link")
        WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,self.account_details_frame_name)))
        anchor_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//a[contains(.,"{account_selector}")]')))
        anchor_link.click()
        
        #reset the driver context.
        driver.switch_to.default_content()

        #select the format you'd like to have.
        print('Selecting format of data')
        format_selector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, self.format_selector_id)))
        Select(format_selector).select_by_value(data_format)

        return driver

    def select_cycle_to_download(self,driver,cycle_to_retrieve='0'):
        #select the cycle you'd like to view.
        print('Selecting cycle')
        cycle_selector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, self.cycle_selector_id)))
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'option[value="{cycle_to_retrieve}"]')))
        Select(cycle_selector).select_by_value(cycle_to_retrieve)

        #download the file.
        print('Downloading selected data')
        download_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, self.download_transaction_button_xpath)))
        download_button.click()

        return driver