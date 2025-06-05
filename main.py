import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:

    #Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_request = (By.CSS_SELECTOR, '.button.round')
    comfort_type = (By.XPATH,
                      '//div[@class="tcard-title" and text()="Comfort"]/ancestor::div[contains(@class, "tcard")]')
    phone_number = (By.CLASS_NAME, 'np-button')
    add_number = (By.ID,'phone')
    next_button = (By.CSS_SELECTOR, '.button.full')
    enter_code = (By.XPATH, '//div[@class="input-container"]/input[@id="code"]')
    confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    payment_method = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card = (By.CSS_SELECTOR, '.pp-row.disabled')
    enter_number = (By.ID,'number')
    enter_card_code = (By.CSS_SELECTOR,'input#code.card-input')
    deselect = (By.CLASS_NAME, 'card-wrapper')
    click_add = (By.XPATH, '//button[@class="button full" and text()="Agregar"]')
    x_button = (By.XPATH, '(//div[contains(@class, "payment-picker") and contains(@class, "open")]//button[contains(@class, "close-button") and contains(@class, "section-close")])[1]')
    driver_message = (By.ID, 'comment')
    blanket_tishue = (By.CSS_SELECTOR, '.slider.round')
    icecream = (By.CLASS_NAME, 'counter-plus')
    request_vehicle = (By.CLASS_NAME, 'smart-button-main')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
#Prueba 1
    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.from_field)
        )
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

#Prueba 2
    def click_request_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.taxi_request)).click()
    def click_comfort_type(self):
        self.wait.until(EC.element_to_be_clickable(self.comfort_type)).click()
#Prueba 3
    def click_phone_number(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_number)).click()
    def set_phone_number(self):
        phone_element = self.wait.until(EC.element_to_be_clickable(self.add_number))
        phone_element.send_keys(data.phone_number)
        self.driver.find_element(*self.next_button).click()
    def card_code(self):
        code_field = self.wait.until(EC.presence_of_element_located(self.enter_code))
        code_field.send_keys(code)
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.confirm_button))
        confirm_button.click()

#Prueba 4
    def add_payment_method(self):
        self.driver.find_element(*self.payment_method).click()
        self.driver.find_element(*self.add_card).click()
        card_details = self.wait.until(EC.element_to_be_clickable(self.enter_number))
        card_details.send_keys(data.card_number)
        self.wait.until(EC.visibility_of_element_located(self.enter_card_code)).send_keys(data.card_code)
        self.driver.find_element(*self.deselect).click()
        self.driver.find_element(*self.click_add).click()
        close = self.wait.until(EC.element_to_be_clickable(self.x_button))
        close.click()

#Prueba 5
    def add_driver_message(self):
        self.wait.until(EC.visibility_of_element_located(self.driver_message)).send_keys(data.message_for_driver)

#Prueba 6
    def add_blanket_tishue(self):
        self.wait.until(EC.visibility_of_element_located(self.blanket_tishue)).click()
        time.sleep(3)
# Prueba 7
    def add_icecreams(self):
            self.driver.find_element(*self.icecream).click()
            self.driver.find_element(*self.icecream).click()

#Prueba 8
    def click_request_vehicle(self):
        self.driver.find_element(*self.request_vehicle).click()
        time.sleep(5)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
# no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

#Test 1
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
#Test 2
    def test_taxi_request(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()

    def test_click_comfort_type(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()

#Test 3
    def test_click_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()
        routes_page.click_phone_number()
        routes_page.set_phone_number()
        # Obtener el código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        print(f'Código de confirmación obtenido: {confirmation_code}')
        # Ingresar el código y confirmar
        code_field = routes_page.wait.until(EC.presence_of_element_located(routes_page.enter_code))
        code_field.send_keys(confirmation_code)
        confirm_button = routes_page.wait.until(EC.element_to_be_clickable(routes_page.confirm_button))
        confirm_button.click()

#Test 4
    def test_payment_method(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()
        routes_page.click_phone_number()
        routes_page.set_phone_number()
        # Obtener el código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        print(f'Código de confirmación obtenido: {confirmation_code}')
        # Ingresar el código y confirmar
        code_field = routes_page.wait.until(EC.presence_of_element_located(routes_page.enter_code))
        code_field.send_keys(confirmation_code)
        confirm_button = routes_page.wait.until(EC.element_to_be_clickable(routes_page.confirm_button))
        confirm_button.click()
        routes_page.add_payment_method()

#Test 5
    def test_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()
        routes_page.click_phone_number()
        routes_page.set_phone_number()
        # Obtener el código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        print(f'Código de confirmación obtenido: {confirmation_code}')
        # Ingresar el código y confirmar
        code_field = routes_page.wait.until(EC.presence_of_element_located(routes_page.enter_code))
        code_field.send_keys(confirmation_code)
        confirm_button = routes_page.wait.until(EC.element_to_be_clickable(routes_page.confirm_button))
        confirm_button.click()
        routes_page.add_payment_method()
        routes_page.add_driver_message()

#Test 6
    def test_blanket_tishue(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()
        routes_page.click_phone_number()
        routes_page.set_phone_number()
        # Obtener el código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        print(f'Código de confirmación obtenido: {confirmation_code}')
        # Ingresar el código y confirmar
        code_field = routes_page.wait.until(EC.presence_of_element_located(routes_page.enter_code))
        code_field.send_keys(confirmation_code)
        confirm_button = routes_page.wait.until(EC.element_to_be_clickable(routes_page.confirm_button))
        confirm_button.click()
        routes_page.add_payment_method()
        routes_page.add_driver_message()
        routes_page.add_blanket_tishue()

#Test 7
    def test_icecreams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()
        routes_page.click_phone_number()
        routes_page.set_phone_number()
        # Obtener el código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        print(f'Código de confirmación obtenido: {confirmation_code}')
        # Ingresar el código y confirmar
        code_field = routes_page.wait.until(EC.presence_of_element_located(routes_page.enter_code))
        code_field.send_keys(confirmation_code)
        confirm_button = routes_page.wait.until(EC.element_to_be_clickable(routes_page.confirm_button))
        confirm_button.click()
        routes_page.add_payment_method()
        routes_page.add_driver_message()
        routes_page.add_blanket_tishue()
        routes_page.add_icecreams()

#Test 8
    def test_request_vehicle(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_request_taxi()
        routes_page.click_comfort_type()
        routes_page.click_phone_number()
        routes_page.set_phone_number()
        # Obtener el código de confirmación
        confirmation_code = retrieve_phone_code(self.driver)
        print(f'Código de confirmación obtenido: {confirmation_code}')
        # Ingresar el código y confirmar
        code_field = routes_page.wait.until(EC.presence_of_element_located(routes_page.enter_code))
        code_field.send_keys(confirmation_code)
        confirm_button = routes_page.wait.until(EC.element_to_be_clickable(routes_page.confirm_button))
        confirm_button.click()
        routes_page.add_payment_method()
        routes_page.add_driver_message()
        routes_page.add_blanket_tishue()
        routes_page.add_icecreams()
        routes_page.click_request_vehicle()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()