# app/services/stars.py
# Заглушка «эмиссии» 25 звёзд. В проде — Stars invoice / transfer через Bot API.
from app.config import cfg

async def credit_stars(user_id: int, amount: int, reason: str) -> bool:
    # здесь: запись в ledger, вызов sendInvoice с currency='XTR' и т.п.
    print(f"[stars] credit user={user_id} amount={amount} reason={reason}")
    return True