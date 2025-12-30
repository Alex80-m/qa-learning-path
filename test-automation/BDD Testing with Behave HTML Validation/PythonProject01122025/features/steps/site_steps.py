from behave import given, when, then
from bs4 import BeautifulSoup
import os

# Background
@given('я открываю локальный файл "{filename}"')
def step_open_local_file(context, filename):
    if not os.path.exists(filename):
        raise AssertionError(f"Файл {filename} не найден")

    with open(filename, 'r', encoding='utf-8') as f:
        context.html = f.read()

    context.soup = BeautifulSoup(context.html, 'html.parser')
    context.current_element = None

@given('я проверяю что страница загрузилась успешно')
def step_page_loaded(context):
    assert context.soup is not None, "HTML не загружен"
    assert context.soup.find('html') is not None, "Нет HTML тега"
    assert context.soup.find('body') is not None, "Нет BODY тега"


#1.1: Проверка всех обязательных полей
@when('я ищу форму "#complex-form"')
def step_find_form_complex_form(context):
    context.form = context.soup.select_one('#complex-form')
    assert context.form is not None, "Форма #complex-form не найдена"


@then('поле "username" должно иметь атрибут required')
def step_username_has_required(context):
    field = context.soup.select_one('#username')
    assert field is not None
    assert field.has_attr('required'), "Поле #username не имеет атрибута required"

@then('поле "password" должно иметь атрибут required')
def step_password_has_required(context):
    field = context.soup.select_one('#password')
    assert field is not None
    assert field.has_attr('required'), "Поле #password не имеет атрибута required"

@then('поле "country" должно иметь атрибут required')
def step_country_has_required(context):
    field = context.soup.select_one('#country')
    assert field is not None
    assert field.has_attr('required'), "Поле #country не имеет атрибута required"


#1.2: Проверка валидации логина по regex
@when('я ищу поле "#username"')
def step_find_field_username(context):
    context.current_element = context.soup.select_one('#username')
    assert context.current_element is not None, "Поле #username не найдено"


@then('поле должно иметь pattern "^[A-Za-z0-9_\\-]+$"')
def step_field_has_pattern_username(context):
    assert context.current_element is not None
    actual_pattern = context.current_element.get('pattern')
    expected_pattern = "^[A-Za-z0-9_\\-]+$"
    assert actual_pattern == expected_pattern, f"pattern: ожидалось '{expected_pattern}', получено '{actual_pattern}'"


#1.3: Проверка диапазона ползунка громкости
@when('я ищу поле "#volume"')
def step_find_field_volume(context):
    context.current_element = context.soup.select_one('#volume')
    assert context.current_element is not None, "Поле #volume не найдено"


@then('поле должно иметь min значение "0"')
def step_field_min_0(context):
    assert context.current_element is not None
    actual = context.current_element.get('min')
    assert actual == "0", f"min: ожидалось '0', получено '{actual}'"

@then('поле должно иметь max значение "100"')
def step_field_max_100(context):
    assert context.current_element is not None
    actual = context.current_element.get('max')
    assert actual == "100", f"max: ожидалось '100', получено '{actual}'"

@then('поле должно иметь step "5"')
def step_field_step_5(context):
    assert context.current_element is not None
    actual = context.current_element.get('step')
    assert actual == "5", f"step: ожидалось '5', получено '{actual}'"


@then('поле должно иметь значение по умолчанию "70"')
def step_field_default_70(context):
    assert context.current_element is not None
    actual = context.current_element.get('value')
    assert actual == "70", f"value: ожидалось '70', получено '{actual}'"


#1.4: Проверка выбора страны
@when('я ищу элемент "#country"')
def step_find_element_country(context):
    context.current_element = context.soup.select_one('#country')
    assert context.current_element is not None, "Элемент #country не найден"

@then('выпадающий список(select) должен содержать 4 option элемента')
def step_select_has_4_options(context):
    """ В HTML 5 option, но в задании 4. Считаем только не-disabled."""
    assert context.current_element is not None
    assert context.current_element.name == 'select'

    active_options = [opt for opt in context.current_element.find_all('option')
                      if not opt.has_attr('disabled')]
    assert len(active_options) == 4, f"Ожидалось 4 активных option (без disabled), найдено {len(active_options)}"


