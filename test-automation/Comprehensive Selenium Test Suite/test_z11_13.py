import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("file:///D:/testsite.html")
    yield driver
    driver.quit()


# 11. Тест на отсутствие дублирующихся id
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Проверка уникальности ID")
class TestUniqueIds:
    @allure.title("Проверка отсутствия дублирующихся ID на странице")
    @allure.description("Тестирование что все атрибуты ID уникальны и нет дубликатов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("id", "validation", "unique")
    def test_no_duplicate_ids(self, driver):
        """- Собирает все значения атрибута id"""
        with allure.step("Сбор всех элементов с атрибутом id"):
            elements_with_id = driver.find_elements(By.XPATH, "//*[@id]")
            all_ids = [element.get_attribute("id") for element in elements_with_id]

        """- Проверяет, что len(ids) == len(set(ids))"""
        with allure.step("Проверка уникальности ID"):
            unique_ids = set(all_ids)
            assert len(all_ids) == len(unique_ids), (
                f"Найдены дубликаты id: {[id for id in all_ids if all_ids.count(id) > 1]}"
            )
            print(f"Все {len(all_ids)} id уникальны")


# 12. Проверка атрибутов aria-* и role
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Accessibility атрибуты")
class TestAriaAttributes:
    @allure.title("Проверка ARIA атрибутов и ролей")
    @allure.description("Тестирование корректности accessibility атрибутов для доступности")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("accessibility", "aria", "role")
    def test_aria_attributes(self, driver):
        """- У <body> есть aria-label='Основное тело страницы'"""
        with allure.step("Проверка aria-label у body элемента"):
            body = driver.find_element(By.ID, "body-main")
            aria_label_body = body.get_attribute("aria-label")
            assert aria_label_body == "Основное тело страницы"

        """- У <nav> есть aria-label='Основная навигация'"""
        with allure.step("Проверка aria-label у nav элемента"):
            nav = driver.find_element(By.ID, "main-nav")
            aria_label_nav = nav.get_attribute("aria-label")
            assert aria_label_nav == "Основная навигация"

        """- У <button id='dropdown-btn'> есть role='menu' (или у родителя)"""
        with allure.step("Проверка role у dropdown меню"):
            dropdown_menu = driver.find_element(By.ID, "custom-dropdown")
            role_dropdown = dropdown_menu.get_attribute("role")
            assert role_dropdown == "menu"

        """- Нет элементов с role, но без необходимых дочерних aria-* атрибутов"""
        with allure.step("Проверка accessibility атрибутов у контейнера меню"):
            menu_container = driver.find_element(By.ID, "custom-dropdown")
            assert menu_container.get_attribute("role") == "menu", "Контейнер меню должен иметь role='menu'"
            assert menu_container.get_attribute("aria-haspopup") == "true", "Меню должно иметь aria-haspopup='true'"


# 13. Проверка связки label ↔ input
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Связка label-input")
class TestLabelInputAssociation:
    @allure.title("Проверка связки label с form элементами")
    @allure.description("Тестирование что все form элементы имеют связанные label")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("accessibility", "forms", "labels")
    def test_label_input_association(self, driver):
        """Для каждого input, select, textarea
        - Найдите соответствующий `<label>`"""
        with allure.step("Сбор всех form элементов (input, select, textarea)"):
            form_elements = driver.find_elements(By.XPATH, "//input | //select | //textarea")

        for element in form_elements:
            element_id = element.get_attribute("id")
            element_type = element.get_attribute("type") or element.tag_name

            with allure.step(f"Проверка элемента {element_type} с id='{element_id}'"):
                if not element_id or element_type in ['button']:
                    continue

                """- Найдите соответствующий <label>"""
                label_by_for = driver.find_elements(By.XPATH, f"//label[@for='{element_id}']")
                label_parent = element.find_elements(By.XPATH, "./ancestor::label")

                """- Убедитесь, что у label есть атрибут for, равный id поля ИЛИ поле находится внутри label"""
                assert len(label_by_for) > 0 or len(label_parent) > 0

    @allure.title("Проверка фокусировки поля при клике на label")
    @allure.description("Тестирование что клик по label переводит фокус на связанное поле")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("accessibility", "interaction", "focus")
    def test_label_click_focus(self, driver):
        """- Проверьте, что клик по `label` фокусирует поле (опционально)"""
        with allure.step("Поиск поля ввода и связанного label"):
            name_input = driver.find_element(By.ID, "fullname")
            name_label = driver.find_element(By.XPATH, "//label[@for='fullname']")
        with allure.step("Клик по label элемента"):
            name_label.click()

        with allure.step("Проверка что поле получило фокус"):
            active_element = driver.switch_to.active_element
            assert name_input == active_element
            print("Клик по label фокусирует поле (опционально)")

