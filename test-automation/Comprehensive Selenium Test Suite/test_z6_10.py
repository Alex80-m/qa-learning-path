import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

#6. Тест кастомного выпадающего меню (hover)
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Кастомное выпадающее меню")
class TestCustomDropdown:
    @allure.title("Проверка hover-поведения кастомного dropdown")
    @allure.description("Тестирование что при наведении появляется dropdown-контент")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("dropdown", "hover", "actionchains")
    def test_dropdown_hover_behavior(self, driver):
        """Проверка что при наведении появляется dropdown-content"""
        with allure.step("Поиск элементов dropdown меню и контента"):
            dropdown_menu = driver.find_element(By.ID, "custom-dropdown")
            dropdown_content = driver.find_element(By.ID, "dropdown-list")
        with allure.step("Проверка начального состояния (display: none)"):
            initial_display = dropdown_content.value_of_css_property("display")
            assert initial_display == "none"

        """- Используйте `ActionChains` для `move_to_element()`"""
        with allure.step("Наведение курсора на dropdown меню с помощью ActionChains"):
            actions = ActionChains(driver)
            actions.move_to_element(dropdown_menu).perform()

        """- После наведения проверьте, что `display` у `.dropdown-content` не `"none"`"""
        with allure.step("Проверка что dropdown-контент появился после наведения"):
            display_after_hover = dropdown_content.value_of_css_property("display")
            assert display_after_hover != "none"

#7. Валидация формы
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Валидация формы")
class TestFormValidation:
    @allure.title("Проверка отправки формы без ошибок валидации")
    @allure.description("Тестирование заполнения и отправки формы с проверкой отсутствия ошибок")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("forms", "validation", "submission")
    def test_form_submission(self, driver):
        with allure.step("Запоминаем начальный URL"):
            initial_url = driver.current_url
        """- Находит форму с `id="sample-form"`"""
        with allure.step("Поиск формы с id='sample-form'"):
            form = driver.find_element(By.ID, "sample-form")

        """- Заполняет обязательные поля (`fullname`, `email`)"""
        with allure.step("Заполнение обязательных полей fullname и email"):
            name_input = driver.find_element(By.ID, "fullname")
            email_input = driver.find_element(By.ID, "email")
        with allure.step("Очищаем данные в поле fullname и email"):
            name_input.clear()
            email_input.clear()
        with allure.step("Вводим данные в поле fullname и email"):
            name_input.send_keys("Иван Иванов")
            email_input.send_keys("ivanov@yandex.ru")

        """- Отправляет форму (клик по `#form-submit-btn`)"""
        with allure.step("Отправка формы кликом по кнопке"):
            submit_button = driver.find_element(By.ID, "form-submit-btn")
            submit_button.click()

        """- Убеждается, что браузер не показывает ошибку валидации """
        with allure.step("Проверка что браузер не показывает ошибку валидации"):
            current_url = driver.current_url
            assert current_url == initial_url, "URL не должен изменяться"
            assert "testsite.html" in current_url, "Должна остаться на той же странице"

