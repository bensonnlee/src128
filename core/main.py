import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decouple import config

from core.driver import Driver

driver = Driver()


def authenticate(
    username: str,
    password: str,
):
    driver.start_login()
    execution = driver.get_execution()
    referer = driver.login(execution, username, password)
    driver.end()

    if "?ticket=ST" in referer:
        return True
    else:
        return False


def generate_id(
    username: str,
    password: str,
):
    driver.start_login()
    execution = driver.get_execution()
    referer = driver.login(execution, username, password)
    bearer = driver.login_finish(referer)
    barcode_id = driver.barcode(bearer)
    driver.end()

    return barcode_id
