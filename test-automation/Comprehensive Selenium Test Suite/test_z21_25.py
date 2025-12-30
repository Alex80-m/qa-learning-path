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

#21. Тест time и abbr
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Семантические элементы")
class TestTimeAndAbbr:
    @allure.title("Проверка атрибута datetime у элемента time")
    @allure.description("Тестирование что элемент time имеет корректный datetime атрибут")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("semantic", "time", "datetime")
    def test_time_element(self, driver):
        """- У <time id='time-element'> есть datetime='2025-11-27'"""
        with allure.step("Поиск элемента time"):
            time_element = driver.find_element(By.ID, "time-element")
        with allure.step("Проверка атрибута datetime"):
            datetime_attr = time_element.get_attribute("datetime")
            assert datetime_attr == "2025-11-27"
            print(f"У <time id='time-element'> есть datetime='2025-11-27")

    @allure.title("Проверка текстового содержимого элемента time")
    @allure.description("Тестирование что элемент time содержит правильный текст")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("semantic", "time", "text")
    def test_time_text(self, driver):
        """- Текст внутри — '27 ноября 2025'"""
        with allure.step("Поиск элемента time"):
            time_element = driver.find_element(By.ID, "time-element")
        with allure.step("Проверка текстового содержимого"):
            time_text = time_element.text
            assert time_text == "27 ноября 2025"
            print(f"Тест прошел успешно: внутри — '27 ноября 2025")

    @allure.title("Проверка атрибута title у элемента abbr")
    @allure.description("Тестирование что элемент abbr имеет корректный title атрибут")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("semantic", "abbr", "title")
    def test_abbr_element(self, driver):
        """- У <abbr id='abbr-html'> есть title='HyperText Markup Language'"""
        with allure.step("Поиск элемента abbr"):
            abbr_element = driver.find_element(By.ID, "abbr-html")
        with allure.step("Проверка атрибута title"):
            title_attr = abbr_element.get_attribute("title")
            assert title_attr == "HyperText Markup Language"
            print(f"У <abbr id='abbr-html'> есть title='HyperText Markup Language'")


#22. Проверка data-* атрибутов
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Data атрибуты")
class TestDataAttributes:
    @allure.title("Проверка data-theme у html элемента")
    @allure.description("Тестирование что html элемент имеет data-theme атрибут")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("data-attributes", "html", "theme")
    def test_html_data_theme(self, driver):
        """- У <html> есть data-theme='light'"""
        with allure.step("Поиск html элемента"):
            html_element = driver.find_element(By.TAG_NAME, "html")
        with allure.step("Проверка data-theme атрибута"):
            data_theme = html_element.get_attribute("data-theme")
            assert data_theme == "light"
            print(f"У <html> есть data-theme='light")

    @allure.title("Проверка data-user у body элемента")
    @allure.description("Тестирование что body элемент имеет data-user атрибут")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("data-attributes", "body", "user")
    def test_body_data_user(self, driver):
        """- У <body> есть data-user='guest'"""
        with allure.step("Поиск body элемента"):
            body_element = driver.find_element(By.ID, "body-main")
        with allure.step("Проверка data-user атрибута"):
            data_user = body_element.get_attribute("data-user")
            assert data_user == "guest"
            print(f"У <body> есть data-user='guest")

    @allure.title("Проверка data-section у секции кнопок")
    @allure.description("Тестирование что секция кнопок имеет data-section атрибут")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("data-attributes", "section", "buttons")
    def test_section_data_section(self, driver):
        """- У <section id='buttons-section'> есть data-section='buttons'"""
        with allure.step("Поиск секции buttons-section"):
            section_element = driver.find_element(By.ID, "buttons-section")
        with allure.step("Проверка data-section атрибута"):
            data_section = section_element.get_attribute("data-section")
            assert data_section == "buttons"
            print(f"У <section id='buttons-section'> есть data-section='buttons'")


