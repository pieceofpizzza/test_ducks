from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import allure
from allure_commons.types import AttachmentType


class Helper:
    def __init__(self):
        self.wd = webdriver.Chrome()
        self.wd.maximize_window()
        self.wd.implicitly_wait(10)

    def open_start_page(self):
        self.wd.get('https://litecart.stqa.ru/en/')  # открываем сайт

    def add_to_cart(self, quantity):
        self.wd.find_element(By.CSS_SELECTOR,
                             '#box-most-popular .campaign-price').click()  # выбираем уточку по скидке
        self.wd.find_element(By.CSS_SELECTOR,
                             '#box-product .options [name="options[Size]"]').click()  # нажимаем выбор размера
        self.wd.find_element(By.CSS_SELECTOR,
                             '#box-product .options [value="Large"]').click()  # выбираем большой размер
        qty_input = self.wd.find_element(By.CSS_SELECTOR, '#box-product .quantity input[name="quantity"]')
        qty_input.clear()
        qty_input.send_keys(str(quantity))  # выбираем кол-во
        self.wd.find_element(By.CSS_SELECTOR,
                             '#box-product .content .buy_now [value="Add To Cart"]').click()  # добавляем в корзину

    def remove_from_cart(self):
        self.wd.find_element(By.CSS_SELECTOR,
                             '#header-wrapper #cart a.image img[src*=cart_filled]').click()  # переходим в корзину
        self.wd.find_element(By.CSS_SELECTOR,
                             '#box-checkout-cart form[name="cart_form"] button[value="Remove"]').click()  # удаляем

    def back_start_page(self):
        self.wd.find_element(By.CSS_SELECTOR,
                             '#checkout-cart-wrapper > p > a[href="https://litecart.stqa.ru/en/"]').click()

    def quit(self):
        self.wd.quit()  # закрываем браузер

    def is_duck_in_cart(self, quantity):
        try:
            WebDriverWait(self.wd, 10).until(
                ec.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, '#header-wrapper #cart > a.content > span.quantity'),
                    str(quantity)
                )
            )
            actual_text = self.wd.find_element(
                By.CSS_SELECTOR, '#header-wrapper #cart > a.content > span.quantity'
            ).text
            print(f'[DEBUG] Ожидаем: {quantity}, В корзине: {actual_text}')
            return int(actual_text) == quantity
        except TimeoutException:
            print(f'[DEBUG] Timeout: не удалось дождаться количества {quantity}')
            return False

    def is_not_duck_in_cart(self):
        return self.is_element_present('#checkout-cart-wrapper > p > a[href="https://litecart.stqa.ru/en/"]')

    def is_element_present(self, locator):
        try:
            self.wd.find_element(By.CSS_SELECTOR, locator)
            return True
        except NoSuchElementException:
            return False

    def is_not_element_present(self, locator):
        self.wd.implicitly_wait(0)
        try:
            self.wd.find_element(By.CSS_SELECTOR, locator)
            return False
        except NoSuchElementException:
            return True
        finally:
            self.wd.implicitly_wait(10)

    def screen_shot(self, name):
        wait = WebDriverWait(self.wd, 5)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        allure.attach(self.wd.get_screenshot_as_png(), name=name, attachment_type=AttachmentType.PNG)
