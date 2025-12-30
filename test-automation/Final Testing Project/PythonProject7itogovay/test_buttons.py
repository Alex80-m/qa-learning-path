import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

HTML_FILE_PATH = "file:///C:/Users/Админ/PycharmProjects/PythonProject7itogovay/academy.html"

def test_ui_buttons_and_forms(driver):
    """6. Проверка работы форм и кнопок"""
    driver.get(HTML_FILE_PATH)

    # 6.1. Проверить, что все кнопки "Купить" активны и кликабельны
    buy_buttons = driver.find_elements(By.CLASS_NAME, "buyBtn")
    assert len(buy_buttons) == 3

    for i, button in enumerate(buy_buttons):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
        button.click()

    driver.get(HTML_FILE_PATH)

    #6.2. Проверить, что кнопка "Оформить заказ" работает корректно при пустой корзине
    checkout_btn = driver.find_element(By.ID, "checkoutBtn")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(checkout_btn))
    checkout_btn.click()

    message = driver.find_element(By.ID, "checkoutMessage").text
    assert message == "Пожалуйста, войдите"

    driver.find_element(By.LINK_TEXT, "Регистрация").click()
    driver.find_element(By.ID, "regEmail").send_keys("test@example.com")
    driver.find_element(By.ID, "regPassword").send_keys("123456")
    driver.find_element(By.ID, "registerForm").submit()

    driver.find_element(By.LINK_TEXT, "Вход").click()
    driver.find_element(By.ID, "loginEmail").send_keys("test@example.com")
    driver.find_element(By.ID, "loginPassword").send_keys("123456")
    driver.find_element(By.ID, "loginForm").submit()

    driver.find_element(By.ID, "checkoutBtn").click()
    assert driver.find_element(By.ID, "checkoutMessage").text == "Заказ оформлен"
    assert driver.find_element(By.ID, "totalPrice").text == "0"

    #6.3. Проверить реакцию на некорректные действия
    # a) Регистрация с пустыми полями
    driver.get(HTML_FILE_PATH)
    driver.find_element(By.ID, "registerForm").submit()

    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "regMessage"))
        )
        assert False, "Форма регистрации не должна была отправиться!"
    except:
        pass

    # b) Вход с пустыми полями
    driver.find_element(By.ID, "loginForm").submit()
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "loginMessage"))
        )
        assert False, "Форма входа не должна была отправиться!"
    except:
        pass