#8. Проверка изображения и медиа
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Медиа элементы")
class TestMediaElements:
    @allure.title("Проверка наличия и атрибутов изображения")
    @allure.description("Тестирование что изображение существует и имеет alt-атрибут")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("media", "image", "accessibility")
    def test_image_presence(self, driver):
        """- Наличие `<img>` с `id="sample-img"`"""
        with allure.step("Поиск изображения с id='sample-img'"):
            image = driver.find_element(By.ID, "sample-img")
            assert image.is_displayed(), "Изображение sample-img не найдено"

        """- Что у изображения задан `alt`"""
        with allure.step("Проверка alt-атрибута изображения"):
            alt_text = image.get_attribute("alt")
            assert alt_text is not None and alt_text != "", "У изображения должен быть задан alt-атрибут"

    @allure.title("Проверка видео и аудио элементов")
    @allure.description("Тестирование наличия медиа элементов и их атрибутов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("media", "video", "audio")
    def test_media_elements(self, driver):
        """- Наличие `<video>` и `<audio>` с `controls`"""
        with allure.step("Проверка video элемента"):
            video = driver.find_element(By.ID, "sample-video")
            assert video.is_displayed()
            assert video.get_attribute("controls") is not None, "Видео должно иметь controls"

        with allure.step("Проверка audio элемента"):
            audio = driver.find_element(By.ID, "sample-audio")
            assert audio.is_displayed()
            assert audio.get_attribute("controls") is not None, "Аудио должно иметь controls"

        """- Что у `<video>` есть дочерний `<source>`"""
        with allure.step("Проверка source элемента у video"):
            video_source = driver.find_element(By.ID, "video-source")
            assert video_source is not None, "Видео должно содержать source элемент"

#9. Проверка семантических элементов
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Семантические элементы")
class TestSemanticElements:
    @allure.title("Проверка наличия семантических элементов")
    @allure.description("Тестирование что все основные семантические элементы присутствуют на странице")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("semantic", "html5", "structure")
    def test_semantic_elements_presence(self, driver):
        """Убедитесь, что присутствуют: `<header id="page-header">`"""
        with allure.step("Проверка header элемента"):
            header = driver.find_element(By.ID, "page-header")
            assert header.is_displayed()
            assert header.tag_name == "header", "Должен быть header"

        """Проверяем - `<nav id="main-nav">`"""
        with allure.step("Проверка nav элемента"):
            nav = driver.find_element(By.ID, "main-nav")
            assert nav.is_displayed()
            assert nav.tag_name == "nav", "Должен быть nav"

        """Проверяем - `<main>` (или хотя бы контент между header/footer)"""
        with allure.step("Проверка наличия контентных секций"):
            content_sections = driver.find_elements(By.CSS_SELECTOR, "section")
            assert content_sections is not None, "Должен быть контент"

        """Проверяем - `<footer id="page-footer">`"""
        with allure.step("Проверка footer элемента"):
            footer = driver.find_element(By.ID, "page-footer")
            assert footer.is_displayed()
            assert footer.tag_name == "footer", "Должен быть footer"


# 10. Проверка таблицы
@allure.epic("Автотесты HTML-элементов")
@allure.feature("HTML таблицы")
class TestTable:
    @allure.title("Проверка структуры HTML таблицы")
    @allure.description("Тестирование наличия и корректности всех элементов таблицы")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("table", "structure", "data")
    def test_table_structure(self, driver):
        """- Наличие таблицы с `id="data-table"`"""
        with allure.step("Проверка наличия таблицы с id='data-table'"):
            table = driver.find_element(By.ID, "data-table")
            assert table.is_displayed(), "Таблица data-table не найдена"
            assert table.tag_name == "table", "Элемент должен быть таблицей"

        """- Наличие `<caption>`"""
        with allure.step("Проверка наличия caption у таблицы"):
            caption = driver.find_element(By.ID, "table-caption")
            assert caption.is_displayed(), "Caption таблицы не найден"
            assert caption.tag_name == "caption", "Должен быть элемент caption"

        """- Что в `<thead>` есть заголовки 'Имя' и 'Возраст'"""
        with allure.step("Проверка заголовков таблицы в thead"):
            header_name = driver.find_element(By.ID, "col-name")
            header_age = driver.find_element(By.ID, "col-age")
            assert header_name.text == "Имя", f"Должен быть 'Имя', а не '{header_name.text}'"
            assert header_age.text == "Возраст", f"Должен быть 'Возраст', а не '{header_age.text}'"

        """- Что в `<tbody>` есть строка с 'Анна' и '28' """
        with allure.step("Проверка данных в tbody"):
            cell_name = driver.find_element(By.ID, "cell-name-1")
            cell_age = driver.find_element(By.ID, "cell-age-1")
            assert cell_name.text == "Анна", f"В ячейке должно быть 'Анна', а не '{cell_name.text}'"
            assert cell_age.text == "28", f"В ячейке должно быть '28', а не '{cell_age.text}'"


