import re
from playwright.sync_api import Page, expect

#ТК 1: Проверка функциональности элемента "Docs" в навигационном меню.
def test_example1(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Docs").click()
    expect(page).to_have_url(re.compile(r"https://playwright.dev/docs/intro"))

#ТК 2: Проверка функциональности элемента "API" в навигационном меню.
def test_example2(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="API").click()
    expect(page).to_have_url(re.compile(r"https://playwright.dev/docs/api/class-playwright"))

#ТК 3: Проверка переключения языка программирования
def test_example3(page: Page):
    page.goto("https://playwright.dev/docs/api/class-playwright")
    current_language_link = page.locator('a.navbar__link:has-text("Node.js")')
    current_language_link.click()
    python_language_option = page.locator('a.dropdown__link:has-text("Python")')
    expect(python_language_option).to_be_visible()
    python_language_option.click()
    expect(page).to_have_url(re.compile(r"https://playwright.dev/python/docs/api/class-playwright"))

#ТК 4: Проверка функциональности элемента "Community" в навигационном меню.
def test_example4(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Community").click()
    expect(page).to_have_url(re.compile(r"https://playwright.dev/community/welcome"))

#ТК 5: Проверка функциональности иконки GitHub в шапке.
def test_example5(page: Page):
    page.goto("https://playwright.dev/")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="GitHub repository").click()
    page1 = page1_info.value
    expect(page1).to_have_url(re.compile(r"https://github.com/microsoft/playwright"))

#ТК 6: Проверка функциональности иконки Discord в шапке.
def test_example6(page: Page):
    page.goto("https://playwright.dev/")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Discord server").click()
    page1 = page1_info.value
    expect(page1).to_have_url(re.compile(r"https://discord.com/servers/playwright-807756831384403968"))

#ТК 7: Проверка функциональности поля поиска.
def test_example7(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("button", name="Search (Ctrl+K)").click()
    page.get_by_role("searchbox", name="Search").fill("python")
    page.get_by_role("searchbox", name="Search").press("Enter")
    locator_for_text_in_modal = page.locator('.DocSearch-Modal')
    expect(locator_for_text_in_modal).to_contain_text("python", ignore_case=True)

#ТК 8: Проверка переключения темы (system mode).
def test_example8(page: Page):
    page.goto("https://playwright.dev/")
    theme_toggle_button = page.get_by_label(re.compile(r"Switch between dark and light mode", re.IGNORECASE))
    theme_toggle_button.click()
    light_icon = theme_toggle_button.locator('.lightToggleIcon_pyhR')
    expect(light_icon).to_be_visible()
    expect(theme_toggle_button.locator('.systemToggleIcon_QzmC')).to_be_hidden()
    expect(theme_toggle_button.locator('.darkToggleIcon_wfgR')).to_be_hidden()
    theme_toggle_button.click()
    dark_icon = theme_toggle_button.locator('.darkToggleIcon_wfgR')
    expect(dark_icon).to_be_visible()
    expect(theme_toggle_button.locator('.systemToggleIcon_QzmC')).to_be_hidden()
    expect(theme_toggle_button.locator('.lightToggleIcon_pyhR')).to_be_hidden()
    theme_toggle_button.click()
    system_icon = theme_toggle_button.locator('.systemToggleIcon_QzmC')
    expect(system_icon).to_be_visible()
    expect(theme_toggle_button.locator('.lightToggleIcon_pyhR')).to_be_hidden()
    expect(theme_toggle_button.locator('.darkToggleIcon_wfgR')).to_be_hidden()

#ТК 9: Проверка функциональности кнопки "Get started "
def test_example9(page: Page):
    page.goto("https://playwright.dev/")
    page.get_by_role("link", name="Get started").click()
    expect(page).to_have_url(re.compile(r"https://playwright.dev/docs/intro"))

#ТК 10: Проверка ссылки на YouTube в разделе "More" подвала
def test_example10(page: Page):
    page.goto("https://playwright.dev/")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="YouTube").click()
    page1 = page1_info.value
    expect(page1).to_have_url(re.compile(r"https://www.youtube.com/channel/UC46Zj8pDH5tDosqm1gd7WTg"))

