
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from faker import Faker
from datetime import datetime
import random
import re


# Инициализация Faker
fake = Faker("ru_RU")

@pytest.fixture(scope="module")
def driver():
    """Фикстура для инициализации и завершения сессии браузера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# --------------------------------------------
#Задание 1
#Сгенерировать тестовые данные для формы регистрации (имя, фамилия, email, пароль) с помощью Faker.
#Заполнить веб-форму и проверить, что все поля корректно заполнены.
# --------------------------------------------
def test_fill_registration_form(driver):
    generated_username = fake.first_name()
    generated_email = fake.email()
    generated_password = fake.password(length=12)

    print(f"\nСгенерированные данные для формы:\n \
    - Username (Имя): {generated_username}\n \
    - Email: {generated_email}\n \
    - Password: {generated_password}")

    driver.get(f"file:///D:/testfile.html")

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    email_input = driver.find_element(By.ID, "emails")

    username_input.clear()
    username_input.send_keys(generated_username)

    password_input.clear()
    password_input.send_keys(generated_password)

    email_input.clear()
    email_input.send_keys(generated_email)

    assert username_input.get_attribute("value") == generated_username
    assert password_input.get_attribute("value") == generated_password
    assert email_input.get_attribute("value") == generated_email

# --------------------------------------------
#Задание 2
#Создать тест, который генерирует случайный список мини-таблицы (имя, роль, активность).
#Проверить, что количество записей больше 0, а итоговая сумма  вычисляется правильно.
# --------------------------------------------
def test_table_data_generation(driver):
    table_data = []
    record_count = random.randint(1, 5)

    for i in range(record_count):
        record = {
            "name": fake.first_name(),
            "role": random.choice(["Admin", "Editor", "User"]),
            "active": random.choice(["Да", "Нет"])
        }
        table_data.append(record)
    print(f"\nСгенерированные данные таблицы ({len(table_data)} записей):")

    driver.get("file:///D:/testfile.html")

    for record in table_data:
        print(f"  Имя: {record['name']}, Роль: {record['role']}, Активен: {record['active']}")
    assert len(table_data) > 0, "Количество записей должно быть больше 0"

    calculated_total = len(table_data)
    assert calculated_total == record_count, f"Ожидалось {record_count}, получено {calculated_total}"

# --------------------------------------------
#Задание 3
#Сгенерировать 10 случайных email и password(пароль).
#Проверить, что все email содержат символ @, а password - не менее 8 символов.
# --------------------------------------------
def test_email_password_generation(driver):
    test_data = []
    for _ in range(10):
        email = fake.email()
        password = fake.password(length=random.randint(8, 12))
        test_data.append((email, password))

    driver.get("file:///D:/testfile.html")
    for email, password in test_data:
        print(f"Email: {email}, Password: {password}")
        assert "@" in email, f"Email {email} не содержит @"
        assert len(password) >= 8, f"Password {password} менее 8 символов"

# --------------------------------------------
#Задание 4
#Сгенерировать Faker с разными локалями.
# --------------------------------------------
def test_simple_locales(driver):
    driver.get("file:///D:/testfile.html")

    print()

    for locale in ['ru_RU', 'en_US', 'de_DE']:
        fake = Faker(locale)

        name = fake.name()
        email = fake.email()
        print(f"{locale}: {name} - {email}")

# --------------------------------------------
#Задание 5
#Сгенерировать случайные пароли и проверить их сложность:
# --------------------------------------------
def test_simple_password_check():
    fake = Faker()
    print()

    for i in range(5):
        password = fake.password(12, True, True, True, True)
        checks = [
            len(password) >= 8,
            bool(re.search(r'[A-Z]', password)),
            bool(re.search(r'[a-z]', password)),
            bool(re.search(r'\d', password)),
            bool(re.search(r'[!@#$%^&*]', password))
        ]
        print(f"{i + 1}. {password} - Сложность: {sum(checks)}/5")
        assert sum(checks) >= 3, f"Пароль '{password}' слишком простой"

# --------------------------------------------
#Задание 6
#Создать параметризованный тест с разными типами пользователей (admin, guest, member).
#Для каждого типа сгенерировать уникальные данные и проверить корректность заполнения формы входа.
# --------------------------------------------
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("file:///D:/testfile.html")  # Укажи свой путь
    yield driver
    driver.quit()

@pytest.mark.parametrize("user_type,expected_role", [
    ("admin", "Админ"),
    ("guest", "Гость"),
    ("member", "Пользователь"),
])
def test_different_user_types(driver, user_type, expected_role):

    print(f"\n=== Тестируем тип: {user_type} ===")

    user_data = {
        "username": f"{user_type}_{fake.user_name()}",
        "email": fake.email(),
        "password": fake.password(length=10),
        "role": expected_role
    }

    print(f"Логин: {user_data['username']}")
    print(f"Email: {user_data['email']}")
    print(f"Пароль: {user_data['password']}")
    print(f"Роль: {user_data['role']}")

    driver.find_element(By.ID, "username").clear()
    driver.find_element(By.ID, "username").send_keys(user_data['username'])

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(user_data['password'])

    assert "@" in user_data['email'], "Email должен содержать @"
    assert len(user_data['password']) >= 8, "Пароль должен быть ≥ 8 символов"
    assert user_type in user_data['username'], "Логин должен содержать тип пользователя"

# --------------------------------------------
#Задание 7
#Сгенерировать случайные адреса с помощью Faker.
#Проверить, что в каждом адресе есть номер дома и что строка не длиннее 100 символов.
# --------------------------------------------
def test_minimal_address_check(driver):
    fake = Faker('ru_RU')

    print()

    for i in range(5):
        address = fake.address().replace('\n', ', ')
        assert any(char.isdigit() for char in address), "Нет номера дома"
        assert len(address) <= 100, "Адрес слишком длинный"
        print(f"{i + 1}. {address}")

        textarea = driver.find_element(By.ID, "bio")
        textarea.clear()
        textarea.send_keys(f"Адрес {i + 1}: {address}")

# --------------------------------------------
#Задание 8
#Сгенерировать случайные даты рождения с помощью Faker.
#Проверить, что возраст каждого пользователя находится в пределах от 18 до 70 лет.
# --------------------------------------------
def test_age_in_form(driver):
    fake = Faker('ru_RU')

    for i in range(5):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
        age = datetime.now().year - birth_date.year
        print(f"\n{i + 1}. Дата рождения: {birth_date.strftime('%d.%m.%Y')}")
        print(f"   Возраст: {age} лет")

        assert 18 <= age <= 70, f"Возраст {age} не в пределах 18-70 лет"

        age_input = driver.find_element(By.ID, "age")
        age_input.clear()
        age_input.send_keys(str(age))

        actual_value = age_input.get_attribute("value")
        assert actual_value == str(age), f"Ожидалось {age}, получено {actual_value}"
        print("Возраст в пределах 18-70 лет")

# --------------------------------------------
#Задание 9
#Создать тест, который случайным образом выбирает город и генерирует почтовый индекс.
#Проверить, что индекс состоит из 5 или 6 цифр и соответствует формату региона.
# --------------------------------------------
def test_city_and_postal_code(driver):
    fake = Faker('ru_RU')

    for i in range(5):
        city = fake.city()
        postal_code = fake.postcode()

        textarea = driver.find_element(By.ID, "bio")
        textarea.clear()
        textarea.send_keys(f"{i + 1}. Город: {city}, Индекс: {postal_code}\n")

        print(f"\n{i + 1}. Город: {city}")
        print(f"   Почтовый индекс: {postal_code}")

        assert postal_code.isdigit(), f"Индекс '{postal_code}' должен содержать только цифры"
        assert len(postal_code) in [5, 6], f"Индекс '{postal_code}' должен быть 5 или 6 цифр"

# --------------------------------------------
#Задание 10
#С помощью Faker сгенерировать несколько профилей пользователей (fake.simple_profile()).
#Проверить, что email уникален для каждого профиля и возраст соответствует дате рождения.
# --------------------------------------------
def test_minimal_profiles(driver):
    fake = Faker('ru_RU')

    print()
    emails = set()

    for i in range(5):
        profile = fake.simple_profile()

        assert profile['mail'] not in emails
        emails.add(profile['mail'])

        birth_year = profile['birthdate'].year
        current_year = datetime.now().year
        age = current_year - birth_year
        assert 0 <= age <= 120, f"Некорректный возраст {age} для даты {profile['birthdate']}"

        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(profile['username'])
        driver.find_element(By.ID, "emails").clear()
        driver.find_element(By.ID, "emails").send_keys(profile['mail'])
        driver.find_element(By.ID, "age").clear()
        driver.find_element(By.ID, "age").send_keys(str(age))

        driver.find_element(By.ID, "bio").clear()
        driver.find_element(By.ID, "bio").send_keys(
            f"Профиль {i + 1}: {profile['name']}\n"
            f"Пол: {profile['sex']}\n"
            f"Адрес: {profile['address']}\n"
            f"Дата рождения: {profile['birthdate']}"
        )
        print(f"{i + 1}. {profile['name']} - {age} лет - {profile['mail']}")

# --------------------------------------------
#Задание 11
#Создать тест на проверку на 6 разных устройств в безголовом режиме с поиском элмента по tag name
# --------------------------------------------
def test_different_screen_sizes():
    devices_sizes = [
        ("iPhone SE", 375, 667),
        ("Pixel 7", 412, 915),
        ("iPad Air", 768, 1024),
        ("Galaxy S5", 360, 640),
        ("Nexus 6P", 412, 732),
        ("iPhone 12 Pro", 390, 844)
    ]

    for device, width, height in devices_sizes:
        mobile_emulation = {"deviceName": device}

        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=chrome_options)


        driver.set_window_size(width, height)
        driver.get("file:///D:/testfile.html")
        window_size = driver.get_window_size()

        print(f"\n{device}:")
        print(f"  Заданный размер: {width}x{height}")
        print(f"  Фактический размер: {window_size['width']}x{window_size['height']}")

        inputs = driver.find_elements(By.TAG_NAME, "input")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")

