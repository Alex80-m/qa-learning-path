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


def test_checkout_order(driver):
    """4. Оформление заказа"""
    driver.get(HTML_FILE_PATH)

    # 4.1. Добавить курс в корзину
    driver.find_element(By.LINK_TEXT, "Курсы").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course"))
    )

    driver.find_elements(By.CLASS_NAME, "buyBtn")[0].click()
    assert driver.find_element(By.ID, "totalPrice").text == "1000"

    # 4.2. Нажать кнопку "Оформить заказ" без входа в систему.
    driver.find_element(By.ID, "checkoutBtn").click()

    assert driver.find_element(By.ID, "checkoutMessage").text == "Пожалуйста, войдите"

    # 4.3.1. Войти под зарегистрированным пользователем и оформить заказ
    driver.find_element(By.LINK_TEXT, "Регистрация").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )

    email = "buyer@example.com"
    password = "buyer123"

    driver.find_element(By.ID, "regEmail").send_keys(email)
    driver.find_element(By.ID, "regPassword").send_keys(password)
    driver.find_element(By.ID, "registerForm").submit()
    assert driver.find_element(By.ID, "regMessage").text == "Регистрация успешна"

    driver.find_element(By.LINK_TEXT, "Вход").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginEmail"))
    )

    driver.find_element(By.ID, "loginEmail").send_keys(email)
    driver.find_element(By.ID, "loginPassword").send_keys(password)
    driver.find_element(By.ID, "loginForm").submit()
    assert driver.find_element(By.ID, "loginMessage").text == "Вход выполнен"

    #4.3.2 Оформляем заказ ПОСЛЕ входа
    driver.find_element(By.ID, "checkoutBtn").click()

    assert driver.find_element(By.ID, "checkoutMessage").text == "Заказ оформлен"

    assert driver.find_element(By.ID, "totalPrice").text == "0"
    cart_items = driver.find_elements(By.CSS_SELECTOR, "#cartList li")
    assert len(cart_items) == 0

    profile_info = driver.find_element(By.ID, "profileInfo").text
    assert "Курс по Python" in profile_info