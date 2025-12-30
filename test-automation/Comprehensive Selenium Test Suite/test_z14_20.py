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


# 14. Тест чекбокса и радиокнопок
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Чекбоксы и радиокнопки")
class TestCheckboxRadio:
    @allure.title("Проверка начального состояния чекбокса")
    @allure.description("Тестирование что чекбокс subscribe изначально отмечен")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("checkbox", "state", "initial")
    def test_checkbox_initial_state(self, driver):
        """- Чекбокс #subscribe изначально отмечен (is_selected() == True)"""
        with allure.step("Поиск чекбокса subscribe"):
            checkbox = driver.find_element(By.ID, "subscribe")
        with allure.step("Проверка что чекбокс отмечен"):
            assert checkbox.is_selected() == True
            print("Чекбокс subscribe изначально отмечен")

    @allure.title("Проверка начального состояния радиокнопок")
    @allure.description("Тестирование что радиокнопка male отмечена, а female - нет")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("radio", "state", "initial")
    def test_radio_buttons_initial_state(self, driver):
        """- Радиокнопка #male отмечена, #female — нет"""
        with allure.step("Поиск радиокнопок male и female"):
            male_radio = driver.find_element(By.ID, "male")
            female_radio = driver.find_element(By.ID, "female")

        with allure.step("Проверка состояний радиокнопок"):
            assert male_radio.is_selected() == True
            assert female_radio.is_selected() == False
            print("Радиокнопка #male отмечена, #female — нет")

    @allure.title("Проверка переключения чекбокса")
    @allure.description("Тестирование возможности снятия и установки чекбокса")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("checkbox", "interaction", "toggle")
    def test_checkbox_toggle(self, driver):
        """- Можно снять/установить чекбокс программно (и проверить состояние)"""
        with allure.step("Поиск чекбокса subscribe"):
            checkbox = driver.find_element(By.ID, "subscribe")
        with allure.step("Снятие чекбокса"):
            checkbox.click()
            assert checkbox.is_selected() == False
            print("Чекбокс снят")

        with allure.step("Установка чекбокса обратно"):
            checkbox.click()
            assert checkbox.is_selected() == True
            print("Чекбокс установлен обратно")

# 15. Проверка валидации формы через JavaScript
@allure.epic("Автотесты HTML-элементов")
@allure.feature("JavaScript валидация формы")
class TestFormJavaScriptValidation:
    @allure.title("Проверка валидации формы с пустыми полями")
    @allure.description("Тестирование что форма невалидна при пустом поле fullname")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("forms", "validation", "javascript")
    def test_form_validation_empty_fields(self, driver):
        """- При пустом fullname — возвращает false"""
        with allure.step("Очистка поля fullname"):
            fullname_input = driver.find_element(By.ID, "fullname")
            fullname_input.clear()
        with allure.step("Проверка валидности формы через JavaScript"):
            is_valid = driver.execute_script("return document.getElementById('sample-form').checkValidity();")
            assert is_valid == False
            print("При пустом fullname - возвращает `false` ")

    @allure.title("Проверка валидации формы с заполненными полями")
    @allure.description("Тестирование что форма валидна при заполненных обязательных полях")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("forms", "validation", "javascript")
    def test_form_validation_valid_fields(self, driver):
        """- При заполнении всех обязательных полей — возвращает true"""
        with allure.step("Очистка и заполнение обязательных полей"):
            fullname_input = driver.find_element(By.ID, "fullname")
            email_input = driver.find_element(By.ID, "email")
            fullname_input.clear()
            email_input.clear()

            fullname_input.send_keys("Иван Иванов")
            email_input.send_keys("test@mail.ru")

        with allure.step("Проверка валидности формы через JavaScript"):
            is_valid = driver.execute_script("return document.getElementById('sample-form').checkValidity();")
            assert is_valid == True
            print("При заполнении всех обязательных полей — возвращает `true`")

