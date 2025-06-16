import os
import sys
import uuid
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.driver import Driver

driver = Driver()

# Mock credentials - only this specific combination will be mocked
MOCK_USERNAME = "testuser"
MOCK_PASSWORD = "testpass"

def authenticate(
    username: str,
    password: str,
) -> bool:
    """
    Authenticate user with username and password.
    Uses mock implementation for testuser/tsetpass, otherwise uses original Driver.

    :param username: username
    :param password: password

    :return: True if authentication was successful, False otherwise
    """
    # Mock implementation for specific credentials
    if username == MOCK_USERNAME and password == MOCK_PASSWORD:
        return True
    
    # Original implementation for all other credentials
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
    Uses mock implementation for testuser/testpass, otherwise uses original Driver.

    :param username: username
    :param password: password
    :param fusion_key: fusion key

    :return: tuple containing the new barcode id and a valid fusion key
    """
    # Mock implementation for specific credentials
    if username == MOCK_USERNAME and password == MOCK_PASSWORD:
        # If fusion key is provided, generate a mock barcode with it
        if fusion_key:
            mock_barcode_id = f"&{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}&"
            return fusion_key, mock_barcode_id
        
        # Generate mock fusion key and barcode id
        mock_fusion_key = "mock_" + str(uuid.uuid4()).replace("-", "")[:50] + "_token"
        mock_barcode_id = f"&{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4().int)[:6]}&"
        
        return mock_fusion_key, mock_barcode_id
    
    # Original implementation for all other credentials
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