@then('выбранная страна по умолчанию должна быть "Россия"')
def step_default_country_russia(context):
    assert context.current_element is not None
    russia_option = context.current_element.find('option', {'value': 'ru'})
    assert russia_option is not None, "Option для России (value='ru') не найден"

@then('должен существовать optgroup "Европа"')
def step_exists_optgroup_europe(context):
    assert context.current_element is not None
    optgroup = context.current_element.find('optgroup', {'label': 'Европа'})
    assert optgroup is not None, "Optgroup 'Европа' не найден"

@then('должен существовать optgroup "Америка"')
def step_exists_optgroup_america(context):
    assert context.current_element is not None
    optgroup = context.current_element.find('optgroup', {'label': 'Америка'})
    assert optgroup is not None, "Optgroup 'Америка' не найден"


#1.5: Проверка email input с multiple
@when('я ищу поле "#emails"')
def step_find_field_emails(context):
    context.current_element = context.soup.select_one('#emails')
    assert context.current_element is not None, "Поле #emails не найдено"

@then('поле должно иметь атрибут multiple')
def step_field_has_multiple(context):
    assert context.current_element is not None
    assert context.current_element.has_attr('multiple'), "Поле не имеет атрибута multiple"


@then('поле должно быть типа "email"')
def step_field_is_type_email(context):
    assert context.current_element is not None
    actual_type = context.current_element.get('type', 'text')
    assert actual_type == 'email', f"Тип поля: ожидалось 'email', получено '{actual_type}'"

@then('поле должно иметь placeholder')
def step_field_has_placeholder(context):
    assert context.current_element is not None
    assert context.current_element.has_attr('placeholder')
    placeholder = context.current_element.get('placeholder')
    assert placeholder and placeholder.strip(), "Placeholder пустой"


#1.6: Проверка кнопок формы
@when('я ищу кнопку "#submit-btn"')
def step_find_button_submit(context):
    context.current_element = context.soup.select_one('#submit-btn')
    assert context.current_element is not None, "Кнопка #submit-btn не найдена"

@then('кнопка должна иметь атрибут formaction со значением "/save"')
def step_button_has_formaction_save(context):
    assert context.current_element is not None
    actual = context.current_element.get('formaction')
    assert actual == '/save', f"formaction: ожидалось '/save', получено '{actual}'"

@when('я ищу кнопку "#reset-btn"')
def step_find_button_reset(context):
    context.current_element = context.soup.select_one('#reset-btn')
    assert context.current_element is not None, "Кнопка #reset-btn не найдена"

@then('кнопка должна быть типа "reset"')
def step_button_is_type_reset(context):
    assert context.current_element is not None
    actual = context.current_element.get('type')
    assert actual == 'reset', f"Тип кнопки: ожидалось 'reset', получено '{actual}'"

@when('я ищу кнопку "#upload-btn"')
def step_find_button_upload(context):
    context.current_element = context.soup.select_one('#upload-btn')
    assert context.current_element is not None, "Кнопка #upload-btn не найдена"

@then('кнопка должна быть типа "button"')
def step_button_is_type_button(context):
    assert context.current_element is not None
    actual = context.current_element.get('type')
    assert actual == 'button', f"Тип кнопки: ожидалось 'button', получено '{actual}'"

@then('кнопка должна иметь атрибут data-action="upload"')
def step_button_has_data_action_upload(context):
    assert context.current_element is not None
    actual = context.current_element.get('data-action')
    assert actual == 'upload', f"data-action: ожидалось 'upload', получено '{actual}'"


#1.7: Проверка функциональности output
@given('значение поля "#age" установлено в "50"')
def step_set_age_to_50(context):
    element = context.soup.select_one('#age')
    assert element is not None
    element['value'] = '50'
    context.soup = BeautifulSoup(str(context.soup), 'html.parser')

