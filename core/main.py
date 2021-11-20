from core.driver import Driver

driver = Driver()


def generate_id(
    username: str,
    password: str,
):
    driver.start_login()
    execution = driver.get_execution()
    url = driver.login(execution, username, password)
    bearer = driver.login_finish(url)
    barcode_id = driver.barcode(bearer)

    return barcode_id
