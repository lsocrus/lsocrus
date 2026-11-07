# app/handlers/__init__.py
from aiogram import Router
from . import user, offer

def setup_handlers(dp):
    root = Router()
    root.include_router(user.router)
    root.include_router(offer.router)
    dp.include_router(root)