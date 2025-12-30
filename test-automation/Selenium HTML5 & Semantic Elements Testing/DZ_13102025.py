import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC


class TestLocators():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    #Проверить наличие таблицы и видимость заголовков (<th>).
    def test_test1(self):
        self.driver.get("file:///D:/testfile.html")
        table = self.driver.find_element(By.ID, "data-table")
        assert table.is_displayed()

        headers = self.driver.find_elements(By.TAG_NAME, "th")
        assert len(headers) == 3
        assert headers[0].text == "Имя"
        assert headers[1].text == "Роль"
        assert headers[2].text == "Активен"

    #Проверить количество строк в <tbody> и корректность данных в ячейках.
    def test_test2(self):
        self.driver.get("file:///D:/testfile.html")
        rows = self.driver.find_elements(By.CSS_SELECTOR, "tbody tr")
        assert len(rows) == 2, "Найдено: {len(rows)}"

        td_row1 = rows[0].find_elements(By.TAG_NAME, "td")
        assert len(td_row1) == 3
        assert td_row1[0].text == "Алексей"
        assert td_row1[1].text == "Админ"
        assert td_row1[2].text == "Да"

        td_row2 = rows[1].find_elements(By.TAG_NAME, "td")
        assert len(td_row2) == 3
        assert td_row2[0].text == "Мария"
        assert td_row2[1].text == "Редактор"
        assert td_row2[2].text == "Нет"

    #Проверить наличие <tfoot> и правильный текст в нём.
    def test_test3(self):
        self.driver.get("file:///D:/testfile.html")
        tfoot = self.driver.find_element(By.TAG_NAME, "tfoot")
        assert tfoot.is_displayed()
        assert tfoot.text == "Количество записей: 2"

    #Проверить наличие и видимость видео и аудио-плееров.
    def test_test4(self):
        self.driver.get("file:///D:/testfile.html")
        video = self.driver.find_element(By.TAG_NAME, "video")
        audio = self.driver.find_element(By.TAG_NAME, "audio")
        assert video.is_displayed()
        assert audio.is_displayed()

    #Проверить, что <video> и <audio> имеют атрибуты controls и aria-label.
    def test_test5(self):
        self.driver.get("file:///D:/testfile.html")
        video = self.driver.find_element(By.TAG_NAME, "video")
        audio = self.driver.find_element(By.TAG_NAME, "audio")

        assert video.get_attribute("controls") is not None
        assert audio.get_attribute("controls") is not None

        assert video.get_attribute("aria-label") == "Демо видео"
        assert audio.get_attribute("aria-label") == "Демо аудио"

    #Проверить, что <picture> содержит корректный <source> и <img>.
    def test_test6(self):
        self.driver.get("file:///D:/testfile.html")
        picture = self.driver.find_element(By.TAG_NAME, "picture")
        source = picture.find_element(By.TAG_NAME, "source")
        img = picture.find_element(By.TAG_NAME, "img")
        assert source.get_attribute("media") == "(min-width:600px)"
        assert img.get_attribute("alt") == "Inline image"
        assert img.is_displayed()

    #Проверить наличие <svg> и его элементы (<rect>, <text>, <linearGradient>).
    def test_test7(self):
        self.driver.get("file:///D:/testfile.html")
        svg = self.driver.find_element(By.TAG_NAME, "svg")
        assert svg.is_displayed()

        rect = svg.find_element(By.TAG_NAME, "rect")
        text = svg.find_element(By.TAG_NAME, "text")
        gradient = svg.find_element(By.TAG_NAME, "linearGradient")
        assert rect.is_displayed()
        assert text.text == "SVG Demo"
        assert gradient.get_attribute("id") == "g"

    #Проверить, что <canvas> отображается.
    def test_test8(self):
        self.driver.get("file:///D:/testfile.html")
        canvas = self.driver.find_element(By.TAG_NAME, "canvas")
        assert canvas.is_displayed()

    #Проверить, что у <canvas> есть заданные width и height.
    def test_test9(self):
        self.driver.get("file:///D:/testfile.html")
        canvas = self.driver.find_element(By.TAG_NAME, "canvas")
        assert canvas.get_attribute("width") == "300"
        assert canvas.get_attribute("height") == "120"

    #Проверить наличие открытого <details> и видимость <summary>.
    def test_test10(self):
        self.driver.get("file:///D:/testfile.html")
        details = self.driver.find_element(By.TAG_NAME, "details")
        summary = details.find_element(By.TAG_NAME, "summary")
        assert details.get_attribute("open") is not None
        assert summary.is_displayed()

    #Проверить, что <details> можно открыть и закрыть через JS.
    """Открыт:
    <details id="faq-1" class="card" data-faq="1" aria-labelledby="faq1-sum" open="">
        <summary id="faq1-sum" role="button" aria-expanded="true" tabindex="0">Часто задаваемый вопрос: что это?</summary>
        <p>Это демонстрация тега &lt;details&gt; с атрибутами.</p>
      </details>
      
      Закрыт:
      <details id="faq-1" class="card" data-faq="1" aria-labelledby="faq1-sum">
        <summary id="faq1-sum" role="button" aria-expanded="true" tabindex="0">Часто задаваемый вопрос: что это?</summary>
        <p>Это демонстрация тега &lt;details&gt; с атрибутами.</p>
      </details>"""
    #или с помощью кода
    def test_test11(self):
        self.driver.get("file:///D:/testfile.html")
        details = self.driver.find_element(By.ID, "faq-1")
        self.driver.execute_script("arguments[0].open = false;", details)
        assert details.get_attribute("open") is None
        self.driver.execute_script("arguments[0].open = true;", details)
        assert details.get_attribute("open") is not None

    #Проверить, что <dialog> с атрибутом open виден.
    def test_test12(self):
        self.driver.get("file:///D:/testfile.html")
        dialog = self.driver.find_element(By.TAG_NAME, "dialog")
        assert dialog.get_attribute("open") is not None
        assert dialog.is_displayed()

    #Проверить наличие кнопки закрытия и её функциональность.
    def test_test13(self):
        self.driver.get("file:///D:/testfile.html")
        close_btn = self.driver.find_element(By.ID, "closeDlg")
        assert close_btn.is_displayed()
        close_btn.click()
        assert close_btn.get_attribute("open") is None

    #Проверить наличие <template> и корректное клонирование его контента.
    def test_test14(self):
        self.driver.get("file:///D:/testfile.html")
        template = self.driver.find_element(By.ID, "person-template")
        assert template.tag_name == "template"
        cloned = self.driver.find_element(By.CSS_SELECTOR, "[data-template-item] .name")
        assert cloned.text == "Валентина"

    #Проверить, что динамически добавленные элементы имеют ожидаемые значения.
    def test_test15(self):
        self.driver.get("file:///D:/testfile.html")
        cloned_card = self.driver.find_element(By.CSS_SELECTOR, "[data-template-item]")
        name_span = cloned_card.find_element(By.CLASS_NAME, "name")
        assert cloned_card.is_displayed()
        assert name_span.text == "Валентина"

    #Проверить наличие <iframe> и корректный srcdoc или src.
    def test_test16(self):
        self.driver.get("file:///D:/testfile.html")
        iframe = self.driver.find_element(By.ID, "frame1")
        assert iframe.get_attribute("srcdoc") == "<p>Встроенный документ (iframe srcdoc).</p>"

    #Проверить видимость и доступность содержимого iframe.
    def test_test17(self):
        self.driver.get("file:///D:/testfile.html")
        iframe = self.driver.find_element(By.ID, "frame1")
        assert iframe.is_displayed()
        assert iframe.is_enabled()

    #Проверить наличие <map> и <area> внутри него.
    def test_test18(self):
        self.driver.get("file:///D:/testfile.html")
        map = self.driver.find_element(By.ID, "map1")
        areas = map.find_elements(By.TAG_NAME, "area")
        assert map.is_displayed()
        assert areas is not None

    #Проверить, что coords, href и alt у <area> корректные.
    def test_test19(self):
        self.driver.get("file:///D:/testfile.html")
        areas = self.driver.find_elements(By.TAG_NAME, "area")

        assert areas[0].get_attribute("coords") == "0,0,160,120"
        #assert areas[0].get_attribute("href") == "#" - с таким кодом выдает ошибку:AssertionError
        assert areas[0].get_attribute("href").endswith("#")
        assert areas[0].get_attribute("alt") == "Левая зона"

        assert areas[1].get_attribute("coords") == "160,0,320,120"
        #assert areas[1].get_attribute("href") == "#" - с таким кодом выдает ошибку: AssertionError
        assert areas[1].get_attribute("href").endswith("#")
        assert areas[1].get_attribute("alt") == "Правая зона"

    #Проверить <mark>, <abbr>, <time>, <code>, <kbd> на видимость и правильные значения/атрибуты.
    def test_test20(self):
        self.driver.get("file:///D:/testfile.html")
        mark = self.driver.find_element(By.TAG_NAME, "mark")
        assert mark.is_displayed()
        assert mark.text == "выделением"

        abbr = self.driver.find_element(By.TAG_NAME, "abbr")
        assert abbr.is_displayed()
        assert abbr.text == "HTML"
        assert abbr.get_attribute("title") == "HyperText Markup Language"

        time = self.driver.find_element(By.TAG_NAME, "time")
        assert time.is_displayed()
        assert time.text == "6 октября 2025"
        assert time.get_attribute("datetime") == "2025-10-06"

        code = self.driver.find_element(By.CSS_SELECTOR, "code[class='mono']")
        assert code.is_displayed()
        assert code.text == "console.log()"

        kbd = self.driver.find_elements(By.TAG_NAME, "kbd")
        assert len(kbd) == 2
        assert kbd[0].text == "Ctrl"
        assert kbd[1].text == "C"
        assert kbd[0].is_displayed()
        assert kbd[1].is_displayed()

    #Проверить <dl> и <blockquote> на корректную структуру и текст.
    def test_test21(self):
        self.driver.get("file:///D:/testfile.html")
        dl = self.driver.find_element(By.TAG_NAME, "dl")
        dts = dl.find_elements(By.TAG_NAME, "dt")
        dds = dl.find_elements(By.TAG_NAME, "dd")

        assert len(dts) == 2
        assert len(dds) == 2
        assert dts[0].text == "HTML"
        assert dds[0].text == "Язык разметки."
        assert dts[1].text == "CSS"
        assert dds[1].text == "Стилизация документа."

        blockquote = self.driver.find_element(By.TAG_NAME, "blockquote")
        assert blockquote.is_displayed()
        assert blockquote.text == "«Это цитата для демонстрации тега blockquote»"

    #Проверить contenteditable и доступность ввода текста.
    def test_test22(self):
        self.driver.get("file:///D:/testfile.html")
        editable = self.driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        assert editable.is_displayed()
        editable.clear()
        editable.send_keys("Проверить доступность ввода текста")
        assert editable.text == "Проверить доступность ввода текста"

    #Проверить наличие aria-атрибутов и tabindex.
    def test_test23(self):
        self.driver.get("file:///D:/testfile.html")
        header = self.driver.find_element(By.ID, "main-header")
        title = self.driver.find_element(By.ID, "site-title")
        assert header.get_attribute("aria-label") == "Шапка демо"
        assert title.get_attribute("tabindex") == "0"

        main = self.driver.find_element(By.CSS_SELECTOR, "a[title='Перейти к основному разделу']")
        assert main.get_attribute("aria-current") == "true"
        assert main.get_attribute("tabindex") == "0"

        forms = self.driver.find_element(By.CSS_SELECTOR, "a[title='Формы']")
        assert forms.get_attribute("tabindex") == "0"

        media = self.driver.find_element(By.CSS_SELECTOR, "a[title='Медиа']")
        assert media.get_attribute("tabindex") == "0"

        summary = self.driver.find_element(By.ID, "faq1-sum")
        assert summary.get_attribute("aria-expanded") == "true"
        assert summary.get_attribute("tabindex") == "0"

        div = self.driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        assert div.get_attribute("aria-label") == "Редактируемая область"
        assert div.get_attribute("tabindex") == "0"

        button = self.driver.find_element(By.ID, "upload-btn")
        assert button.get_attribute("aria-label") == "Загрузить файлы"

        svg = self.driver.find_element(By.ID, "logo")
        assert svg.get_attribute("aria-labelledby") == "logoTitle logoDesc"

        username = self.driver.find_element(By.ID, "username")
        assert username.get_attribute("aria-required") == "true"

        password = self.driver.find_element(By.ID, "password")
        assert password.get_attribute("aria-describedby") == "pwd-help"

    #Проверить <progress> и <meter> на корректные значения.
    def test_test24(self):
        self.driver.get("file:///D:/testfile.html")
        progress = self.driver.find_element(By.ID, "progress")
        assert progress.get_attribute("value") == "32"
        assert progress.get_attribute("max") == "100"
        assert progress.get_attribute("aria-valuemin") == "0"
        assert progress.get_attribute("aria-valuemax") == "100"

        meter = self.driver.find_element(By.ID, "cpu")
        assert meter.get_attribute("value") == "0.72"
        assert meter.get_attribute("min") == "0"
        assert meter.get_attribute("max") == "1"
        assert meter.get_attribute("low") == "0.3"
        assert meter.get_attribute("high") == "0.9"
        assert meter.get_attribute("optimum") == "0.5"
        assert meter.get_attribute("title") == "Нагрузка на CPU"

    #Проверить <output> на динамическое обновление при изменении input-значений.
    def test_test25(self):
        self.driver.get("file:///D:/testfile.html")
        output = self.driver.find_element(By.ID, "calc-result")
        age_input = self.driver.find_element(By.ID, "age")
        volume_input = self.driver.find_element(By.ID, "volume")
        assert "Возраст 30, громкость 70" in output.text

        age_input.clear()
        age_input.send_keys("25")
        #volume_input.clear()
        #volume_input.send_keys("50") - вызывает ошибку
        self.driver.execute_script("""
               arguments[0].value = '50';
               arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
           """, volume_input)
        assert "Возраст 25, громкость 50" in output.text



