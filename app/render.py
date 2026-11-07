# app/render.py
import io
from PIL import Image, ImageDraw, ImageFont

def _fonts():
    try:
        return (ImageFont.truetype("DejaVuSans-Bold.ttf", 34),
                ImageFont.truetype("DejaVuSans.ttf", 22),
                ImageFont.truetype("DejaVuSans.ttf", 18))
    except Exception:
        f = ImageFont.load_default()
        return f, f, f

def make_offer_card(nft_url: str, price: int) -> bytes:
    W, H = 720, 420
    img = Image.new("RGB", (W, H), (14, 16, 22))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([10, 10, W-10, H-10], radius=22, outline=(60, 180, 255), width=3)
    fl, fm, fs = _fonts()
    d.text((34, 34),  "NFT OFFER", fl, fill=(90, 200, 255))
    d.text((34, 90),  "Вам поступило предложение:", fm, fill=(230, 230, 230))
    short = nft_url if len(nft_url) <= 62 else nft_url[:59] + "..."
    d.text((34, 140), short, fs, fill=(150, 200, 255))
    d.rounded_rectangle([34, 210, 260, 280], radius=14, fill=(30, 90, 160))
    d.text((60, 225), f"{price} ⭐", fl, fill=(255, 255, 255))
    d.text((290, 232), "за этот NFT", fm, fill=(200, 200, 200))
    d.text((34, 330), "Подтвердите или отклоните оффер ↓", fs, fill=(120, 120, 120))
    buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()