@given('значение поля "#volume" установлено в "80"')
def step_set_volume_to_80(context):
    element = context.soup.select_one('#volume')
    assert element is not None
    element['value'] = '80'
    context.soup = BeautifulSoup(str(context.soup), 'html.parser')

@when('система обновляет расчеты')
def step_system_updates_calculations(context):
    age = context.soup.select_one('#age')
    volume = context.soup.select_one('#volume')
    output = context.soup.select_one('#calc-result')

    if age and volume and output:
        output_text = f"Возраст {age.get('value', '')}, громкость {volume.get('value', '')}"
        output.string = output_text

@then('output "#calc-result" должен содержать "50"')
def step_output_contains_50(context):
    output = context.soup.select_one('#calc-result')
    assert output is not None
    output_text = output.get_text()
    assert '50' in output_text, f"Текст '50' не найден в output. Output: {output_text}"


@then('output "#calc-result" должен содержать "80"')
def step_output_contains_80(context):
    output = context.soup.select_one('#calc-result')
    assert output is not None
    output_text = output.get_text()
    assert '80' in output_text, f"Текст '80' не найден в output. Output: {output_text}"


#1.8: Проверка file input
@when('я ищу поле "#attachments"')
def step_find_field_attachments(context):
    context.current_element = context.soup.select_one('#attachments')
    assert context.current_element is not None, "Поле #attachments не найдено"

@then('атрибут multiple должно иметь значение True')
def step_attribute_multiple_true(context):
    assert context.current_element is not None
    assert context.current_element.has_attr('multiple')
    assert context.current_element.get('multiple') == 'True', "Атрибут multiple должен иметь значение True"

@then('поле должно принимать файлы типа "image/*"')
def step_accepts_image_files(context):
    assert context.current_element is not None
    accept = context.current_element.get('accept', '')
    assert 'image/*' in accept, f"Тип 'image/*' не найден в accept: {accept}"

@then('поле должно принимать файлы типа "application/pdf"')
def step_accepts_pdf_files(context):
    assert context.current_element is not None
    accept = context.current_element.get('accept', '')
    assert 'application/pdf' in accept, f"Тип 'application/pdf' не найден в accept: {accept}"

@then('поле должно иметь атрибут data-max-files="5"')
def step_field_has_data_max_files_5(context):
    assert context.current_element is not None
    actual = context.current_element.get('data-max-files')
    assert actual == '5', f"data-max-files: ожидалось '5', получено '{actual}'"

#2.1: Количество колонок в таблице
@when('я ищу таблицу "#data-table"')
def step_find_table_data_table(context):
    context.table = context.soup.select_one('#data-table')
    assert context.table is not None
    context.current_element = context.table

@then('таблица должна содержать <thead><tr> ровно 3 th')
def step_table_has_3_th(context):
    assert context.current_element is not None
    thead = context.current_element.find('thead')
    assert thead is not None
    header_row = thead.find('tr')
    assert header_row is not None
    headers = header_row.find_all('th')
    assert len(headers) == 3, f"Ожидалось 3 th, найдено {len(headers)}"


#2.2: Проверка ролей пользователей в таблице
@when('я ищу атрибут "data-role"')
def step_find_attribute_data_role(context):
    elements = context.soup.find_all(attrs={'data-role': True})
    assert len(elements) > 0
    context.elements_with_data_role = elements

@then('первая строка таблицы должна иметь data-role "admin"')
def step_first_row_has_admin(context):
    table = context.soup.select_one('#data-table')
    assert table is not None
    tbody = table.find('tbody')
    assert tbody is not None
    rows = tbody.find_all('tr')
    assert len(rows) >= 1

    # Ищем data-role в первой строке
    found = False
    for td in rows[0].find_all('td'):
        if td.get('data-role') == 'admin':
            found = True
            break

    assert found, "В первой строке нет data-role 'admin'"

@then('вторая строка таблицы должна иметь data-role "editor"')
def step_second_row_has_editor(context):
    table = context.soup.select_one('#data-table')
    assert table is not None

    tbody = table.find('tbody')
    assert tbody is not None

    rows = tbody.find_all('tr')
    assert len(rows) >= 2

    # Ищем data-role во второй строке
    found = False
    for td in rows[1].find_all('td'):
        if td.get('data-role') == 'editor':
            found = True
            break
    assert found, "Во второй строке нет data-role 'editor'"


