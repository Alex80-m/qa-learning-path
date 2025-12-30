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


def test_add_course_to_cart(driver):
    """3. Добавление курса в корзину"""
    driver.get(HTML_FILE_PATH)

    # 3.1. Перейти на страницу курсов (#courses)
    driver.find_element(By.LINK_TEXT, "Курсы").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "course"))
    )

    # 3.2. Нажать кнопку "Купить" для одного курса
    buy_buttons = driver.find_elements(By.CLASS_NAME, "buyBtn")
    buy_buttons[0].click()

    cart_items = driver.find_elements(By.CSS_SELECTOR, "#cartList li")
    assert len(cart_items) == 1
    assert "Курс по Python" in cart_items[0].text
    assert driver.find_element(By.ID, "totalPrice").text == "1000"

    # 3.3. Добавить несколько курсов.
    buy_buttons[1].click()
    buy_buttons[2].click()

    cart_items = driver.find_elements(By.CSS_SELECTOR, "#cartList li")
    assert len(cart_items) == 3
    course_names = [item.text for item in cart_items]
    assert "Курс по Python - 1000 ₽" in course_names
    assert "Курс по JavaScript - 1500 ₽" in course_names
    assert "Курс по HTML/CSS - 2000 ₽" in course_names

    assert driver.find_element(By.ID, "totalPrice").text == "4500"

    # 3.4. Проверить, что при добавлении одного и того же курса дважды, он учитывается дважды в сумме.
    buy_buttons[0].click()

    cart_items = driver.find_elements(By.CSS_SELECTOR, "#cartList li")
    assert len(cart_items) == 4
    assert driver.find_element(By.ID, "totalPrice").text == "5500"

    python_items = [item for item in cart_items if "Курс по Python" in item.text]
    assert len(python_items) == 2