import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.driver import Driver

driver = Driver()


def authenticate(
    username: str,
    password: str,
):
    driver.start_login()
    execution = driver.get_execution()
    referer = driver.login(execution, username, password)

    if "?ticket=ST" in referer:
        return True
    else:
        return False


def generate_id(
    username: str,
    password: str,
    fusion_key: str,
):
    if fusion_key:
        try:
            barcode_id = driver.barcode(fusion_key)
            return fusion_key, barcode_id
        except KeyError:
            pass

    driver.start_login()
    execution = driver.get_execution()
    referer = driver.login(execution, username, password)
    bearer = driver.login_finish(referer)
    barcode_id = driver.barcode(bearer)

    return bearer, barcode_id