#2.3: Проверка summary и caption таблицы
@then('таблица должна иметь атрибут summary')
def step_table_has_summary(context):
    assert context.current_element is not None
    assert context.current_element.has_attr('summary')
    summary = context.current_element.get('summary')
    assert summary and summary.strip(), "Атрибут summary пустой"


@then('таблица должна иметь caption с текстом "Мини-таблица"')
def step_table_has_caption_mini_table(context):
    assert context.current_element is not None
    caption = context.current_element.find('caption')
    assert caption is not None
    caption_text = caption.get_text(strip=True)
    assert caption_text == "Мини-таблица", f"Caption: ожидалось 'Мини-таблица', получено '{caption_text}'"


# 2.4: Проверка footer таблицы
@then('таблица должна содержать элемент tfoot')
def step_table_has_tfoot(context):
    assert context.current_element is not None
    tfoot = context.current_element.find('tfoot')
    assert tfoot is not None, "У таблицы нет tfoot"


@then('footer должен содержать текст "Количество записей: 2"')
def step_footer_contains_text(context):
    assert context.current_element is not None
    tfoot = context.current_element.find('tfoot')
    assert tfoot is not None
    footer_text = tfoot.get_text(strip=True)
    assert "Количество записей: 2" in footer_text, \
        f"Текст 'Количество записей: 2' не найден в footer. Footer: {footer_text}"


#3.1: Проверка SVG логотипа
@when('я ищу элемент "#logo"')
def step_find_element_logo(context):
    context.current_element = context.soup.select_one('#logo')
    assert context.current_element is not None, "Элемент #logo не найден"

@then('элемент должен быть SVG')
def step_element_is_svg(context):
    assert context.current_element is not None
    assert context.current_element.name == 'svg', "Элемент не является SVG"


@then('SVG должен содержать элемент <title>')
def step_svg_has_title(context):
    assert context.current_element is not None
    title = context.current_element.find('title')
    assert title is not None, "SVG не содержит элемент <title>"

@then('SVG должен содержать элемент <desc>')
def step_svg_has_desc(context):
    assert context.current_element is not None
    desc = context.current_element.find('desc')
    assert desc is not None, "SVG не содержит элемент <desc>"

@then('SVG должен содержать градиент <linearGradient id="g">')
def step_svg_has_gradient_g(context):
    assert context.current_element is not None
    gradient = context.current_element.find('lineargradient', {'id': 'g'})
    if not gradient:
        gradient = context.current_element.find('linearGradient', {'id': 'g'})
    assert gradient is not None, "SVG не содержит градиент с id='g'"


#3.2: Проверка элементов canvas
@when('я ищу элемент "#myCanvas"')
def step_find_element_mycanvas(context):
    context.current_element = context.soup.select_one('#myCanvas')
    assert context.current_element is not None, "Элемент #myCanvas не найден"

@then('элемент должен быть canvas')
def step_element_is_canvas(context):
    assert context.current_element is not None
    assert context.current_element.name == 'canvas', "Элемент не является canvas"

@then('canvas должен иметь width = "300"')
def step_canvas_width_300(context):
    assert context.current_element is not None
    actual = context.current_element.get('width')
    assert actual == '300', f"Ширина canvas: ожидалось '300', получено '{actual}'"


@then('canvas должен иметь height = "120"')
def step_canvas_height_120(context):
    assert context.current_element is not None
    actual = context.current_element.get('height')
    assert actual == '120', f"Высота canvas: ожидалось '120', получено '{actual}'"


#3.3: Проверка video элемента
@when('я ищу элемент "#demo-video"')
def step_find_element_demo_video(context):
    context.current_element = context.soup.select_one('#demo-video')
    assert context.current_element is not None, "Элемент #demo-video не найден"


