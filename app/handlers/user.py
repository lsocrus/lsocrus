# app/handlers/user.py
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.db import upsert_user
from app.config import cfg

router = Router()

@router.message(CommandStart())
async def start(m: Message):
    await upsert_user(m.from_user.id, m.from_user.username)
    await m.answer(
        "Кинь ссылку на NFT — сделаю оффер за "
        f"<b>{cfg.price_stars} ⭐</b>.\nФормат: <code>https://...</code>"
    )