# 16. Тест placeholder и value
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Placeholder и значения полей")
class TestPlaceholderAndValue:
    @allure.title("Проверка placeholder у поля fullname")
    @allure.description("Тестирование что у поля fullname есть корректный placeholder")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("forms", "placeholder", "input")
    def test_fullname_placeholder(self, driver):
        """- У #fullname есть placeholder='Введите имя'"""
        with allure.step("Поиск поля fullname"):
            fullname_input = driver.find_element(By.ID, "fullname")
        with allure.step("Проверка placeholder"):
            placeholder = fullname_input.get_attribute("placeholder")
            assert placeholder == "Введите имя"
            print("У fullname есть placeholder='Введите имя'")

    @allure.title("Проверка значения по умолчанию у поля age")
    @allure.description("Тестирование что у поля age установлено значение по умолчанию 18")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("forms", "value", "default")
    def test_age_default_value(self, driver):
        """- У #age есть value='18' (по умолчанию)"""
        with allure.step("Поиск поля age"):
            age_input = driver.find_element(By.ID, "age")
        with allure.step("Проверка значения по умолчанию"):
            value = age_input.get_attribute("value")
            assert value == "18"
            print("У age есть value='18' (по умолчанию)")

    @allure.title("Проверка textarea bio")
    @allure.description("Тестирование что textarea bio имеет пустое значение и placeholder")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("forms", "textarea", "placeholder")
    def test_textarea_placeholder_and_value(self, driver):
        """- У textarea#bio — пустой value, но есть placeholder"""
        with allure.step("Поиск textarea bio"):
            bio_textarea = driver.find_element(By.ID, "bio")
        with allure.step("Проверка значения и placeholder"):
            value = bio_textarea.get_attribute("value")
            placeholder = bio_textarea.get_attribute("placeholder")
            assert value == "" or value is None
            assert placeholder == "Расскажите о себе..."
            print("У textarea#bio — пустой value и есть placeholder")

# 17. Проверка ссылок и навигации
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Навигация по ссылкам")
class TestLinksNavigation:
    @allure.title("Проверка href у навигационных ссылок")
    @allure.description("Тестирование что ссылки в nav ведут на правильные якоря")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("navigation", "links", "anchors")
    def test_nav_links_hrefs(self, driver):
        """- Убедитесь, что ссылки в <nav> ведут на якоря (href='#forms', и т.д.)"""
        with allure.step("Поиск всех ссылок в навигации"):
            nav_links = driver.find_elements(By.CSS_SELECTOR, "#main-nav a")
            expected_anchors = ["#forms", "#buttons", "#media"]

        with allure.step("Проверка href каждой ссылки"):
            for i, link in enumerate(nav_links):
                href = link.get_attribute("href")
                assert href.endswith(
                    expected_anchors[i])
                print(f"Ссылка {i + 1} ведет на {expected_anchors[i]}")

    @allure.title("Проверка изменения hash при навигации")
    @allure.description("Тестирование что клик по ссылке меняет location.hash и прокручивает страницу")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("navigation", "hash", "scroll")
    def test_nav_link_click_changes_hash(self, driver):
        """- После клика по #nav-link-forms — страница прокручивается к секции #forms"""
        with allure.step("Проверка что секция forms существует"):
            forms_section = driver.find_element(By.ID, "forms")
            assert forms_section.is_displayed()

        """- Проверьте, что location.hash меняется"""
        with allure.step("Клик по ссылке forms и проверка hash"):
            forms_link = driver.find_element(By.ID, "nav-link-forms")
            forms_link.click()
            current_hash = driver.execute_script("return window.location.hash;")
            assert current_hash == "#forms"


