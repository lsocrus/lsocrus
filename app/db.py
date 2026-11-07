# app/db.py
import aiosqlite
from app.config import cfg

SCHEMA = """
CREATE TABLE IF NOT EXISTS offers (
    id          TEXT PRIMARY KEY,
    sender_id   INTEGER NOT NULL,
    target_id   INTEGER,
    nft_url     TEXT NOT NULL,
    price       INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending', -- pending|accepted|rejected|expired
    created_at  INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    decided_at  INTEGER
);
CREATE INDEX IF NOT EXISTS idx_offers_sender ON offers(sender_id);
CREATE INDEX IF NOT EXISTS idx_offers_target ON offers(target_id);
CREATE INDEX IF NOT EXISTS idx_offers_status ON offers(status);

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY,
    username    TEXT,
    first_seen  INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);
"""

async def init_db():
    async with aiosqlite.connect(cfg.db_path) as db:
        await db.executescript(SCHEMA)
        await db.commit()

async def upsert_user(user_id: int, username: str | None):
    async with aiosqlite.connect(cfg.db_path) as db:
        await db.execute(
            "INSERT INTO users(id, username) VALUES(?, ?) "
            "ON CONFLICT(id) DO UPDATE SET username=excluded.username",
            (user_id, username),
        )
        await db.commit()

async def create_offer(offer_id: str, sender_id: int, nft_url: str,
                       price: int, target_id: int | None = None):
    async with aiosqlite.connect(cfg.db_path) as db:
        await db.execute(
            "INSERT INTO offers(id, sender_id, target_id, nft_url, price) "
            "VALUES(?, ?, ?, ?, ?)",
            (offer_id, sender_id, target_id, nft_url, price),
        )
        await db.commit()

async def get_offer(offer_id: str) -> dict | None:
    async with aiosqlite.connect(cfg.db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM offers WHERE id=?", (offer_id,)) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None

async def decide_offer(offer_id: str, status: str) -> bool:
    """Атомарно меняет статус только если он pending. True — если переключили."""
    async with aiosqlite.connect(cfg.db_path) as db:
        cur = await db.execute(
            "UPDATE offers SET status=?, decided_at=strftime('%s','now') "
            "WHERE id=? AND status='pending'",
            (status, offer_id),
        )
        await db.commit()
        return cur.rowcount > 0