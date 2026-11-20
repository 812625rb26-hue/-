#!/usr/bin/env python3
"""Show Time Madrid Chamartin B carousel builder (template method, no Canva).
Text is drawn with PIL so names/ratings are exact. 1080x1440 per page.
The end date is unverified, so no end date is drawn anywhere; the pack is
labelled only as 開催中 (now on)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1440
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
OUT = os.path.expanduser("~/workspace/goals/ai/files/showtime-images")
os.makedirs(OUT, exist_ok=True)

GOLD = (255, 196, 64)
GOLD_SOFT = (255, 224, 138)
PURPLE = (168, 85, 247)
WHITE = (255, 255, 255)
MUTED = (203, 196, 232)
DARK = (7, 6, 24)

def font(size):
    return ImageFont.truetype(FONT, size, index=0)

def bg(watermark="ST"):
    img = Image.new("RGB", (W, H), DARK)
    px = img.load()
    top = (24, 16, 58)
    bottom = (4, 3, 14)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(0, W, 4):
            for dx in range(4):
                px[x + dx, y] = c
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([W - 430, -230, W + 170, 370], fill=(168, 85, 247, 42))
    d.ellipse([-270, H - 430, 330, H + 170], fill=(255, 196, 64, 30))
    d.text((W - 430, 130), watermark, font=font(430), fill=(255, 255, 255, 13))
    d.text((30, H - 560), watermark, font=font(330), fill=(255, 255, 255, 9))
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

def footer(d, page):
    f = font(34)
    d.text((48, H - 84), "ひとこと日和", font=f, fill=MUTED)
    s = f"{page} / 5"
    d.text((W - 48 - text_w(d, s, f), H - 84), s, font=f, fill=MUTED)

def pill(d, label, y, outline=GOLD, fill=None, text_fill=WHITE, start=64):
    f = fit_font(d, label, start, 40, W - 240)
    w = text_w(d, label, f)
    x = (W - w) / 2
    d.rounded_rectangle([x - 40, y - 16, x + w + 40, y + f.size + 28], radius=30,
                        outline=outline, width=5, fill=fill)
    d.text((x, y), label, font=f, fill=text_fill)
    return y + f.size + 80

# ---------- Page 1: cover ----------
img = bg(); d = ImageDraw.Draw(img)
center(d, "Show Time", fit_font(d, "Show Time", 124, 76, W - 120), 120, GOLD)
center(d, "マドリード・", fit_font(d, "マドリード・", 118, 70, W - 120), 330, WHITE)
center(d, "シャマルティンB！", fit_font(d, "シャマルティンB！", 118, 70, W - 120), 480, WHITE)
center(d, "若手3人が登場", fit_font(d, "若手3人が登場", 108, 64, W - 120), 700, GOLD_SOFT)
pill(d, "開催中", 950, outline=GOLD, fill=GOLD, text_fill=(24, 16, 4), start=72)
center(d, "11/16 登場", font(52), 1140, MUTED)
footer(d, 1)
img.convert("RGB").save(f"{OUT}/page1.png")

# ---------- Pages 2-4: one player each ----------
players = [
    (2, "ヤン・ディオマンデ", "RWF", 100),
    (3, "エンドリッキ", "CF", 100),
    (4, "カルロス・エスピ", "CF", 99),
]
for page, name, pos, rating in players:
    img = bg("ST"); d = ImageDraw.Draw(img)
    pill(d, "Show Time", 96, outline=PURPLE, start=58)
    center(d, name, fit_font(d, name, 124, 64, W - 110), 330, WHITE)
    pf = font(76)
    pw = text_w(d, pos, pf)
    px = (W - pw) / 2
    d.rounded_rectangle([px - 44, 520, px + pw + 44, 520 + pf.size + 34], radius=30,
                        fill=(168, 85, 247, 70), outline=PURPLE, width=4)
    d.text((px, 534), pos, font=pf, fill=WHITE)
    center(d, "総合値", font(64), 730, MUTED)
    center(d, str(rating), font(300), 812, GOLD)
    center(d, "マドリード・シャマルティンB", fit_font(d, "マドリード・シャマルティンB", 50, 36, W - 160), 1210, MUTED)
    footer(d, page)
    img.convert("RGB").save(f"{OUT}/page{page}.png")

# ---------- Page 5: closing ----------
img = bg(); d = ImageDraw.Draw(img)
pill(d, "Show Time", 96, outline=PURPLE, start=58)
center(d, "3人とも", font(104), 250, WHITE)
center(d, "99〜100", font(220), 380, GOLD)
center(d, "若手アタッカー", fit_font(d, "若手アタッカー", 104, 64, W - 120), 660, GOLD_SOFT)
center(d, "11/16に登場した", fit_font(d, "11/16に登場した", 72, 48, W - 140), 900, WHITE)
center(d, "ガチャだよ", font(72), 996, WHITE)
center(d, "終了日はゲーム内で", fit_font(d, "終了日はゲーム内で", 54, 40, W - 140), 1160, MUTED)
center(d, "チェックしてね", font(54), 1232, MUTED)
footer(d, 5)
img.convert("RGB").save(f"{OUT}/page5.png")

print("done")
