from enum import Enum, auto
from importlib.resources import path
from tabnanny import check
from xmlrpc.client import boolean
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC


class CheckType(Enum):
    """
        This is a kind of check we're doing ENUM
    """
    LESS_THAN = auto()
    GREATER_THAN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    

class Notification_Type(Enum):
    """
        This is a notification type that is currently accepted
    """
    EMAIL = auto()
    SMS = auto()
 

class Notification(object):
    def __init__(self, notification_type: Notification_Type, address: str, carrier: str=None):
        if carrier is None:
            self.notification_type = notification_type
            self.address = address
            self.carrier = carrier
        else:
            self.notification_type = notification_type
            self.address = address

    @staticmethod
    def from_json(json_dct):
        try:
            if json_dct["notification_type"] == 1:
                return Notification(json_dct['notification_type'], json_dct['address'])
            else:
                return Notification(json_dct['notification_type'], json_dct['address'], json_dct["carrier"])
        except KeyError:
            print("Make sure that you have proper json with appropriate keys. For Example: Carrier is set if you have sms as a notification")

class GeneralItem(object):
    """
        This is a general item which we can use to track
    """
    def __init__(self, url: str, check: CheckType, check_against: any, htmlId: str, check_period: int, notify: Notification_Type):
        self.url = url
        self.check = check
        self.check_against = check_against
        self.htmlId = htmlId
        self.check_period = check_period
        self.notify = notify


    # Custom Deserilize method
    @staticmethod
    def from_json(json_dct):
        try:
            return GeneralItem(json_dct["url"], json_dct["check"], json_dct["check_against"], json_dct["htmlId"], json_dct["check_period"], json_dct["notify"])
        except KeyError:
            return Notification.from_json(json_dct)

    def track(self) -> boolean:
        # Get the attribute
        value = self.__getattribute()

        # Check to see if the returned attribute requires notification
        if self.check == 1:
            return value < self.check_against
        elif self.check == 2:
            return value > self.check_against
        elif self.check == 3:
            return value == self.check_against
        elif self.check == 4:
            self.check != self.check_against
        else:
            return False



    def __getattribute(self) -> any:
        # Setup selenium
        options = Options()
        options.headless = True
        dr = webdriver.Chrome("./chromedriver", options=options)

        # request the webpage
        dr.get(self.url)
        dr.implicitly_wait(5)

        # create beautiful soup object to parse the html page
        soup = bs(dr.page_source, 'html.parser')
        dr.quit()

        # return the attribute
        # Since Amazon wants to do things differntly, had to do this manually
        if "amazon.com" in self.url:
            attr = soup.find('span', {'class': self.htmlId})
        elif "ebay.com" in self.url:
            attr = soup.find('span', {'id': self.htmlId})
        elif "coinmarketcap.com" in self.url:
            attr = soup.find('div', {'class': self.htmlId})
        else:
            attr = soup.find(id=self.htmlId)

        if attr is None:
            print("There was a error with trying to find the htmlId. Please Try Again!! ")
            exit()
        # Get the attributes text and convert it into into if we're comparing with <  or >
        # Clean up the string
        attr_str = attr.get_text().replace('.', '').replace('$', '').replace('US', '').replace(',','').strip()

        # if comparing with < or >
        if self.check == 1 or self.check == 2:
            return int(attr_str)
        else:
            return attr_str


    def valid_check(self) -> bool:
        if self.check == 1 or self.check == 2:
            if type(self.check_against) is str:
                return False
            return True
        return True
            
