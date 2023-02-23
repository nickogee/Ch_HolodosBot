from config import TOKEN
from keyboards_text import KEYBOARDS_TEXT_FUNC, TEXTS
from func_classes import UpdateBalance, WareHouses, WriteOff

import telebot.callback_data
import telebot

from telebot import types


def run_bot():
    bot = telebot.TeleBot(TOKEN)

    # Словарь будет хранить словари с текущим шагом и объектами для каждого юзера
    # id юзера - ключ к словарю с данными этого юзера
    users_step = {}

    bot.current_states.data = {}

    def find_selected_wh(wh_obj, selected_wh_name):

        for cur_dict in wh_obj.wh_dict_list:
            if cur_dict['Name'] == selected_wh_name:
                wh_obj.selected_wh = cur_dict
                break
        return None

    def split_catalog_list(markup, catalog_list):

        while len(catalog_list) > 0:

            if len(catalog_list) >= 4:
                btn1, btn2, btn3, btm4 = types.KeyboardButton(catalog_list.pop()), \
                                        types.KeyboardButton(catalog_list.pop()), \
                                        types.KeyboardButton(catalog_list.pop()), \
                                        types.KeyboardButton(catalog_list.pop())

                markup.add(btn1, btn2, btn3, btm4)

            elif len(catalog_list) == 3:
                btn1, btn2, btn3 = types.KeyboardButton(catalog_list.pop()), \
                    types.KeyboardButton(catalog_list.pop()), \
                    types.KeyboardButton(catalog_list.pop())

                markup.add(btn1, btn2, btn3)

            elif len(catalog_list) == 2:
                btn1, btn2 = types.KeyboardButton(catalog_list.pop()), \
                    types.KeyboardButton(catalog_list.pop())

                markup.add(btn1, btn2)

            else:
                btn1 = types.KeyboardButton(catalog_list.pop())
                markup.add(btn1)

        return

    def prev_step(message):
        return users_step[message.from_user.id]

    # шаг 0 - /start
    @bot.message_handler(commands=['start'])
    def start(message):
        nonlocal users_step

        users_step[message.from_user.id] = '0'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton(TEXTS['begin'])
        markup.add(btn1)
        bot.send_message(message.from_user.id, TEXTS['start'], reply_markup=markup)

    # Шаг 1. Пришло приветствие - выбор склада
    @bot.message_handler(content_types=['text'], func=lambda message: message.text == TEXTS['begin'] or \
                                                                      message.text == KEYBOARDS_TEXT_FUNC['back_to_start'][0])
    def select_wh(message):
        nonlocal users_step

        users_step[message.from_user.id] = '1'

        wh_obj = WareHouses()

        # Получим склады Микромаркета из 1С
        wh_obj.get_response()

        # Для текущего юзера будем записывать шаг, на котором он находится, и объекты взаимодействия с 1с
        user_dict = bot.current_states.data
        user_dict[message.from_user.id] = {}
        user_dict[message.from_user.id]['wh_obj'] = wh_obj

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
        if wh_obj.wh_name_list:
            split_catalog_list(markup, wh_obj.wh_name_list.copy())
            bot.send_message(message.from_user.id, TEXTS['select_wh'], reply_markup=markup)
        else:
            btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
            markup.add(btn_back)
            bot.send_message(message.from_user.id, TEXTS['error_wh'], reply_markup=markup)

    # Шаг 2. Пришел выбранный склад - выбор сценария
    @bot.message_handler(content_types=['text'], func=lambda message: prev_step(message) == '1')
    def select_scenario(message):
        nonlocal users_step

        users_step[message.from_user.id] = '2'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        wh_obj = user_dict[message.from_user.id]['wh_obj']

        # Уставновим выбранный склад в атрибут объекта
        find_selected_wh(wh_obj, message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)

        btn1 = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['update_balances'][0])
        btn2 = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['write_off_goods'][0])
        btn3 = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['inventory'][0])
        markup.add(btn1, btn2, btn3)

        btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
        markup.add(btn_back)

        bot.send_message(message.from_user.id, TEXTS['select_skript'], reply_markup=markup)

    ######################################## Обновить остатки #######################################

    # Шаг 3.1. Пришел выбранный сценарий - update_balances
    @bot.message_handler(content_types=['text'], func=lambda message: message.text == KEYBOARDS_TEXT_FUNC['update_balances'][0])
    def start_update_balances(message):
        nonlocal users_step

        users_step[message.from_user.id] = '3.1'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        wh_obj = user_dict[message.from_user.id]['wh_obj']

        update_balance = UpdateBalance()

        update_balance.selected_wh = wh_obj.selected_wh
        result = update_balance.get_response()

        # Поместим update_balance в данные юзера
        user_dict[str(message.from_user.id)]['update_balance'] = update_balance

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
        btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
        markup.add(btn_back)
        bot.send_message(message.from_user.id, result, reply_markup=markup)

    ######################################## Списание товара #######################################

    # Шаг 3.2. Пришел выбранный сценарий write_off_goods - выбираем категорию товара
    @bot.message_handler(content_types=['text'], func=lambda message: message.text == KEYBOARDS_TEXT_FUNC['write_off_goods'][0])
    def select_category(message):
        nonlocal users_step

        users_step[message.from_user.id] = '3.2'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        wh_obj = user_dict[message.from_user.id]['wh_obj']

        write_off = WriteOff()

        write_off.selected_wh = wh_obj.selected_wh
        write_off.get_response()
        write_off.set_category_list()

        # Поместим write_off в данные юзера
        user_dict[message.from_user.id]['write_off'] = write_off

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=4)
        if write_off.category_list:
            split_catalog_list(markup, write_off.category_list.copy())
            btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
            markup.add(btn_back)
            bot.send_message(message.from_user.id, TEXTS['select_category'], reply_markup=markup)

        else:
            btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
            markup.add(btn_back)
            bot.send_message(message.from_user.id, TEXTS['error_category'], reply_markup=markup)

    # Шаг 3.2.1 Пришла выбранная категория - выбираем товар
    @bot.message_handler(content_types=['text'], func=lambda message: prev_step(message) == '3.2')
    def select_write_off_goods(message):
        nonlocal users_step

        users_step[message.from_user.id] = '3.2.1'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        write_off = user_dict[message.from_user.id]['write_off']

        write_off.set_goods_lists(category_name=message.text)

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=4)
        if write_off.goods_name_list:
            split_catalog_list(markup, write_off.goods_name_list.copy())

            btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
            markup.add(btn_back)
            bot.send_message(message.from_user.id, TEXTS['select_goods'], reply_markup=markup)

        else:
            btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
            markup.add(btn_back)
            bot.send_message(message.from_user.id, TEXTS['error_goods'], reply_markup=markup)

    # Шаг 3.2.2 Пришел выбранный товар - просим отправить фото
    @bot.message_handler(content_types=['text'], func=lambda message: prev_step(message) == '3.2.1')
    def to_send_photo_write_off_goods(message):
        nonlocal users_step

        users_step[message.from_user.id] = '3.2.2'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        write_off = user_dict[message.from_user.id]['write_off']

        write_off.set_selected_good(message.text)

        bot.send_message(message.from_user.id, f'{TEXTS["send_photo"]}: \n{message.text}')

    # Шаг 3.2.3 Пришло фото товара - сохраняем фото, просим указать количество для списания
    @bot.message_handler(content_types=["photo"], func=lambda message: prev_step(message) == '3.2.2')
    def send_cunt_no_write_off(message):
        nonlocal users_step

        users_step[message.from_user.id] = '3.2.3'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        write_off = user_dict[message.from_user.id]['write_off']

        raw = message.photo[1].file_id
        name = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)

        write_off.save_photo(name=name, downloaded_file=downloaded_file)

        bot.send_message(message.from_user.id, f'{TEXTS["set_count"]}')

    # Шаг 3.2.4 Пришло количество товара для списания - проверяем количество, вызываем метод 1С, конец сценария
    @bot.message_handler(content_types=["text"], func=lambda message: prev_step(message) == '3.2.3')
    def send_cunt_no_write_off(message):
        nonlocal users_step

        if not message.text.isdigit():
            bot.send_message(message.from_user.id, TEXTS["error_not_num"])
        else:
            users_step[message.from_user.id] = '3.2.4'

            # Для текущего юзера будем записывать объекты взаимодействия с 1с
            user_dict = bot.current_states.data

            # Извлечем объект write_off из данных юзера
            write_off = user_dict[message.from_user.id]['write_off']

            # Извлечем объект wh_obj из данных юзера
            wh_obj = user_dict[message.from_user.id]['wh_obj']

            count = int(message.text)
            if write_off.selected_good['Count'] < count:
                users_step[message.from_user.id] = '3.2.3'
                bot.send_message(message.from_user.id, TEXTS['error_count'])
            else:
                # вызываем метод 1с
                result = write_off.post_write_off(wh_obj.selected_wh['GUID'], count)

                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

                btn_back = types.KeyboardButton(KEYBOARDS_TEXT_FUNC['back_to_start'][0])
                markup.add(btn_back)
                bot.send_message(message.from_user.id, result, reply_markup=markup)

    ######################################## Инвентаризация #######################################

    # Шаг 3.3. Пришел выбранный сценарий inventory
    @bot.message_handler(content_types=['text'],
                         func=lambda message: message.text == KEYBOARDS_TEXT_FUNC['inventory'][0])
    def select_category(message):
        nonlocal users_step

        users_step[message.from_user.id] = '3.3'

        # Для текущего юзера будем записывать объекты взаимодействия с 1с
        user_dict = bot.current_states.data

        # Извлечем объект wh_obj из данных юзера
        wh_obj = user_dict[message.from_user.id]['wh_obj']








    bot.polling(none_stop=True, interval=3)


if __name__ == '__main__':
    run_bot()


