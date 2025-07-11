import logging
from urllib.parse import quote

import requests
from decouple import config

# Set up console logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
log.addHandler(console_handler)


class Driver:
    ses = requests.Session()

    def __init__(
        self,
    ):
        self.execution = ""

    def start_login(
        self,
    ):
        """
        Retrieve cookies from login page and attach to session
        """
        self.ses.cookies.clear()
        url = "https://innosoftfusiongo.com/sso/login/login-start.php?id=124"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X)"
                " AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            ),
            "Accept-Language": "en-us",
        }

        self.ses.get(url, headers=headers)

    def get_execution(
        self,
    ) -> str:
        """
        Extract execution string from login page

        :return: execution string
        """
        url = "https://auth.ucr.edu/cas/login?service=https%3A%2F%2Finnosoftfusiongo.com%2Fsso%2Flogin%2Flogin-process-cas.php"

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X)"
                " AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            ),
            "Accept-Language": "en-us",
            "Referer": "https://innosoftfusiongo.com/sso/login/login-start.php?id=124",
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
        }
        resp = self.ses.get(url, headers=headers)
        log.info(f"Response text: {resp.text}")

        execution = resp.text.split('name="execution" value="')[1].split('"')[0]
        return execution

    def login(
        self,
        execution: str,
        username: str,
        password: str,
    ) -> str:
        """
        Send login paylaod to UCR CAS endpoint

        :param execution: execution string from login page
        :param username: username
        :param password: password

        :return: url with ST query parameter
        """
        url = "https://auth.ucr.edu/cas/login?service=https%3A%2F%2Finnosoftfusiongo.com%2Fsso%2Flogin%2Flogin-process-cas.php"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://auth.ucr.edu",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X)"
                " AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            ),
            "Referer": "https://auth.ucr.edu/cas/login?service=https%3A%2F%2Finnosoftfusiongo.com%2Fsso%2Flogin%2Flogin-process-cas.php",
            "Accept-Language": "en-US",
        }

        payload = f"username={quote(username)}&password={quote(password)}&execution={quote(execution)}&_eventId=submit&geolocation="

        resp = self.ses.post(url, headers=headers, data=payload)

        return resp.url

    def login_finish(
        self,
        referer: str,
    ) -> str:
        """
        Get fusion token from login finish endpoint

        :param referer: url with ST query parameter

        :return: fusion token
        """
        url = "https://innosoftfusiongo.com/sso/login/login-finish.php"

        headers = {
            "Content-Type": "multipart/form-data; boundary=",
            "Origin": "https://innosoftfusiongo.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X)"
                " AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
            ),
            "Accept-Language": "en-us",
            "Referer": referer,
            "Connection": "keep-alive",
            "Accept-Encoding": "gzip, deflate, br",
        }

        resp = self.ses.post(url, headers=headers)
        log.info(f"Response text: {resp.text}")

        bearer = resp.headers["Fusion-Token"]
        return bearer

    def barcode(
        self,
        bearer: str,
    ) -> str:
        """
        Get barcode from barcode endpoint

        :param bearer: fusion token

        :return: barcode id number
        """
        url = "https://innosoftfusiongo.com/sso/api/barcode.php?id=124"

        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json;charset=utf-8;",
            "Connection": "keep-alive",
            "Accept-Language": "en-us",
            "Authorization": f"Bearer {bearer}",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "UCRSRC/268 CFNetwork/1240.0.4 Darwin/20.6.0",
        }

        resp = self.ses.get(url, headers=headers)

        return resp.json()[0]["AppBarcodeIdNumber"]
