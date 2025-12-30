import pathlib

from playwright.sync_api import Page, expect
from playwright.sync_api import Playwright, sync_playwright, expect


#1️⃣ Проверить, что заголовок страницы отображается и содержит нужный текст
def test1(page: Page):
    page.goto("file:///D:/testselect.html")
    title = page.title()
    assert "Demo — Checkboxes, Radios & Selects" in title
    element = page.locator("#page-title")
    assert element.is_visible()
    assert element.text_content() == "Демо: Checkboxes, Radio Buttons и Select"

#2️⃣ Проверить, что при нажатии кнопки «Отметить все» все чекбоксы становятся отмеченными.
def test2(page: Page):
    page.goto("file:///D:/testselect.html")
    page.uncheck("#cb-news")
    page.uncheck("#cb-sports")
    page.uncheck("#cb-music")
    page.uncheck("#cb-coding")
    page.click("#check-all")
    assert page.is_checked("#cb-news")
    assert page.is_checked("#cb-sports")
    assert page.is_checked("#cb-music")
    assert page.is_checked("#cb-coding")

#3️⃣ Проверить, что при нажатии «Снять все» все чекбоксы становятся неотмеченными.
def test3(page: Page):
    page.goto("file:///D:/testselect.html")
    page.check("#cb-news")
    page.check("#cb-sports")
    page.check("#cb-music")
    page.check("#cb-coding")
    page.click("#uncheck-all")
    assert not page.is_checked("#cb-news")
    assert not page.is_checked("#cb-sports")
    assert not page.is_checked("#cb-music")
    assert not page.is_checked("#cb-coding")

#4️⃣ Проверить, что кнопка «Инвертировать» меняет состояние чекбоксов на противоположное.
def test4(page: Page):
    page.goto("file:///D:/testselect.html")
    initial_news = page.is_checked("#cb-news")
    initial_sports = page.is_checked("#cb-sports")
    page.click("#invert")
    assert page.is_checked("#cb-news") != initial_news
    assert page.is_checked("#cb-sports") != initial_sports

#5️⃣ Проверить, что при нажатии «Выбрать тёмную» активируется радиокнопка «Тёмная тема».
def test5(page: Page):
    page.goto("file:///D:/testselect.html")
    page.check("#theme-light")
    page.click("#select-dark")
    assert page.is_checked("#theme-dark")
    assert not page.is_checked("#theme-light")
    assert not page.is_checked("#theme-auto")

#6️⃣ Проверить, что в выпадающем списке (Select) можно выбрать страну, и значение сохраняется.
def test6(page: Page):
    page.goto("file:///D:/testselect.html")
    page.select_option("#single-select", "de")
    assert page.input_value("#single-select") == "de"

    page.select_option("#single-select", "fr")
    assert page.input_value("#single-select") == "fr"

    page.select_option("#single-select", "ru")
    assert page.input_value("#single-select") == "ru"

#7️⃣ Проверить, что в списке с множественным выбором (multiple select) можно выбрать несколько языков одновременно.
def test7(page: Page):
    page.goto("file:///D:/testselect.html")
    page.select_option("#multi-select", ["ru", "en", "de"])
    page.click("#show-selection")
    output = page.locator("#selection-output")
    output_text = output.text_content()
    assert "ru" in output_text
    assert "en" in output_text
    assert "de" in output_text

