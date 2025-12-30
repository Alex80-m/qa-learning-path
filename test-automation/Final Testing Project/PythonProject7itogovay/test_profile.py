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


def test_profile_page(driver):
    """5. Личный кабинет"""
    driver.get(HTML_FILE_PATH)

    #5.1. Открыть страницу личного кабинета (#profile).
    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    profile_info = driver.find_element(By.ID, "profileInfo").text
    assert profile_info == "Пожалуйста, войдите, чтобы увидеть информацию."

    #5.2. Войти под пользователем и открыть кабинет.
    driver.find_element(By.LINK_TEXT, "Регистрация").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "regEmail"))
    )

    email = "user_profile@example.com"
    password = "profile123"

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

    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    profile_info = driver.find_element(By.ID, "profileInfo").text

    assert email in profile_info

    # 5.3. Проверить обновление списка курсов после оформления нового заказа
    driver.find_element(By.LINK_TEXT, "Курсы").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course"))
    )

    driver.find_elements(By.CLASS_NAME, "buyBtn")[1].click()
    driver.find_element(By.ID, "checkoutBtn").click()

    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    profile_info = driver.find_element(By.ID, "profileInfo").text

    assert email in profile_info
    assert "Курс по JavaScript" in profile_info