# 23. Тест blockquote и cite
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Цитаты")
class TestBlockquote:
    @allure.title("Проверка атрибута cite у blockquote")
    @allure.description("Тестирование что blockquote имеет корректный cite атрибут")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("blockquote", "cite", "semantic")
    def test_blockquote_cite(self, driver):
        """- У <blockquote> есть cite='https://example.com'"""
        with allure.step("Поиск элемента blockquote"):
            blockquote = driver.find_element(By.ID, "quote-block")
        with allure.step("Проверка атрибута cite"):
            cite_attr = blockquote.get_attribute("cite")
            assert cite_attr == "https://example.com/"
            print(f"У <blockquote> есть cite='https://example.com/'")


    @allure.title("Проверка текста внутри blockquote")
    @allure.description("Тестирование что blockquote содержит правильный текст")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("blockquote", "text", "content")
    def test_blockquote_text(self, driver):
        """- Внутри есть <p> с текстом 'Это цитата.'"""
        with allure.step("Поиск текста цитаты"):
            quote_text = driver.find_element(By.ID, "quote-text")
        with allure.step("Проверка текстового содержимого"):
            assert quote_text.text == "Это цитата."
            print(f"Внутри есть <p> с текстом 'Это цитата.")

# 24. Проверка кода в pre и code
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Элементы кода")
class TestCodeElements:
    @allure.title("Проверка блока кода в pre элементе")
    @allure.description("Тестирование что pre элемент содержит код функции")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("code", "pre", "syntax")
    def test_pre_code_block(self, driver):
        """- Внутри <pre id='code-block'> есть текст с function hello()"""
        with allure.step("Поиск элемента pre с кодом"):
            code_block = driver.find_element(By.ID, "code-block")
        with allure.step("Проверка содержимого кода"):
            code_text = code_block.text
            assert "function hello()" in code_text
            print(f"Внутри <pre id='code-block'> есть текст с function hello()")

    @allure.title("Проверка inline кода")
    @allure.description("Тестирование что inline code элемент содержит правильный текст")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("code", "inline", "text")
    def test_inline_code(self, driver):
        """- Элемент <code id='inline-code'> содержит текст 'код'"""
        with allure.step("Поиск inline code элемента"):
            inline_code = driver.find_element(By.ID, "inline-code")
        with allure.step("Проверка текстового содержимого"):
            assert inline_code.text == "код"
            print(f" Элемент <code id='inline-code'> содержит текст 'код'")

# 25. Тест на отсутствие "мертвых" атрибутов
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Accessibility проверки")
class TestNoDeadAttributes:
    @allure.title("Проверка отсутствия мертвых атрибутов")
    @allure.description("Тестирование что все referenced ID существуют на странице")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("accessibility", "validation", "dead-attributes")
    def test_all_referenced_ids_exist(self, driver):
        """Проверьте, что все id, указанные в for, aria-labelledby, aria-describedby, действительно существуют на странице"""
        # Собираем все существующие id на странице
        with allure.step("Сбор всех существующих ID на странице"):
            all_elements_with_id = driver.find_elements(By.XPATH, "//*[@id]")
            existing_ids = {element.get_attribute("id") for element in all_elements_with_id}

        # Проверяем атрибуты for
        with allure.step("Проверка атрибутов for у label элементов"):
            labels_with_for = driver.find_elements(By.XPATH, "//label[@for]")
            for label in labels_with_for:
                for_attr = label.get_attribute("for")
                assert for_attr in existing_ids, f"label for='{for_attr}' ссылается на несуществующий id"

        # Проверяем aria-labelledby
        with allure.step("Проверка aria-labelledby атрибутов"):
            elements_with_labelledby = driver.find_elements(By.XPATH, "//*[@aria-labelledby]")
            for element in elements_with_labelledby:
                labelledby_attr = element.get_attribute("aria-labelledby")
                for ref_id in labelledby_attr.split():
                    assert ref_id in existing_ids, f"aria-labelledby='{labelledby_attr}' ссылается на несуществующий id '{ref_id}'"

        # Проверяем aria-describedby
        with allure.step("Проверка aria-describedby атрибутов"):
            elements_with_describedby = driver.find_elements(By.XPATH, "//*[@aria-describedby]")
            for element in elements_with_describedby:
                describedby_attr = element.get_attribute("aria-describedby")
                for ref_id in describedby_attr.split():
                    assert ref_id in existing_ids, f"aria-describedby='{describedby_attr}' ссылается на несуществующий id '{ref_id}'"

            print("Все атрибуты существуют на странице")