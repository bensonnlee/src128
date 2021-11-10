from api.driver import Driver

driver = Driver()


def generate_id():
    driver.start_login()
    execution = driver.get_execution()
    url = driver.login(execution)
    bearer = driver.login_finish(url)
    barcode_id = driver.barcode(bearer)

    return barcode_id
