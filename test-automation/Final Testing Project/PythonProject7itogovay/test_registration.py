import pytest
import os
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

def test_register_user_success_then_duplicate(driver):
    """1.1: Открыть страницу регистрации (#register)"""
    driver.get(HTML_FILE_PATH + "#register")

    """1.2 Ввести корректный e-mail и пароль, нажать кнопку "Зарегистрироваться"."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )

    email = "test_user@example.com"
    password = "secure123"

    driver.find_element(By.ID, "regEmail").send_keys(email)
    driver.find_element(By.ID, "regPassword").send_keys(password)
    driver.find_element(By.ID, "registerForm").submit()

    message = driver.find_element(By.ID, "regMessage").text
    assert message == "Регистрация успешна"

    """1.3: Попробовать зарегистрировать того же пользователя повторно."""
    driver.find_element(By.ID, "regEmail").clear()
    driver.find_element(By.ID, "regPassword").clear()

    driver.find_element(By.ID, "regEmail").send_keys(email)
    driver.find_element(By.ID, "regPassword").send_keys(password)
    driver.find_element(By.ID, "registerForm").submit()

    message = driver.find_element(By.ID, "regMessage").text
    assert message == "Пользователь уже существует"

def test_register_invalid_email_not_submitted(driver):
    """1.4: Ввести некорректный e-mail (например, user@@example.com)."""
    driver.get(HTML_FILE_PATH)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )

    driver.find_element(By.ID, "regEmail").send_keys("user@@example.com")
    driver.find_element(By.ID, "regPassword").send_keys("pass123")
    driver.find_element(By.ID, "registerForm").submit()

    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "regMessage"))
        )
        assert False, "Форма не должна была отправиться!"
    except:
        pass


def test_register_empty_fields_not_submitted(driver):
    """1.5: Пустые поля — форма не отправляется"""
    driver.get(HTML_FILE_PATH)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )

    driver.find_element(By.ID, "registerForm").submit()

    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "regMessage"))
        )
        assert False, "Форма не должна была отправиться при пустых полях!"
    except:
        pass