from func_classes import *

TEXTS = {
    'start': 'Привет! 👻 Я твой бот-помощник!',
    'begin': '🗿 Начать',
    'wait': '🗿 Ждите...',
    'select_skript': 'Выберите действие',
    'select_wh': 'Выберите склад',
    'select_category': 'Выберите категорию',
    'select_goods': 'Выберите товар',
    'send_photo': 'Пришлите фото',
    'success_write_off': 'Списание прошло корректно.',
    'success_mark_z_up': 'Обновление заказов прошло корректно.',
    'set_count': 'Укажите количество для списания',
    'set_count_inv': 'Укажите количество в наличии:\n',
    'invent_category': 'Товыры по категории',
    'next_category': 'Следующая категория',
    'invent_done': 'Все товарные позиции проинвентаризированны.',
    # ERRORS
    'error_wh': 'В 1С не найдено ни одного склада Микромаркета',
    'error_category': 'В 1С не найдено ни одного товара на складе Микромаркета',
    'error_goods': 'Не найдено такого товара',
    'error_not_num': 'Укажите количество для списания - только цифры',
    'error_count': 'Указанное количество больше остатка товара',
}


KEYBOARDS_TEXT_FUNC = {
    'write_off_goods': ['♻ Списать товар'],
    'inventory': ['☑ Инвентаризация'],
    'update_balances': ['🔃 Обновить остатки'],
    'back_to_start': ['🔙 Вернуться в начало'],
    'ok': ['Далее'],
    'end_invent': ['Завершить инвентаризацию'],


}
