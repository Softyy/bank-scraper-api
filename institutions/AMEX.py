from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


DEFAULT_COUNTRY = 'canada'
DEFAULT_URL = 'https://www.americanexpress.com/canada/'

SUPPORTED_COUNTIES = ['canada']

class AMEX():

    username_html_id = 'login-user'
    password_html_id = 'login-password'
  
    login_submit_id = 'login-submit'
    login_submit_xpath = ''

    xpath_for_statement_options = '//button[@title="Statement"]'

    xpath_for_export_data = '//a[@title="Export Statement Data"]'

    format_selector_options = ['CSV','QTF','ms_money','quickbooks','quicken']

    select_card_id = 'selectCard10'

    cycle_selector_id = 'cycles' 
    cycle_mutli_select = True
    cycle_selector_options = ['radioid00','radioid01','radioid02','radioid03','radioid04','radioid05','radioid06'] # 0 = current, 1 = last cycle, 2 = 2 cycles ago, 3 = etc

    download_transaction_button_xpath = '//a[contains(.,"Download Now")]'

    def get_login_page(self,country_name=DEFAULT_COUNTRY,url=None):
        if (country_name is None):
            country_name = DEFAULT_COUNTRY

        if (url is not None):
            return url
        elif (country_name==DEFAULT_COUNTRY):
            return DEFAULT_URL
        else:
            raise Exception(f'Unknown country: {country_name}, maybe try passing the url via the key arg "url"')

    def login(self,driver,selection_params=None,url=None,user_name=None,password=None):
        if (selection_params is None):
            print(f'You didn\'t select any additional params, just so you know this cli supports {SUPPORTED_COUNTIES}')
        driver.get(self.get_login_page(selection_params,url=url))

        if (user_name is None):
            user_name = input("Please enter your AMEX username: ")

        if (password is None):
            password = input("Please enter your AMEX password: ")

        login_form_username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-user')))
        login_form_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))
        submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-submit')))

        login_form_username.send_keys(user_name)
        login_form_password.send_keys(password)
        submit_button.click()

        return driver

    def navigate_to_downloads(self,driver,account_selector=None,data_format='CSV'):
        if (data_format not in self.format_selector_options):
            print(f'The data format {data_format} isn\'t supported, AMEX only takes {self.format_selector_options}')
            return driver

        if (account_selector is not None):
            print('AMEX has an ancient interface for this, this tool expects an ID in the form "selectCardXX"')
            if 'selectCard' not in account_selector:
                print(f'key_word {account_selector} doesn\'t meet amex style.')
                driver.close()
                return

        statement_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@title="Statement"]')))
        statement_button.click()
        anchor_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@title="Export Statement Data"]')))
        anchor_link.click()
        radio = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, data_format)))
        radio.click()
        input_download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, account_selector)))
        input_download.click()

        return driver

    def select_cycle_to_download(self,driver,cycle_index=None):
        if (cycle_index == None):
            print(f'You didn\'t select a cycle to download, your banks supports multi_select={self.cycle_mutli_select} and options={self.cycle_selector_options} and we\'ve defaulted to {self.cycle_selector_options[0]}')
            cycle_index = [self.cycle_selector_options[0]]

        elements = [WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, ci))) for ci in cycle_index]

        for element in elements:
            element.click()

        download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(.,"Download Now")]')))
        download.click()
        return driver

    
    