from enum import Enum, auto
import json
import requests
import time
from bs4 import BeautifulSoup as bs

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

class GeneralTracker(object):
    """
        This is a class for General Price Tracker
    """
    
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
                    return GeneralTracker.Notification(json_dct['notification_type'], json_dct['address'])
                else:
                    return  GeneralTracker.Notification(json_dct['notification_type'], json_dct['address'], json_dct["carrier"])
            except KeyError:
                print("Make sure that you have proper json with appropriate keys. For Example: Carrier is set if you have sms as a notification")

    class GeneralItem(object):
        """
            This is a general item which we can use to track
        """
        def __init__(self, url: str, check: CheckType, htmlId: str, check_period: int, notify: Notification_Type):
            self.url = url
            self.check = check
            self.htmlId = htmlId
            self.check_period = check_period
            self.notify = notify

        # Custom Deserilize method
        @staticmethod
        def from_json(json_dct):
            try:
                return GeneralTracker.GeneralItem(json_dct["url"], json_dct["check"], json_dct["htmlId"], json_dct["check_period"], json_dct["notify"])
            except KeyError:
                return GeneralTracker.Notification.from_json(json_dct)

    #######################################################################################################################################
    def __init__(self, config: dict[str: any]) -> None:
        print("This worked somehow")
        self.config = config 
