
import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


@pytest.fixture
def page_url():
    file_path = os.path.join(os.path.dirname(__file__), "testfile2.html")
    return "file:///" + file_path.replace("\\", "/")


def test_1_simple_alert(driver, page_url):
    """1. Проверка обычного alert()."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '1. Обычный alert()')]").click()
    alert = driver.switch_to.alert
    assert alert.text == "Привет! Это обычный alert!"
    alert.accept()


def test_2_confirm_accept(driver, page_url):
    """2. Проверка confirm() - OK."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '2. confirm()')]").click()
    alert = driver.switch_to.alert
    alert.accept()

    result_alert = driver.switch_to.alert
    assert result_alert.text == "Вы нажали: OK"
    result_alert.accept()


def test_3_confirm_dismiss(driver, page_url):
    """3. Проверка confirm() - Отмена."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '2. confirm()')]").click()
    alert = driver.switch_to.alert
    alert.dismiss()

    result_alert = driver.switch_to.alert
    assert result_alert.text == "Вы нажали: Отмена"
    result_alert.accept()


def test_4_prompt_with_name(driver, page_url):
    """4. Проверка prompt() с именем."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '3. prompt()')]").click()
    alert = driver.switch_to.alert
    alert.send_keys("Анна")
    alert.accept()

    result_alert = driver.switch_to.alert
    assert "Привет, Анна!" in result_alert.text
    result_alert.accept()


def test_5_prompt_empty(driver, page_url):
    """5. Проверка prompt() без имени."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '3. prompt()')]").click()
    alert = driver.switch_to.alert
    alert.send_keys("")
    alert.accept()

    result_alert = driver.switch_to.alert
    assert result_alert.text == "Вы не ввели имя."
    result_alert.accept()


def test_6_custom_alert(driver, page_url):
    """6. Проверка кастомного alert."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '4. Кастомный Alert')]").click()
    custom_alert = driver.find_element(By.ID, "customAlert")
    assert custom_alert.is_displayed()

    custom_alert.find_element(By.TAG_NAME, "button").click()
    assert not custom_alert.is_displayed()


def test_7_prompt_cancel(driver, page_url):
    """7. Проверка prompt() - Отмена."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '3. prompt()')]").click()
    alert = driver.switch_to.alert
    alert.dismiss()

    result_alert = driver.switch_to.alert
    assert "Вы не ввели имя." in result_alert.text
    result_alert.accept()


def test_8_custom_alert_close_overlay(driver, page_url):
    """8. Проверка закрытия кастомного alert через оверлей."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '4. Кастомный Alert')]").click()
    custom_alert = driver.find_element(By.ID, "customAlert")
    overlay = driver.find_element(By.ID, "overlay")
    assert custom_alert.is_displayed()
    assert overlay.is_displayed()

    # Используем JavaScript для клика по оверлею, так как кастомный алерт перекрывает его
    driver.execute_script("arguments[0].click();", overlay)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "customAlert"))
    )
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.ID, "overlay"))
    )
    assert not custom_alert.is_displayed()
    assert not overlay.is_displayed()

def test_9_custom_alert_text_content(driver, page_url):
    """9. Проверка текста в кастомном alert."""
    driver.get(page_url)

    driver.find_element(By.XPATH, "//button[contains(text(), '4. Кастомный Alert')]").click()

    custom_alert_text = driver.find_element(By.ID, "customAlertText")
    assert custom_alert_text.text == "✨ Это кастомный alert! ✨"

    driver.find_element(By.CSS_SELECTOR, "#customAlert button").click()
    assert not driver.find_element(By.ID, "customAlert").is_displayed()

def test_10_prompt_default_value(driver, page_url):
    """10. Проверка prompt() со значением по умолчанию."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '3. prompt()')]").click()
    alert = driver.switch_to.alert
    alert_text = alert.text
    assert "Как вас зовут?" in alert_text
    alert.accept()

    result_alert = driver.switch_to.alert
    assert "Привет, Гость!" in result_alert.text
    result_alert.accept()


def test_11_multiple_alerts_sequence(driver, page_url):
    """11. Проверка последовательности вызова разных алертов."""
    driver.get(page_url)
    driver.find_element(By.XPATH, "//button[contains(text(), '1. Обычный alert()')]").click()
    alert1 = driver.switch_to.alert
    assert "Привет! Это обычный alert!" in alert1.text
    alert1.accept()
    driver.find_element(By.XPATH, "//button[contains(text(), '2. confirm()')]").click()
    alert2 = driver.switch_to.alert
    alert2.accept()

    result_alert = driver.switch_to.alert
    assert "Вы нажали: OK" in result_alert.text
    result_alert.accept()

    driver.find_element(By.XPATH, "//button[contains(text(), '4. Кастомный Alert')]").click()
    custom_alert = driver.find_element(By.ID, "customAlert")
    assert custom_alert.is_displayed()
    custom_alert.find_element(By.TAG_NAME, "button").click()
    assert not custom_alert.is_displayed()