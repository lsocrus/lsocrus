# app/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    token: str
    db_path: str
    price_stars: int
    throttle_rate: float

cfg = Config(
    token=os.getenv("BOT_TOKEN", ""),
    db_path=os.getenv("DB_PATH", "offers.db"),
    price_stars=int(os.getenv("PRICE_STARS", "25")),
    throttle_rate=float(os.getenv("THROTTLE_RATE", "1.5")),
)