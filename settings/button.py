from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def promt_btn(chat_id, user_id):
    btn = [[InlineKeyboardButton(text="Нет", callback_data="No"),
            InlineKeyboardButton(text="Да", callback_data=f"{chat_id}-{user_id}")]]
    return InlineKeyboardMarkup(inline_keyboard=btn)