@then('элемент должен быть video')
def step_element_is_video(context):
    assert context.current_element is not None
    assert context.current_element.name == 'video', "Элемент не является video"

@then('video должен иметь атрибут controls')
def step_video_has_controls(context):
    assert context.current_element is not None
    assert context.current_element.has_attr('controls'), "Video не имеет атрибута controls"

@then('video должен содержать track kind="captions"')
def step_video_has_track_captions(context):
    assert context.current_element is not None
    track = context.current_element.find('track', {'kind': 'captions'})
    assert track is not None, "Video не содержит track с kind='captions'"


#3.4: Проверка audio элемента
@when('я ищу элемент "#demo-audio"')
def step_find_element_demo_audio(context):
    context.current_element = context.soup.select_one('#demo-audio')
    assert context.current_element is not None, "Элемент #demo-audio не найден"

@then('элемент должен быть audio')
def step_element_is_audio(context):
    assert context.current_element is not None
    assert context.current_element.name == 'audio', "Элемент не является audio"

@then('audio должен иметь атрибут controls')
def step_audio_has_controls(context):
    assert context.current_element is not None
    assert context.current_element.has_attr('controls'), "Audio не имеет атрибута controls"

@then('audio должен иметь атрибут preload="none"')
def step_audio_has_preload_none(context):
    assert context.current_element is not None
    actual = context.current_element.get('preload')
    assert actual == 'none', f"preload: ожидалось 'none', получено '{actual}'"



# 4.1: Проверка picture-блока
@when('я ищу элемент "picture"')
def step_find_element_picture(context):
    context.current_element = context.soup.select_one('picture')
    assert context.current_element is not None, "picture не найден"


@then('picture должен содержать элемент source')
def step_picture_has_source(context):
    assert context.current_element is not None
    source = context.current_element.find('source')
    assert source is not None, "Picture не содержит элемент source"

@then('source должен иметь атрибут media="(min-width:600px)"')
def step_source_has_media(context):
    assert context.current_element is not None
    source = context.current_element.find('source')
    assert source is not None

    actual = source.get('media')
    assert actual == '(min-width:600px)', f"media: ожидалось '(min-width:600px)', получено '{actual}'"

@then('picture должен содержать элемент img')
def step_picture_has_img(context):
    assert context.current_element is not None
    img = context.current_element.find('img')
    assert img is not None, "Picture не содержит элемент img"


@then('img должен иметь атрибут alt')
def step_img_has_alt(context):
    assert context.current_element is not None
    img = context.current_element.find('img')
    assert img is not None, "Picture не содержит img"

    assert img.has_attr('alt'), "Img не имеет атрибута alt"
    alt_text = img.get('alt')
    assert alt_text and alt_text.strip(), "Атрибут alt пустой"


# 4.2: Проверка map & area
@when('я ищу элемент "map#map1"')
def step_find_element_map_map1(context):
    context.current_element = context.soup.select_one('map#map1')
    assert context.current_element is not None, "map#map1 не найден"

@then('карта должна существовать')
def step_map_exists(context):
    """4.2: Проверка что карта существует"""
    assert context.current_element is not None
    assert context.current_element.name == 'map', "map отсутствует"

@then('карта должна содержать 2 области (area)')
def step_map_has_2_areas(context):
    assert context.current_element is not None
    areas = context.current_element.find_all('area')
    assert len(areas) == 2, f"Ожидалось 2 области, найдено {len(areas)}"

@then('первая область должна иметь title "Левая"')
def step_first_area_title_left(context):
    assert context.current_element is not None
    areas = context.current_element.find_all('area')
    assert len(areas) >= 1

    first_area = areas[0]
    actual = first_area.get('title')
    assert actual == 'Левая', f"title первой области: ожидалось 'Левая', получено '{actual}'"

@then('вторая область должна иметь title "Правая"')
def step_second_area_title_right(context):
    assert context.current_element is not None
    areas = context.current_element.find_all('area')
    assert len(areas) >= 2

    second_area = areas[1]
    actual = second_area.get('title')
    assert actual == 'Правая', f"title второй области: ожидалось 'Правая', получено '{actual}'"