#18. Тест кастомной кнопки (`<input type="button">`)
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Кастомные кнопки")
class TestCustomButton:
    @allure.title("Проверка наличия кастомной кнопки")
    @allure.description("Тестирование что элемент input-button существует")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("buttons", "custom", "existence")
    def test_input_button_exists(self, driver):
        """- Элемент #input-button существует"""
        with allure.step("Поиск кастомной кнопки"):
            button = driver.find_element(By.ID, "input-button")
            assert button.is_displayed()

    @allure.title("Проверка alert при клике на кнопку")
    @allure.description("Тестирование что клик на кнопку вызывает alert с правильным текстом")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("buttons", "alert", "interaction")
    def test_input_button_click_alert(self, driver):
        """- При клике вызывается alert"""
        """- Сымитируйте клик и перехватите `alert` через `browser.switch_to.alert`"""
        with allure.step("Клик по кастомной кнопке"):
            button = driver.find_element(By.ID, "input-button")
            button.click()

        with allure.step("Перехват и проверка alert"):
            alert = driver.switch_to.alert
            assert alert.text == "Клик!"
            alert.accept()


# 19. Проверка семантической вложенности
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Семантическая вложенность")
class TestSemanticNesting:
    @allure.title("Проверка вложенности article внутри main")
    @allure.description("Тестирование что все article элементы находятся внутри main")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("semantic", "nesting", "article")
    def test_article_inside_main(self, driver):
        """- <article> находится внутри <main>"""
        with allure.step("Поиск всех article элементов"):
            articles = driver.find_elements(By.TAG_NAME, "article")
        with allure.step("Проверка что каждый article внутри main"):
            for article in articles:
                main_parent = article.find_elements(By.XPATH, "./ancestor::main")
                assert len(main_parent) > 0
                print(f"<article> находится внутри <main>")

    @allure.title("Проверка вложенности aside внутри main")
    @allure.description("Тестирование что все aside элементы находятся внутри main")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("semantic", "nesting", "aside")
    def test_aside_inside_main(self, driver):
        """- <aside> тоже внутри <main>"""
        with allure.step("Поиск всех aside элементов"):
            asides = driver.find_elements(By.TAG_NAME, "aside")
        with allure.step("Проверка что каждый aside внутри main"):
            for aside in asides:
                main_parent = aside.find_elements(By.XPATH, "./ancestor::main")
                assert len(main_parent) > 0, "<aside> должен находиться внутри <main>"
                print(f"<aside> находится внутри <main>")

    @allure.title("Проверка верхнеуровневых header и footer")
    @allure.description("Тестирование что header и footer находятся на верхнем уровне")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("semantic", "nesting", "header-footer")
    def test_header_footer_top_level(self, driver):
        """- <header> и <footer> — на верхнем уровне (не внутри <article>)"""
        with allure.step("Поиск header и footer элементов"):
            header = driver.find_element(By.ID, "page-header")
            footer = driver.find_element(By.ID, "page-footer")

        with allure.step("Проверка что header и footer не внутри article"):
            header_article_parent = header.find_elements(By.XPATH, "./ancestor::article")
            footer_article_parent = footer.find_elements(By.XPATH, "./ancestor::article")

            assert len(header_article_parent) == 0
            assert len(footer_article_parent) == 0
            print("<header> и <footer> — на верхнем уровне")

# 20. Проверка атрибута loading="lazy" у изображения
@allure.epic("Автотесты HTML-элементов")
@allure.feature("Lazy loading изображений")
class TestLazyLoading:
    @allure.title("Проверка lazy loading у изображения")
    @allure.description("Тестирование что у изображения установлен атрибут loading='lazy'")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("images", "performance", "lazy-loading")
    def test_image_loading_lazy(self, driver):
        """- Убедитесь, что у <img id='sample-img'> есть атрибут loading со значением 'lazy'"""
        with allure.step("Поиск изображения sample-img"):
            image = driver.find_element(By.ID, "sample-img")
        with allure.step("Проверка атрибута loading"):
            loading_attr = image.get_attribute("loading")
            assert loading_attr == "lazy"
            print(f"У `<img id='sample-img'>` есть атрибут `loading` со значением `'lazy'`")

