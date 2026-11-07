# app/models.py
from dataclasses import dataclass

@dataclass
class Offer:
    id: str
    sender_id: int
    target_id: int | None
    nft_url: str
    price: int
    status: str

    @classmethod
    def from_row(cls, row: dict) -> "Offer":
        return cls(
            id=row["id"], sender_id=row["sender_id"], target_id=row["target_id"],
            nft_url=row["nft_url"], price=row["price"], status=row["status"],
        )