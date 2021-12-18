import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.driver import Driver

driver = Driver()


def authenticate(
    username: str,
    password: str,
) -> bool:
    """
    Authenticate user with username and password.

    :param username: username
    :param password: password

    :return: True if authentication was successful, False otherwise
    """
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
) -> tuple:
    """
    Generate new barcode id

    :param username: username
    :param password: password
    :param fusion_key: fusion key

    :return: tuple containing the new barcode id and a valid fusion key
    """
    # if fusion key is provided, skip to the last request
    if fusion_key:
        try:
            barcode_id = driver.barcode(fusion_key)
            return fusion_key, barcode_id
        except KeyError:
            pass

    # otherwise, go through the entire login and barcode generation process
    driver.start_login()
    execution = driver.get_execution()
    referer = driver.login(execution, username, password)
    if "?ticket=ST" not in referer:
        return "", ""

    bearer = driver.login_finish(referer)
    barcode_id = driver.barcode(bearer)

    return bearer, barcode_id
