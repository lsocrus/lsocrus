# app/keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def offer_kb(offer_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"acc:{offer_id}"),
        InlineKeyboardButton(text="❌ Отклонить",  callback_data=f"rej:{offer_id}"),
    ]])