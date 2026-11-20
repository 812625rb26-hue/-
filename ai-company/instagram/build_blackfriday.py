#!/usr/bin/env python3
"""Black Friday 2026 carousel builder (template method + official photos).
Facts verified 2026-11-20 against KONAMI official campaign page
https://www.konami.com/efootball/en/topic/promotion/campaign/947/
and Steam official news (KONAMI). 1080x1440, 5 pages.
Photos: official KONAMI key visuals (Steam CDN) - see package md for sources.
No player names/ratings are printed in text; card images are used as-is.
The Highlight card ratings visible inside the official image (94/93) are
KONAMI's 'highest possible rating' examples (per the visual's own footnote)
and are NOT stated in the post text."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1440
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
OUT = os.path.expanduser("~/workspace/goals/ai/files/blackfriday-images")
os.makedirs(OUT, exist_ok=True)
TMP = "/tmp"

GOLD = (255, 196, 64)
GOLD_SOFT = (255, 224, 138)
WHITE = (255, 255, 255)
MUTED = (203, 196, 200)
DARK = (8, 6, 10)

def font(size):
    return ImageFont.truetype(FONT, size, index=0)

def bg():
    img = Image.new("RGB", (W, H), DARK)
    px = img.load()
    top = (26, 18, 8)
    bottom = (5, 4, 8)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(0, W, 4):
            for dx in range(4):
                px[x + dx, y] = c
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([W - 430, -230, W + 170, 370], fill=(255, 196, 64, 40))
    d.ellipse([-270, H - 430, 330, H + 170], fill=(255, 196, 64, 26))
    return Image.alpha_composite(img.convert("RGBA"), ov)

def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]

def fit_font(d, s, start, min_size, max_w):
    size = start
    while size > min_size and text_w(d, s, font(size)) > max_w:
        size -= 4
    return font(size)

def center(d, s, f, y, fill):
    w = text_w(d, s, f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)
    return y + f.size

def left(d, s, f, x, y, fill):
    d.text((x, y), s, font=f, fill=fill)

def footer(d, page):
    f = font(34)
    d.text((48, H - 84), "ひとこと日和", font=f, fill=MUTED)
    s = f"{page} / 5"
    d.text((W - 48 - text_w(d, s, f), H - 84), s, font=f, fill=MUTED)

def pill(d, label, y, outline=GOLD, fill=None, text_fill=WHITE, start=64):
    f = fit_font(d, label, start, 36, W - 240)
    w = text_w(d, label, f)
    x = (W - w) / 2
    d.rounded_rectangle([x - 40, y - 16, x + w + 40, y + f.size + 28], radius=30,
                        outline=outline, width=5, fill=fill)
    d.text((x, y), label, font=f, fill=text_fill)
    return y + f.size + 80

def paste_cover(img, src, box, border=GOLD):
    """Paste a photo into box (x, y, w, h) cropped to fill, with gold border."""
    x, y, w, h = box
    ph = Image.open(src).convert("RGB")
    sw, sh = ph.size
    scale = max(w / sw, h / sh)
    ph = ph.resize((int(sw * scale) + 1, int(sh * scale) + 1), Image.LANCZOS)
    left_x = (ph.width - w) // 2
    top_y = (ph.height - h) // 2
    ph = ph.crop((left_x, top_y, left_x + w, top_y + h))
    img.paste(ph, (x, y))
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=border, width=6)

# Official photos (downloaded from Steam CDN, KONAMI official news)
KEYVISUAL = f"{TMP}/bf_keyvisual.png"      # BLACK FRIDAY Campaign key visual
HENRY_CARD = f"{TMP}/henry_card.png"       # Big Time & Epic: Arsenal FC key visual

# Pre-crop the card strip and platinum area from the key visual
kv = Image.open(KEYVISUAL).convert("RGB")
kv.crop((405, 122, 775, 222)).save(f"{TMP}/bf_cards_strip.png")   # 5 Highlight cards
kv.crop((28, 112, 398, 282)).save(f"{TMP}/bf_platinum.png")       # Platinum Ticket
hc = Image.open(HENRY_CARD).convert("RGB")
hc.crop((105, 168, 292, 405)).save(f"{TMP}/bf_henry_card.png")    # Henry Big Time card

# ---------- Page 1: cover ----------
img = bg(); d = ImageDraw.Draw(img)
center(d, "BLACK FRIDAY", fit_font(d, "BLACK FRIDAY", 118, 72, W - 100), 84, GOLD)
center(d, "開催中！", fit_font(d, "開催中！", 108, 64, W - 120), 224, WHITE)
paste_cover(img, KEYVISUAL, (48, 380, 984, 554))
center(d, "無料でもらえるものまとめ", fit_font(d, "無料でもらえるものまとめ", 76, 48, W - 110), 990, GOLD_SOFT)
center(d, "期間 11/12 〜 12/3 10:59まで", fit_font(d, "期間 11/12 〜 12/3 10:59まで", 52, 40, W - 120), 1110, MUTED)
footer(d, 1)
img.convert("RGB").save(f"{OUT}/page1.png")

# ---------- Page 2: period ----------
img = bg(); d = ImageDraw.Draw(img)
pill(d, "期間", 96, outline=GOLD, fill=GOLD, text_fill=(24, 16, 4), start=72)
center(d, "11/12 〜 12/3", fit_font(d, "11/12 〜 12/3", 150, 90, W - 100), 290, GOLD)
center(d, "10:59まで", fit_font(d, "10:59まで", 96, 60, W - 120), 480, WHITE)
center(d, "ログインするだけでも", fit_font(d, "ログインするだけでも", 64, 44, W - 140), 660, WHITE)
center(d, "もらえるものがあるよ", fit_font(d, "もらえるものがあるよ", 64, 44, W - 140), 748, WHITE)
paste_cover(img, f"{TMP}/bf_henry_card.png", (390, 880, 300, 424))
footer(d, 2)
img.convert("RGB").save(f"{OUT}/page2.png")

# ---------- Page 3: login rewards + card designs ----------
img = bg(); d = ImageDraw.Draw(img)
pill(d, "ログインでもらえるもの（累計）", 96, outline=GOLD, start=56)
paste_cover(img, f"{TMP}/bf_cards_strip.png", (48, 250, 984, 266))
items = [
    ("「Highlight: Arsenal FC」", "抽選契約権 ×1"),
    ("スキル追加トークン ×2", None),
    ("ポジション適性トークン ×2", None),
    ("GP 110,000", None),
    ("経験値 60,000", None),
]
y = 590
for main, sub in items:
    f = fit_font(d, main, 62, 40, W - 180)
    left(d, "・", f, 84, y, GOLD)
    left(d, main, f, 140, y, WHITE)
    y += 78
    if sub:
        fs = fit_font(d, sub, 62, 40, W - 180)
        left(d, sub, fs, 140, y, WHITE)
        y += 78
center(d, "※期間中にログインするともらえるよ", fit_font(d, "※期間中にログインするともらえるよ", 44, 32, W - 160), 1200, MUTED)
footer(d, 3)
img.convert("RGB").save(f"{OUT}/page3.png")

# ---------- Page 4: Campaign Hub ----------
img = bg(); d = ImageDraw.Draw(img)
pill(d, "Campaign Hub", 96, outline=GOLD, start=60)
center(d, "試合をすると", fit_font(d, "試合をすると", 92, 60, W - 120), 290, WHITE)
center(d, "チケットがもらえる", fit_font(d, "チケットがもらえる", 92, 60, W - 120), 404, WHITE)
paste_cover(img, f"{TMP}/bf_platinum.png", (90, 560, 900, 414))
center(d, "プラチナチケットは", fit_font(d, "プラチナチケットは", 76, 48, W - 140), 1030, GOLD_SOFT)
center(d, "最大5,000コインのチャンス！", fit_font(d, "最大5,000コインのチャンス！", 72, 44, W - 120), 1122, GOLD)
center(d, "（当たるかは運しだい）", fit_font(d, "（当たるかは運しだい）", 50, 36, W - 160), 1230, MUTED)
footer(d, 4)
img.convert("RGB").save(f"{OUT}/page4.png")

# ---------- Page 5: additions + closing ----------
img = bg(); d = ImageDraw.Draw(img)
pill(d, "追加情報", 96, outline=GOLD, fill=GOLD, text_fill=(24, 16, 4), start=72)
center(d, "11/19と11/26に", fit_font(d, "11/19と11/26に", 92, 60, W - 120), 300, WHITE)
center(d, "新しい目標とイベントが", fit_font(d, "新しい目標とイベントが", 76, 48, W - 120), 430, GOLD_SOFT)
center(d, "追加されるよ！", fit_font(d, "追加されるよ！", 76, 48, W - 120), 528, GOLD_SOFT)
center(d, "Team Effort は 11/19から", fit_font(d, "Team Effort は 11/19から", 68, 44, W - 140), 700, WHITE)
center(d, "English Clubs は 11/26から", fit_font(d, "English Clubs は 11/26から", 68, 44, W - 140), 800, WHITE)
center(d, "ログインだけでも忘れずに！", fit_font(d, "ログインだけでも忘れずに！", 68, 44, W - 140), 960, GOLD)
center(d, "みんなはもうログインした？", fit_font(d, "みんなはもうログインした？", 64, 44, W - 140), 1120, WHITE)
footer(d, 5)
img.convert("RGB").save(f"{OUT}/page5.png")

print("done")
for i in range(1, 6):
    im = Image.open(f"{OUT}/page{i}.png")
    print(f"page{i}: {im.size}")
