import re
import allure
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def driver():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = context.new_page()
    yield page
    context.close()
    browser.close()
    playwright.stop()


@allure.epic("Тестирование сайта Playwright.dev")
@allure.feature("Основные функции сайта")
@allure.suite("Smoke тесты")
#ТЕСТ 1
@allure.title("Тест 1: Проверка ссылки 'Docs'")
@allure.description("Нажимаем на Docs и проверяем переход")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("navigation", "main_menu")
def test_docs_navigation(page: Page):
    with allure.step("Шаг 1: Открыть главную страницу"):
        page.goto("https://playwright.dev/")
        print("Открыли сайт")
    with allure.step("Шаг 2: Кликнуть на 'Docs' в меню"):
        page.get_by_role("link", name="Docs").click()
        print("Кликнули на Docs")
    with allure.step("Шаг 3: Проверить, что перешли на страницу документации"):
        expect(page).to_have_url(re.compile(r"https://playwright.dev/docs/intro"))
        print("URL верный!")

# ТЕСТ 2
@allure.title("Тест 2: Проверка ссылки 'API'")
@allure.description("Нажимаем на API и проверяем переход")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("navigation", "main_menu")
def test_api_navigation(page: Page):
    with allure.step("Шаг 1: Открыть главную страницу"):
        page.goto("https://playwright.dev/")
        print("Открыли сайт")
    with allure.step("Шаг 2: Кликнуть на 'API' в меню"):
        page.get_by_role("link", name="API").click()
        print("Кликнули на API")
    with allure.step("Шаг 3: Проверить URL API документации"):
        expect(page).to_have_url(re.compile(r"https://playwright.dev/docs/api/class-playwright"))
        print("URL API верный!")


#ТЕСТ 3
@allure.title("Тест 3: Проверка переключения языка на Python")
@allure.description("Меняем язык документации с Node.js на Python")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("language", "settings")
def test_language_switch(page: Page):
    with allure.step("Шаг 1: Открыть страницу API"):
        page.goto("https://playwright.dev/docs/api/class-playwright")
        print("Открыли страницу API")
    with allure.step("Шаг 2: Найти и кликнуть на текущий язык (Node.js)"):
        page.locator('a.navbar__link:has-text("Node.js")').click()
        print("Открыли меню выбора языка")
    with allure.step("Шаг 3: Выбрать Python из списка"):
        page.locator('a.dropdown__link:has-text("Python")').click()
        print("Выбрали Python")
    with allure.step("Шаг 4: Проверить, что перешли на Python документацию"):
        expect(page).to_have_url(re.compile(r"https://playwright.dev/python/docs/api/class-playwright"))
        print("Язык изменен на Python!")

#ТЕСТ 4
@allure.title("Тест 4: Проверка ссылки на GitHub")
@allure.description("Кликаем на иконку GitHub и проверяем открытие новой вкладки")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("external_links", "github")
def test_github_link(page: Page):
    with allure.step("Шаг 1: Открыть главную страницу"):
        page.goto("https://playwright.dev/")
        print("Открыли сайт")
    with allure.step("Шаг 2: Кликнуть на иконку GitHub"):
        with page.expect_popup() as new_tab:
            page.get_by_role("link", name="GitHub repository").click()
        github_page = new_tab.value
        print("Открылась новая вкладка")
    with allure.step("Шаг 3: Проверить URL GitHub"):
        expect(github_page).to_have_url(re.compile(r"https://github.com/microsoft/playwright"))
        print("Это действительно GitHub Playwright!")

#ТЕСТ 5
@allure.title("Тест 5: Проверка поиска по сайту")
@allure.description("Ищем 'python' через поиск и проверяем результаты")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("search", "functionality")
def test_search_functionality(page: Page):
    with allure.step("Шаг 1: Открыть главную страницу"):
        page.goto("https://playwright.dev/")
        print("Открыли сайт")
    with allure.step("Шаг 2: Открыть поиск"):
        page.get_by_role("button", name="Search (Ctrl+K)").click()
        print("Открыли поле поиска")
    with allure.step("Шаг 3: Ввести 'python' в поиск"):
        search_box = page.get_by_role("searchbox", name="Search")
        search_box.fill("python")
        print("Ввели 'python' в поиск")
    with allure.step("Шаг 4: Нажать Enter и проверить результаты"):
        search_box.press("Enter")
        results = page.locator('.DocSearch-Modal')
        expect(results).to_contain_text("python", ignore_case=True)
        print("В результатах поиска есть 'python'!")