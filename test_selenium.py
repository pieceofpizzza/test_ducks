import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


@pytest.mark.parametrize('quantity', [1, 2, 3])
def test_cart(app, quantity):
    with allure.step('Добавление уточек в корзину'):
        app.add_to_cart(quantity)
        WebDriverWait(app.wd, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#header-wrapper #cart a.image img[src*=cart_filled]')))
        app.screen_shot('Уточки добавлены в корзину')
        assert app.is_duck_in_cart(quantity), f"Ошибка добавления уточек, ожидается {quantity}, на выходе {app.wd.find_element(By.CSS_SELECTOR, '#header-wrapper #cart > a.content > span.quantity').text}"
    with allure.step('Удаление уточек из корзины'):
        app.remove_from_cart()
        WebDriverWait(app.wd, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#checkout-cart-wrapper > p > a[href="https://litecart.stqa.ru/en/"]')))
        app.screen_shot('Уточки удалены из корзины')
        assert app.is_not_duck_in_cart(), "Уточка не была удалена из корзины"
    with allure.step('Возврат на главную страницу'):
        app.back_start_page()
        app.screen_shot('Выполнен возврат на главную страницу')
