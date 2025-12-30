import csv
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["element_id"], row["expected_type"], row["expected_placeholder"]))
    return data

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("file:///D:/testfile.html")
    yield driver
    driver.quit()

#Часть 1. Текстовые поля и input
#Проверка типа и placeholder через CSV
#Создать CSV с колонками: element_id, expected_type, expected_placeholder.
#Написать тест, который проверяет каждый элемент формы по этим данным.
@pytest.mark.parametrize("element_id,expected_type,expected_placeholder", read_csv("form_elements.csv"))
def testcsv(driver, element_id, expected_type, expected_placeholder):
    elem = driver.find_element(By.ID, element_id)
    assert elem.get_attribute("type") == expected_type
    assert elem.get_attribute("placeholder") == expected_placeholder

#Проверка обязательных полей через CSV
#CSV: element_id, is_required (true/false).
#Тест проверяет, что поля формы имеют/не имеют атрибут required.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["element_id"], row["is_required"]))
    return data

@pytest.mark.parametrize("element_id,is_required", read_csv("required_fields.csv"))
def test_required(driver, element_id, is_required):
    elem = driver.find_element(By.ID, element_id)
    actual_required = elem.get_attribute("required")
    if is_required.lower() == "true":
        assert actual_required is not None, f"Элемент {element_id} должен быть обязательным"
    else:
        assert actual_required is None, f"Элемент {element_id} не должен быть обязательным"

#Проверка min/max/step для числовых полей
#CSV: element_id, min_value, max_value, step.
#Тест проверяет атрибуты min, max и step для input[type=number/range].
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["element_id"], row["min_value"], row["max_value"], row["step"]))
    return data

@pytest.mark.parametrize("element_id,min_value,max_value,step", read_csv("numeric_fields.csv"))
def test_numeric(driver, element_id, min_value, max_value, step):
    elem = driver.find_element(By.ID, element_id)
    assert elem.get_attribute("min") == min_value
    assert elem.get_attribute("max") == max_value
    assert elem.get_attribute("step") == step

#Проверка multiple email через CSV
#CSV: element_id, emails.
#Тест заполняет поле и проверяет значение после ввода нескольких email.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["element_id"], row["emails"]))
    return data

@pytest.mark.parametrize("element_id,emails", read_csv("multiple_emails.csv"))
def test_multiple_emails(driver, element_id, emails):
    elem = driver.find_element(By.ID, element_id)
    elem.clear()
    elem.send_keys(emails)
    assert elem.get_attribute("value") == emails

#Часть 2. Кнопки и действия
#Проверка кнопок по CSV
#CSV: button_id, expected_text, expected_type, aria_pressed.
#Тест проверяет текст кнопки, type и состояние aria-pressed.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["button_id"], row["expected_text"], row["expected_type"], row["aria_pressed"]))
    return data


@pytest.mark.parametrize("button_id,expected_text,expected_type,aria_pressed", read_csv("buttons.csv"))
def test_buttons(driver, button_id, expected_text, expected_type, aria_pressed):
    button = driver.find_element(By.ID, button_id)
    assert button.text == expected_text
    assert button.get_attribute("type") == expected_type
    actual_aria_pressed = button.get_attribute("aria-pressed")
    expected_aria_pressed = aria_pressed if aria_pressed else None
    assert actual_aria_pressed == expected_aria_pressed

#Проверка кнопок на видимость и доступность
#CSV: button_id, is_displayed, is_enabled.
#Тест проверяет, что кнопка видима и активна.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["button_id"], row["is_displayed"], row["is_enabled"]))
    return data
@pytest.mark.parametrize("button_id,is_displayed,is_enabled", read_csv("buttons_visibility.csv"))
def test_buttons_visibility(driver, button_id, is_displayed, is_enabled):
    button = driver.find_element(By.ID, button_id)
    assert button.is_displayed() == (is_displayed.lower() == "true"), f"Неверная видимость кнопки {button_id}"
    assert button.is_enabled() == (is_enabled.lower() == "true"), f"Неверная доступность кнопки {button_id}"

#Проверка reset кнопки через CSV
#CSV: input_id, initial_value.
#Тест изменяет значение поля, нажимает reset и проверяет, что поле вернулось к initial_value.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["input_id"], row["initial_value"]))
    return data
@pytest.mark.parametrize("input_id,initial_value", read_csv("reset_test.csv"))
def test_reset(driver, input_id, initial_value):
    input_field = driver.find_element(By.ID, input_id)
    reset_button = driver.find_element(By.ID, "reset-btn")
    input_field.clear()
    input_field.send_keys("test_value")
    reset_button.click()
    assert input_field.get_attribute("value") == initial_value

#Часть 3. Таблицы
#Проверка значений таблицы через CSV
#CSV: row_index, col_index, expected_text.
#Тест проверяет содержимое каждой ячейки таблицы.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((int(row["row_index"]), int(row["col_index"]), row["expected_text"]))
    return data


@pytest.mark.parametrize("row_index,col_index,expected_text", read_csv("table_data.csv"))
def test_table_data(driver, row_index, col_index, expected_text):
    table = driver.find_element(By.ID, "data-table")
    row = table.find_elements(By.TAG_NAME, "tr")[row_index]
    cell = row.find_elements(By.TAG_NAME, "td")[col_index]
    assert cell.text == expected_text

#Проверка количества строк и колонок таблицы
#CSV: table_id, expected_rows, expected_columns.
#Тест проверяет размеры таблицы.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["table_id"], int(row["expected_rows"]), int(row["expected_columns"])))
    return data
@pytest.mark.parametrize("table_id,expected_rows,expected_columns", read_csv("table_size.csv"))
def test_table_size(driver, table_id, expected_rows, expected_columns):
    table = driver.find_element(By.ID, table_id)
    rows = table.find_elements(By.TAG_NAME, "tr")
    actual_rows = len(rows)
    first_row = rows[0]
    columns = first_row.find_elements(By.TAG_NAME, "th") or first_row.find_elements(By.TAG_NAME, "td")
    actual_columns = len(columns)
    assert actual_rows == expected_rows
    assert actual_columns == expected_columns

#Часть 4. Select / Option
#Проверка выбранных опций select через CSV
#CSV: select_id, expected_value.
#Тест проверяет, что по умолчанию выбрана правильная опция.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["select_id"], row["expected_value"]))
    return data
@pytest.mark.parametrize("select_id,expected_value", read_csv("select_options.csv"))
def test_select_options(driver, select_id, expected_value):
    select_element = driver.find_element(By.ID, select_id)
    select = Select(select_element)
    selected_option = select.first_selected_option
    actual_value = selected_option.get_attribute("value")
    assert actual_value == expected_value

#Проверка всех доступных опций select через CSV
#CSV: select_id, option_index, expected_text, expected_value.
#Тест проверяет текст и значение каждой опции.
def read_csv(file_path):
    data = []
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row["select_id"], int(row["option_index"]), row["expected_text"], row["expected_value"]))
    return data
@pytest.mark.parametrize("select_id,option_index,expected_text,expected_value", read_csv("select_all_options.csv"))
def test_select_all_options(driver, select_id, option_index, expected_text, expected_value):
    select_element = driver.find_element(By.ID, select_id)
    select = Select(select_element)
    options = select.options
    assert option_index < len(options)
    option = options[option_index]
    assert option.text == expected_text
    assert option.get_attribute("value") == expected_value