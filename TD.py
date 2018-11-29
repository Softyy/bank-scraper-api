DEFAULT_SERVICE = 'easyweb'
DEFAULT_URL = 'https://easyweb.td.com'

INVESTMENT_SERVICE = 'webbroker'
INVESTMENT_URL = 'https://webbroker.td.com'

class TD():

    username_html_id = 'username'
    password_html_id = 'password'
    login_submit_xpath = "//button[@type='submit']"

    account_details_frame_name = 'tddetails'

    account_anchor_xpath = '//a[contains(@class, "td-link-standalone") and contains(.,%s)]'

    cycle_selector_id = 'cycle' 
    cycle_selector_options = [0,1,2,3,4,5,6] # 0 = current, 1 = last cycle, 2 = 2 cycles ago, 3 = etc

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

    