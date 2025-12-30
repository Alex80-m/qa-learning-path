import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import time


class TestAllWaits:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.get('file:///D:/testfile.html')

    def teardown_method(self, method):
        self.driver.quit()

    #Найти элемент #form-title и дождаться, пока он станет видимым.
    def test_test1(self):
        self.driver.get("file:///D:/testfile.html")
        wait = WebDriverWait(self.driver, 10)
        form_title = wait.until(EC.presence_of_element_located((By.ID, "form-title")))
        assert form_title.tag_name == "h4"
        assert form_title.is_displayed()

    #Ввести логин и пароль в поля #username и #password, нажать кнопку #submit-btn, дождаться появления подтверждения.
    def test_test2(self):
        self.driver.get("file:///D:/testfile.html")
        wait = WebDriverWait(self.driver, 10)
        username = wait.until(EC.visibility_of_element_located((By.ID, "username")))
        username.clear()
        username.send_keys("логин")

        password = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        password.clear()
        password.send_keys("пароль")

        self.driver.find_element(By.ID, "submit-btn").click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-template-item]")))

    #Проверить, что при клике по кнопке #upload-btn открывается поле выбора файла #attachments.
    def test_test3(self):
        self.driver.get("file:///D:/testfile.html")
        wait = WebDriverWait(self.driver, 10)
        upload_btn = self.driver.find_element(By.ID, "upload-btn")
        upload_btn.click()

        attachments_field = self.driver.find_element(By.ID, "attachments")
        assert attachments_field.is_displayed()
        assert attachments_field.is_enabled()
        time.sleep(1)

    #Выбрать значение «Тёмная» в группе радио-кнопок name="theme" и убедиться, что оно активно.
    def test_test4(self):
        self.driver.get("file:///D:/testfile.html")
        wait = WebDriverWait(self.driver, 10)
        dark_radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='theme'][value='dark']")))
        dark_radio.click()
        wait.until(EC.element_to_be_selected(dark_radio))
        assert dark_radio.is_selected()
        assert dark_radio.is_enabled()

    #В выпадающем списке #country выбрать пункт «Бразилия» и дождаться обновления значения value.
    def test_test5(self):
        self.driver.get("file:///D:/testfile.html")
        wait = WebDriverWait(self.driver, 10)
        country = wait.until(EC.element_to_be_clickable((By.ID, "country")))
        country.click()
        brazil = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//select[@id='country']/optgroup[@label='Америка']/option[text()='Бразилия']")))
        brazil.click()
        wait.until(EC.text_to_be_present_in_element_value((By.ID, "country"), "br"))
        assert country.get_attribute("value") == "br"

    #Ввести несколько адресов в поле #emails и убедиться, что атрибут multiple работает (значения через запятую).
    def test_test6(self):
        self.driver.get("file:///D:/testfile.html")
        wait = WebDriverWait(self.driver, 10)
        emails_field = self.driver.find_element(By.ID, "emails")
        assert emails_field.get_attribute("multiple") == "true"

        emails_field.send_keys("one@mail.com,two@mail.com")
        value = emails_field.get_attribute("value")
        assert "one@mail.com" in value and "two@mail.com" in value

    #Изменить ползунок #volume и дождаться, пока значение обновится в #calc-result.
    def test_test7(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.execute_script(
            "document.getElementById('volume').value = '90'; document.getElementById('volume').dispatchEvent(new Event('input'));")
        wait.until(EC.text_to_be_present_in_element((By.ID, "calc-result"), "90"))

    #Проверить, что поле #csrf_token скрыто (type="hidden") и содержит значение длиной 9 символов.
    def test_test8(self):
        wait = WebDriverWait(self.driver, 10)
        csrf_token = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='csrf_token']")))
        assert csrf_token.get_attribute("type") == "hidden"
        csrf_value = csrf_token.get_attribute("value")
        assert csrf_value is not None
        assert len(csrf_value) == 9, f"Длина значения {len(csrf_value)} вместо 9"

    #Ввести текст в #bio, затем очистить его и убедиться, что значение стало пустым.
    def test_test9(self):
        wait = WebDriverWait(self.driver, 10)
        bio_field = wait.until(EC.element_to_be_clickable((By.ID, "bio")))
        test_text = "Текст для поля bio"
        bio_field.send_keys(test_text)
        assert bio_field.get_attribute("value") == test_text
        bio_field.clear()
        assert bio_field.get_attribute("value") == "", "Поле не очистилось"

    #Дождаться появления SVG-логотипа #logo и проверить наличие тега <linearGradient>.
    def test_test10(self):
        wait = WebDriverWait(self.driver, 10)
        svg_logo = wait.until(EC.presence_of_element_located((By.ID, "logo")))
        assert svg_logo.tag_name == "svg"
        linear_gradient = svg_logo.find_element(By.CSS_SELECTOR, "linearGradient")
        assert linear_gradient.get_attribute("id") == "g"

    #Проверить, что элемент <meter id="cpu"> имеет значение выше 0.5.
    def test_test11(self):
        wait = WebDriverWait(self.driver, 10)
        label_cpu = wait.until(EC.presence_of_element_located((By.ID, "cpu")))
        value = float(label_cpu.get_attribute("value"))
        assert value > 0.5

    #Нажать кнопку #reset-btn, дождаться, что значение #age вернулось к 30.
    def test_test12(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.find_element(By.ID, "age").send_keys("99")
        self.driver.find_element(By.ID, "reset-btn").click()
        wait.until(EC.text_to_be_present_in_element_value((By.ID, "age"), "30"))

    #Проверить, что атрибут aria-required="true" присутствует у поля #username.
    def test_test13(self):
        wait = WebDriverWait(self.driver, 10)
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        assert username.get_attribute("aria-required") == "true"

    #Кликнуть по <details id="faq-1">, дождаться, что атрибут open меняет состояние.
    def test_test14(self):
        wait = WebDriverWait(self.driver, 10)
        self.driver.find_element(By.ID, "faq1-sum").click()
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "#faq-1[open]")))
        faq_element = self.driver.find_element(By.ID, "faq-1")
        assert faq_element.get_attribute("open") is None

    #Найти цитату <blockquote> и дождаться, пока атрибут cite содержит ссылку.
    def test_test15(self):
        wait = WebDriverWait(self.driver, 10)
        blockquote = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "blockquote[cite]")))
        cite_url = blockquote.get_attribute("cite")
        assert "example.com" in cite_url

    #Проверить, что внутри таблицы #data-table количество строк tbody > tr равно 2.
    def test_test16(self):
        wait = WebDriverWait(self.driver, 10)
        table = wait.until(EC.presence_of_element_located((By.ID, "data-table")))
        rows = table.find_elements(By.CSS_SELECTOR, "tbody > tr")
        assert len(rows) == 2

    #Кликнуть по первой области <area> внутри карты #map1 и дождаться загрузки новой страницы или события.
    def test_test17(self):
        wait = WebDriverWait(self.driver, 10)
        first_area = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "area[alt='Левая зона']")))
        original_url = self.driver.current_url
        first_area.click()
        wait.until(EC.url_changes(original_url))

    #Дождаться появления элемента [data-editable="true"] и ввести в него текст через send_keys.
    def test_test18(self):
        wait = WebDriverWait(self.driver, 10)
        editable = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-editable='true']")))
        editable.clear()
        test_text = "Тест-проверка ввода текста через send_keys"
        editable.send_keys(test_text)
        assert test_text in editable.text
        time.sleep(3)

    #Проверить, что тег <time> имеет значение даты, содержащее «2025».
    def test_test19(self):
        wait = WebDriverWait(self.driver, 10)
        time = wait.until(EC.presence_of_element_located((By.TAG_NAME, "time")))
        datetime = time.get_attribute("datetime")
        assert "2025" in datetime

    #Переключиться во iframe#frame1, дождаться появления текста и вернуться обратно.
    def test_test20(self):
        #В данном примере проверяем просто текст в iframe#frame1
        wait = WebDriverWait(self.driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.ID, "frame1")))
        srcdoc = iframe.get_attribute("srcdoc")
        assert srcdoc is not None
        assert "Встроенный документ" in srcdoc

        #Для того чтобы Переключиться во iframe#frame1, нужно использовать: switch_to.frame()
    def test_switch_to_iframe(self):
        wait = WebDriverWait(self.driver, 10)
        iframe_element = self.driver.find_element(By.ID, "frame1")
        self.driver.switch_to.frame(iframe_element)
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Встроенный документ"))
        self.driver.switch_to.default_content()

    #Проверить, что footer[data-section="footer"] присутствует на странице и содержит слово «max-elements».
    def test_test21(self):
        wait = WebDriverWait(self.driver, 10)
        footer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "footer[data-section='footer']")))
        assert footer.is_displayed()
        footer_text = footer.text
        assert "max-elements" in footer_text.lower()

    #Найти элемент <canvas id="myCanvas">, выполнить JS-проверку отрисовки и убедиться, что ширина 300 пикселей.
    def test_test22(self):
        wait = WebDriverWait(self.driver, 10)
        canvas = wait.until(EC.presence_of_element_located((By.ID, "myCanvas")))
        canvas_width = canvas.get_attribute("width")
        assert canvas_width == "300"

    #Проверить, что элемент <dialog> имеет атрибут open при загрузке и исчезает после клика по #closeDlg.
    def test_test23(self):
        wait = WebDriverWait(self.driver, 10)
        dialog = wait.until(EC.presence_of_element_located((By.ID, "infoDialog")))
        assert dialog.get_attribute("open") == "true"
        wait.until(EC.element_to_be_clickable((By.ID, "closeDlg"))).click()
        wait.until(EC.invisibility_of_element_located((By.ID, "closeDlg")))
        assert dialog.get_attribute("open") is None

    #Использовать ожидание, чтобы убедиться, что <output id="calc-result"> изменяется при вводе новых значений.
    def test_test24(self):
        wait = WebDriverWait(self.driver, 10)
        output = self.driver.find_element(By.ID, "calc-result")
        age = self.driver.find_element(By.ID, "age")
        original_text = output.text
        age.clear()
        age.send_keys("32")
        wait.until(EC.text_to_be_present_in_element((By.ID, "calc-result"), "32"))
        new_text = output.text
        print(f"Новый текст: '{new_text}'")
        assert new_text != original_text

    #Проверить, что <progress> и <meter> имеют корректные диапазоны 0–100 и 0–1.
    def test_test25(self):
        wait = WebDriverWait(self.driver, 10)
        progress = wait.until(EC.presence_of_element_located((By.ID, "progress")))
        meter = wait.until(EC.presence_of_element_located((By.ID, "cpu")))
        assert progress.get_attribute("max") == "100"
        assert meter.get_attribute("min") == "0"
        assert meter.get_attribute("max") == "1"
        assert 0 <= float(progress.get_attribute("value")) <= 100
        assert 0 <= float(meter.get_attribute("value")) <= 1