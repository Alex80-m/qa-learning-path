Feature: Проверка демо-страницы с большим количеством HTML элементов
  Эта фича проверяет корректность ключевых элементов страницы max-elements.html,
  включая заголовок, форму, таблицы, мультимедиа, интерактивные элементы
  и кастомные data-атрибуты.
  Background:
    Given я открываю локальный файл "max-elements.html"
    And я проверяю что страница загрузилась успешно


  Scenario: 1.1. Проверка всех обязательных полей
    When я ищу форму "#complex-form"
    Then поле "username" должно иметь атрибут required
    And поле "password" должно иметь атрибут required
    And поле "country" должно иметь атрибут required

  Scenario: 1.2. Проверка валидации логина по regex
    When я ищу поле "#username"
    Then поле должно иметь pattern "^[A-Za-z0-9_\-]+$"

  Scenario: 1.3. Проверка диапазона ползунка громкости
    When я ищу поле "#volume"
    Then поле должно иметь min значение "0"
    And поле должно иметь max значение "100"
    And поле должно иметь step "5"
    And поле должно иметь значение по умолчанию "70"

  Scenario: 1.4. Проверка выбора страны
    When я ищу элемент "#country"
    Then выпадающий список(select) должен содержать 4 option элемента
    And выбранная страна по умолчанию должна быть "Россия"
    And должен существовать optgroup "Европа"
    And должен существовать optgroup "Америка"

  Scenario: 1.5. Проверка email input с multiple
    When я ищу поле "#emails"
    Then поле должно иметь атрибут multiple
    And поле должно быть типа "email"
    And поле должно иметь placeholder

  Scenario: 1.6. Проверка кнопок формы
    When я ищу кнопку "#submit-btn"
    Then кнопка должна иметь атрибут formaction со значением "/save"

    When я ищу кнопку "#reset-btn"
    Then кнопка должна быть типа "reset"

    When я ищу кнопку "#upload-btn"
    Then кнопка должна быть типа "button"
    And кнопка должна иметь атрибут data-action="upload"

  Scenario: 1.7. Проверка функциональности output (#calc-result)
    Given значение поля "#age" установлено в "50"
    And значение поля "#volume" установлено в "80"
    When система обновляет расчеты
    Then output "#calc-result" должен содержать "50"
    And output "#calc-result" должен содержать "80"

  Scenario: 1.8. Проверка file input
    When я ищу поле "#attachments"
    Then поле должно иметь атрибут multiple
    And поле должно принимать файлы типа "image/*"
    And поле должно принимать файлы типа "application/pdf"
    And поле должно иметь атрибут data-max-files="5"

  Scenario: 2.1. Проверка количества колонок в таблице
    When я ищу таблицу "#data-table"
    Then таблица должна содержать <thead><tr> ровно 3 th

  Scenario: 2.2. Проверка ролей пользователей в таблице
    When я ищу атрибут "data-role"
    Then первая строка таблицы должна иметь data-role "admin"
    And вторая строка таблицы должна иметь data-role "editor"

  Scenario: 2.3. Проверка summary и caption таблицы
    When я ищу таблицу "#data-table"
    Then таблица должна иметь атрибут summary
    And таблица должна иметь caption с текстом "Мини-таблица"

  Scenario: 2.4. Проверка footer таблицы
    When я ищу таблицу "#data-table"
    Then таблица должна содержать элемент tfoot
    And footer должен содержать текст "Количество записей: 2"


  Scenario: 3.1. Проверка SVG логотипа
    When я ищу элемент "#logo"
    Then элемент должен быть SVG
    And SVG должен содержать элемент <title>
    And SVG должен содержать элемент <desc>
    And SVG должен содержать градиент <linearGradient id="g">

  Scenario: 3.2. Проверка элементов canvas
    When я ищу элемент "#myCanvas"
    Then элемент должен быть canvas
    And canvas должен иметь width = "300"
    And canvas должен иметь height = "120"

  Scenario: 3.3. Проверка video элемента
    When я ищу элемент "#demo-video"
    Then элемент должен быть video
    And video должен иметь атрибут controls
    And video должен содержать track kind="captions"

  Scenario: 3.4. Проверка audio элемента
    When я ищу элемент "#demo-audio"
    Then элемент должен быть audio
    And audio должен иметь атрибут controls
    And audio должен иметь атрибут preload="none"


  Scenario: 4.1. Проверка picture-блока
    When я ищу элемент "picture"
    Then picture должен содержать элемент source
    And source должен иметь атрибут media="(min-width:600px)"
    And picture должен содержать элемент img
    And img должен иметь атрибут alt

  Scenario: 4.2. Проверка map & area
    When я ищу элемент "map#map1"
    Then карта должна существовать
    And карта должна содержать 2 области (area)
    And первая область должна иметь title "Левая"
    And вторая область должна иметь title "Правая"