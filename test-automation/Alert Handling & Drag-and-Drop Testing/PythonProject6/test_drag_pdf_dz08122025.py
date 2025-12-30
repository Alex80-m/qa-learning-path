import os
import tempfile
import time
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def page_url():
    file_path = os.path.join(os.path.dirname(__file__), "testfile3.html")
    return "file:///" + file_path.replace("\\", "/")


def test_drag_and_drop_existing_pdf(driver, page_url):
    """Тест загрузки существующего PDF файла через drag-and-drop."""
    pdf_path = os.path.join(os.path.dirname(__file__), "file.pdf")
    driver.get(page_url)
    drop_zone = driver.find_element(By.ID, "dropZone")

    js_script = """
    const dropZone = arguments[0];
    const filePath = arguments[1];
    const fileName = filePath.split('/').pop();

    // Создаем fake File объект
    const file = new File(['test content'], fileName, {
        type: arguments[2]
    });

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);

    const event = new DragEvent('drop', {
        bubbles: true,
        cancelable: true,
        dataTransfer: dataTransfer
    });

    dropZone.dispatchEvent(event);
    """
    driver.execute_script(js_script, drop_zone, pdf_path, 'application/pdf')
    time.sleep(1)

    file_list = driver.find_element(By.ID, "fileList").text
    assert "pdf" in file_list.lower()
    print(f"PDF файл успешно обработан: {file_list}")

def test_drag_and_drop_existing_image(driver, page_url):
    """Тест загрузки изображения через drag-and-drop."""
    image_path = os.path.join(os.path.dirname(__file__), "file.jpg")
    driver.get(page_url)
    drop_zone = driver.find_element(By.ID, "dropZone")

    js_script = """
    const dropZone = arguments[0];
    const filePath = arguments[1];
    const fileName = filePath.split('/').pop();

    // Создаем fake File объект
    const file = new File(['fake image content'], fileName, {
        type: 'image/jpeg'
    });

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);

    const event = new DragEvent('drop', {
        dataTransfer: dataTransfer,
        bubbles: true
    });

    dropZone.dispatchEvent(event);
    """
    driver.execute_script(js_script, drop_zone, image_path, 'image/jpeg')
    time.sleep(1)

    file_list = driver.find_element(By.ID, "fileList").text
    assert "jpg" in file_list.lower() or "file.jpg" in file_list.lower()
    print(f"JPG изображение успешно обработано: {file_list}")


def test_drag_and_drop_existing_docx(driver, page_url):
    """Тест загрузки DOCX файла через drag-and-drop."""
    docx_path = os.path.join(os.path.dirname(__file__), "file.docx")
    driver.get(page_url)
    drop_zone = driver.find_element(By.ID, "dropZone")

    js_script = """
    const dropZone = arguments[0];
    const filePath = arguments[1];
    const fileName = filePath.split('/').pop();

    // Создаем fake File объект
    const file = new File(['fake doc content'], fileName, {
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    });

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);

    const event = new DragEvent('drop', {
        dataTransfer: dataTransfer,
        bubbles: true
    });

    dropZone.dispatchEvent(event);
    """
    driver.execute_script(js_script, drop_zone, docx_path,
                          'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    time.sleep(1)

    file_list = driver.find_element(By.ID, "fileList").text
    assert "docx" in file_list.lower() or "file.docx" in file_list.lower()
    print(f"DOCX файл успешно обработан: {file_list}")


def test_drag_and_drop_multiple_existing_files(driver, page_url):
    """Тест загрузки нескольких существующих файлов разных типов."""
    driver.get(page_url)
    drop_zone = driver.find_element(By.ID, "dropZone")
    test_files = [
        ("file.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("file.jpg", "image/jpeg"),
        ("file.pdf", "application/pdf")
    ]

    existing_files = []
    for filename, mime_type in test_files:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(file_path):
            existing_files.append((filename, mime_type))
        else:
            print(f"Файл {filename} не найден, пропускаем")

    if not existing_files:
        pytest.skip("Нет существующих файлов для тестирования")

    js_script = """
    const dropZone = arguments[0];
    const filesData = arguments[1];

    const dataTransfer = new DataTransfer();

    filesData.forEach(fileInfo => {
        const fileName = fileInfo[0].split('/').pop();
        const file = new File(['test content for ' + fileName], fileName, {
            type: fileInfo[1]
        });
        dataTransfer.items.add(file);
    });

    const event = new DragEvent('drop', {
        dataTransfer: dataTransfer,
        bubbles: true
    });

    dropZone.dispatchEvent(event);
    """
    driver.execute_script(js_script, drop_zone, existing_files)
    time.sleep(1)

    files_count = drop_zone.get_attribute('data-files-count')
    assert files_count == str(len(existing_files))

    file_list = driver.find_element(By.ID, "fileList").text
    print(f"Список загруженных файлов:\n{file_list}")

    for filename, mime_type in test_files:
        file_ext = filename.split('.')[-1]
        if file_ext in ['docx', 'jpg', 'pdf']:
            assert file_ext in file_list.lower()

    print(f"Все {len(existing_files)} файлов успешно обработаны")

def test_drag_and_drop_empty(driver, page_url):
    """Тест попытки перетаскивания без файлов."""
    driver.get(page_url)
    drop_zone = driver.find_element(By.ID, "dropZone")
    js_script = """
    const dropZone = arguments[0];
    const dataTransfer = new DataTransfer();
    const event = new DragEvent('drop', {
        dataTransfer: dataTransfer,
        bubbles: true
    });
    dropZone.dispatchEvent(event);
    """
    driver.execute_script(js_script, drop_zone)
    time.sleep(0.5)

    file_list = driver.find_element(By.ID, "fileList").text
    assert "Загруженные файлы:" in file_list

    files_count = drop_zone.get_attribute('data-files-count')
    assert files_count == '0'

    print("Пустой drag-and-drop корректно обработан")


