from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import *


def send_contact_button():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Поделится контактом', request_contact=True)]
    ], resize_keyboard=True)


def generate_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Сделать заказ')],
        [KeyboardButton(text='История'), KeyboardButton(text='Карзина 🧺'), KeyboardButton(text='Настройки'),],
    ], resize_keyboard=True)


def generate_category_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    categories = get_all_categories()
    buttons = []
    for category in categories:
        btn = InlineKeyboardButton(text=category[1], callback_data=f'category_{category[0]}')
        buttons.append(btn)

    markup.add(*buttons)
    return markup


def generate_products_by_category(category_id):
    markup = InlineKeyboardMarkup(row_width=2)
    products = get_products_by_category_id(category_id)
    button = []
    for product in products:
        btn = InlineKeyboardButton(text=product[1], callback_data=f'product_{product[0]}')
        button.append(btn)
    markup.add(*button)
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data='back'),
        InlineKeyboardButton(text='Меню', callback_data='main_menu'),
        InlineKeyboardButton(text='Далее', callback_data='next')
    )
    return markup


def generate_product_detail_menu(product_id, category_id, cart_id, product_name='', c=0):
    markup = InlineKeyboardMarkup(row_width=3)
    try:
        quantity = get_quantity(cart_id, product_name)
    except:
        quantity = c

    buttons = []
    btn_back = InlineKeyboardButton(text=str('Назад'), callback_data=f'back_{quantity}_{product_id}')
    btn_quantity = InlineKeyboardButton(text=str(quantity), callback_data=f'coll')
    btn_next = InlineKeyboardButton(text=str('Далее'), callback_data=f'next_{quantity}_{product_id}')
    buttons.append(btn_back)
    buttons.append(btn_quantity)
    buttons.append(btn_next)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='Добавить в корзину', callback_data=f'cart_{product_id}_{quantity}')
    )
    markup.row(
        InlineKeyboardButton(text='Меню', callback_data=f'menu_{category_id}')
    )
    return markup


def generate_cart_menu(cart_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Оформить заказ', callback_data=f'order_{cart_id}')
    )
    cart_products = get_carts_products_for_delete(cart_id)
    for cart_product_id, product_name in cart_products:
        markup.row(
            InlineKeyboardButton(text=f'Удалить {product_name}', callback_data=f'delete_{cart_product_id}')
        )
    return markup
