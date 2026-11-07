# app/handlers/offer.py
import uuid
from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from app.db import create_offer, get_offer, decide_offer
from app.keyboards import offer_kb
from app.render import make_offer_card
from app.config import cfg
from app.services.stars import credit_stars
from app.models import Offer

router = Router()

@router.message(StateFilter(None), lambda m: m.text and m.text.startswith("http"))
async def on_link(m: Message, bot: Bot):
    url = m.text.strip().split()[0]
    offer_id = uuid.uuid4().hex[:12]
    await create_offer(offer_id, m.from_user.id, url, cfg.price_stars)
    png = make_offer_card(url, cfg.price_stars)
    await m.answer_photo(
        BufferedInputFile(png, "offer.png"),
        caption=(
            f"🪙 <b>NFT-оффер</b>\nЦена: <b>{cfg.price_stars} ⭐</b>\n"
            f"Ссылка: <a href=\"{url}\">{url[:40]}</a>\n"
            f"<i>ID: {offer_id}</i>"
        ),
        reply_markup=offer_kb(offer_id),
    )

@router.callback_query(lambda c: c.data and c.data.startswith(("acc:", "rej:")))
async def on_decision(cb: CallbackQuery, bot: Bot):
    action, offer_id = cb.data.split(":", 1)
    row = await get_offer(offer_id)
    if not row:
        await cb.answer("Оффер не найден.", show_alert=True); return
    new_status = "accepted" if action == "acc" else "rejected"
    if not await decide_offer(offer_id, new_status):
        await cb.answer("Оффер уже обработан.", show_alert=True); return

    offer = Offer.from_row(row)
    if new_status == "accepted":
        await credit_stars(offer.sender_id, offer.price, f"offer:{offer.id}")
        await cb.message.edit_caption(
            caption=f"✅ <b>Оффер принят</b>\n{offer.price} ⭐ зачислены\nNFT: {offer.nft_url}",
            reply_markup=None)
        await bot.send_message(offer.sender_id,
            f"💰 Оффер принят! {offer.price} ⭐ зачислены.\nNFT: {offer.nft_url}")
    else:
        await cb.message.edit_caption(
            caption=f"❌ <b>Оффер отклонён</b>\nNFT: {offer.nft_url}",
            reply_markup=None)
        await bot.send_message(offer.sender_id, "❌ Получатель отклонил оффер.")
    await cb.answer()