import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

HTML5_DND_SCRIPT = """
function simulateDragDrop(sourceNode, destinationNode) {
    var EVENT_TYPES = {
        DRAG_END: 'dragend',
        DRAG_START: 'dragstart',
        DROP: 'drop',
        DRAG_OVER: 'dragover'
    }

    function createCustomEvent(type) {
        var event = new CustomEvent(type, {
            bubbles: true,
            cancelable: true,
            detail: 0
        });
        event.dataTransfer = {
            data: {},
            setData: function(key, value) { this.data[key] = value; },
            getData: function(key) { return this.data[key]; },
            setDragImage: function() {},
            effectAllowed: 'all',
            dropEffect: 'move',
            files: [],
            types: []
        };
        return event;
    }

    function dispatchEvent(node, event, transferData) {
        if (transferData !== undefined) {
            event.dataTransfer = transferData;
        }
        node.dispatchEvent(event);
    }

    var dragStartEvent = createCustomEvent(EVENT_TYPES.DRAG_START);
    dragStartEvent.dataTransfer.setData('text/plain', sourceNode.id);
    dispatchEvent(sourceNode, dragStartEvent);

    var dragOverEvent = createCustomEvent(EVENT_TYPES.DRAG_OVER);
    dragOverEvent.preventDefault = function() {};
    dispatchEvent(destinationNode, dragOverEvent);

    var dropEvent = createCustomEvent(EVENT_TYPES.DROP);
    dropEvent.preventDefault = function() {};
    dispatchEvent(destinationNode, dropEvent, dragStartEvent.dataTransfer);

    var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
    dispatchEvent(sourceNode, dragEndEvent, dropEvent.dataTransfer);

    if (typeof window.dropHandler === 'function') {
        var ev = {
            preventDefault: function() {},
            dataTransfer: dragStartEvent.dataTransfer,
            target: destinationNode
        };
        window.dropHandler(ev);
    }
}
simulateDragDrop(arguments[0], arguments[1]);
"""


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")


    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_w3schools_drag_and_drop_image(driver):
    #Тест перетаскивания изображения между двумя div-элементами
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop2")

    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.ID, "iframeResult")))
    driver.switch_to.frame(iframe)

    draggable_img = driver.find_element(By.ID, "img1")
    div1 = driver.find_element(By.ID, "div1")
    div2 = driver.find_element(By.ID, "div2")
    assert draggable_img in div1.find_elements(By.XPATH, ".//*")

    driver.execute_script(HTML5_DND_SCRIPT, draggable_img, div2)
    time.sleep(1)

    assert draggable_img in div2.find_elements(By.XPATH, ".//*")
    assert len(div1.find_elements(By.XPATH, ".//img")) == 0
    driver.execute_script(HTML5_DND_SCRIPT, draggable_img, div1)
    time.sleep(1)

    # Проверяем, что изображение вернулось в div1
    assert draggable_img in div1.find_elements(By.XPATH, ".//*")
    assert len(div2.find_elements(By.XPATH, ".//img")) == 0



def test_drag_and_drop_with_action_chains(driver, selenium=None):
    #Альтернативный тест с использованием ActionChains.
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop2")

    wait = WebDriverWait(driver, 10)
    iframe = wait.until(EC.presence_of_element_located((By.ID, "iframeResult")))
    driver.switch_to.frame(iframe)

    draggable_img = driver.find_element(By.ID, "img1")
    div2 = driver.find_element(By.ID, "div2")

    actions = ActionChains(driver)
    actions.drag_and_drop(draggable_img, div2).perform()
    time.sleep(2)

    img_parent = draggable_img.find_element(By.XPATH, "..")
    parent_id = img_parent.get_attribute("id")


def test_drag_image_to_empty_div(driver):
    """Тест: перетаскивание изображения в пустой div2."""
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop2")
    driver.switch_to.frame(driver.find_element(By.ID, "iframeResult"))

    img = driver.find_element(By.ID, "img1")
    div2 = driver.find_element(By.ID, "div2")
    assert len(div2.find_elements(By.XPATH, ".//*")) == 0

    driver.execute_script(HTML5_DND_SCRIPT, img, div2)
    time.sleep(0.5)
    assert len(div2.find_elements(By.XPATH, ".//img")) == 1


def test_drag_multiple_times(driver):
    """Тест: многократное перетаскивание туда-обратно."""
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop2")
    driver.switch_to.frame(driver.find_element(By.ID, "iframeResult"))

    img = driver.find_element(By.ID, "img1")
    div1 = driver.find_element(By.ID, "div1")
    div2 = driver.find_element(By.ID, "div2")

    for i in range(3):
        # Из div1 в div2
        driver.execute_script(HTML5_DND_SCRIPT, img, div2)
        time.sleep(0.3)
        assert img in div2.find_elements(By.XPATH, ".//*")

        # Из div2 обратно в div1
        driver.execute_script(HTML5_DND_SCRIPT, img, div1)
        time.sleep(0.3)
        assert img in div1.find_elements(By.XPATH, ".//*")


def test_drag_image_to_itself(driver):
    """Тест: попытка перетащить изображение в тот же div (не должно измениться)."""
    driver.get("https://www.w3schools.com/html/tryit.asp?filename=tryhtml5_draganddrop2")
    driver.switch_to.frame(driver.find_element(By.ID, "iframeResult"))

    img = driver.find_element(By.ID, "img1")
    div1 = driver.find_element(By.ID, "div1")

    # Пытаемся перетащить в тот же div
    driver.execute_script(HTML5_DND_SCRIPT, img, div1)
    time.sleep(0.5)

    assert img in div1.find_elements(By.XPATH, ".//*")
