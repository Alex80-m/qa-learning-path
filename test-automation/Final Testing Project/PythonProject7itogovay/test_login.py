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


def test_login_success(driver):
    """2.1: Перейти на страницу входа (#login)."""
    driver.get(HTML_FILE_PATH + "#login")

    """2.2: Ввести корректный e-mail и пароль зарегистрированного пользователя, нажать "Войти"."""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )

    email = "user@example.com"
    password = "pass123"

    driver.find_element(By.ID, "regEmail").send_keys(email)
    driver.find_element(By.ID, "regPassword").send_keys(password)
    driver.find_element(By.ID, "registerForm").submit()
    assert driver.find_element(By.ID, "regMessage").text == "Регистрация успешна"

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginEmail"))
    )

    driver.find_element(By.ID, "loginEmail").clear()
    driver.find_element(By.ID, "loginPassword").clear()
    driver.find_element(By.ID, "loginEmail").send_keys(email)
    driver.find_element(By.ID, "loginPassword").send_keys(password)
    driver.find_element(By.ID, "loginForm").submit()
    assert driver.find_element(By.ID, "loginMessage").text == "Вход выполнен"

    profile_text = driver.find_element(By.ID, "profileInfo").text
    assert email in profile_text


def test_login_wrong_password(driver):
    """2.3: Ввести правильный e-mail и неверный пароль."""
    driver.get(HTML_FILE_PATH)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )
    email = "testuser@example.com"
    correct_password = "right123"
    wrong_password = "wrong123"

    # Регистрируем пользователя
    driver.find_element(By.ID, "regEmail").send_keys(email)
    driver.find_element(By.ID, "regPassword").send_keys(correct_password)
    driver.find_element(By.ID, "registerForm").submit()
    assert driver.find_element(By.ID, "regMessage").text == "Регистрация успешна"

    driver.find_element(By.LINK_TEXT, "Вход").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginEmail"))
    )

    # Вводим правильный email, но НЕВЕРНЫЙ пароль
    driver.find_element(By.ID, "loginEmail").send_keys(email)
    driver.find_element(By.ID, "loginPassword").send_keys(wrong_password)
    driver.find_element(By.ID, "loginForm").submit()

    # Проверяем сообщение
    assert driver.find_element(By.ID, "loginMessage").text == "Неверные данные"


def test_login_unregistered_email(driver):
    """2.4: Ввести незарегистрированный e-mail."""
    driver.get(HTML_FILE_PATH)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginEmail"))
    )

    driver.find_element(By.ID, "loginEmail").send_keys("unknown@example.com")
    driver.find_element(By.ID, "loginPassword").send_keys("any_pass")
    driver.find_element(By.ID, "loginForm").submit()
    assert driver.find_element(By.ID, "loginMessage").text == "Неверные данные"