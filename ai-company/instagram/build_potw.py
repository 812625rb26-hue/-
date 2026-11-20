#!/usr/bin/env python3
"""POTW National carousel builder v2 (template method, no Canva).
Text is drawn with PIL so names/ratings are exact. 1080x1440 per page.
v2 fixes: position labels now stay inside the row band; page 4 uses
compact rows so all three fit above the footer."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1440
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
OUT = os.path.expanduser("~/workspace/goals/ai/files/potw-images")
os.makedirs(OUT, exist_ok=True)

GREEN = (0, 230, 118)
GREEN_SOFT = (105, 240, 174)
WHITE = (255, 255, 255)
MUTED = (196, 222, 208)
DARK = (3, 20, 13)

def font(size):
    return ImageFont.truetype(FONT, size, index=0)

def bg():
    img = Image.new("RGB", (W, H), DARK)
    px = img.load()
    top = (6, 42, 27)
    bottom = (2, 13, 8)
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(0, W, 4):
            for dx in range(4):
                px[x + dx, y] = c
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.ellipse([W - 420, -220, W + 160, 360], fill=(0, 230, 118, 36))
    d.ellipse([-260, H - 420, 320, H + 160], fill=(0, 230, 118, 28))
    d.text((W - 330, 120), "?", font=font(560), fill=(255, 255, 255, 16))
    d.text((40, H - 620), "?", font=font(420), fill=(255, 255, 255, 12))
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

def header(d, label, y=110):
    f = fit_font(d, label, 92, 60, W - 160)
    w = text_w(d, label, f)
    x = (W - w) / 2
    d.rounded_rectangle([x - 36, y - 18, x + w + 36, y + f.size + 30], radius=28,
                        outline=GREEN, width=5)
    d.text((x, y), label, font=f, fill=WHITE)
    return y + f.size + 90

def player_row(d, name, pos, rating, y, name_size=100):
    """Band height 208: name on line 1, position on line 2, both inside."""
    d.rounded_rectangle([56, y, W - 56, y + 208], radius=30, fill=(0, 0, 0, 96),
                        outline=(0, 230, 118, 120), width=3)
    nf = fit_font(d, name, name_size, 56, 540)
    d.text((96, y + 22), name, font=nf, fill=WHITE)
    pf = font(42)
    d.text((98, y + 22 + nf.size + 8), pos, font=pf, fill=GREEN_SOFT)
    rf = font(118)
    s = str(rating)
    d.text((W - 96 - text_w(d, s, rf), y + 40), s, font=rf, fill=GREEN)
    return y + 208 + 36

def compact_row(d, name, pos, rating, y):
    """Band height 150: name and position on one line."""
    d.rounded_rectangle([56, y, W - 56, y + 150], radius=26, fill=(0, 0, 0, 96),
                        outline=(0, 230, 118, 120), width=3)
    nf = fit_font(d, name, 80, 52, 520)
    d.text((96, y + 32), name, font=nf, fill=WHITE)
    pf = font(42)
    d.text((96 + text_w(d, name, nf) + 26, y + 62), pos, font=pf, fill=GREEN_SOFT)
    rf = font(100)
    s = str(rating)
    d.text((W - 96 - text_w(d, s, rf), y + 22), s, font=rf, fill=GREEN)
    return y + 150 + 26

# ---------- Page 1: cover ----------
img = bg(); d = ImageDraw.Draw(img)
center(d, "POTW National", fit_font(d, "POTW National", 118, 70, W - 120), 110, GREEN)
center(d, "来た！", font(290), 280, WHITE)
center(d, "目玉はハーランド", fit_font(d, "目玉はハーランド", 108, 64, W - 120), 690, WHITE)
center(d, "総合値", font(68), 838, MUTED)
center(d, "98", font(270), 908, GREEN)
d.rounded_rectangle([W/2 - 210, 1252, W/2 + 210, 1344], radius=46, fill=GREEN)
s = "11/26まで"
sf = font(58)
d.text(((W - text_w(d, s, sf)) / 2, 1266), s, font=sf, fill=(2, 26, 15))
footer(d, 1)
img.convert("RGB").save(f"{OUT}/page1.png")

# ---------- Page 2: top 3 ----------
img = bg(); d = ImageDraw.Draw(img)
y = header(d, "目玉3人")
y = player_row(d, "ハーランド", "CF", 98, y, 104)
y = player_row(d, "サラー", "RWF", 96, y, 104)
y = player_row(d, "ドク", "LMF", 96, y, 104)
footer(d, 2)
img.convert("RGB").save(f"{OUT}/page2.png")

# ---------- Page 3: others ----------
img = bg(); d = ImageDraw.Draw(img)
y = header(d, "他の収録選手")
y = player_row(d, "コンサ", "CB", 95, y, 96)
y = player_row(d, "ラインデルス", "AMF", 95, y, 96)
y = player_row(d, "ホイルンド", "CF", 94, y, 96)
y = player_row(d, "プリシッチ", "AMF", 94, y, 96)
footer(d, 3)
img.convert("RGB").save(f"{OUT}/page3.png")

# ---------- Page 4: Nakamura + compact rows ----------
img = bg(); d = ImageDraw.Draw(img)
header(d, "日本代表もいる！")
center(d, "中村敬斗", fit_font(d, "中村敬斗", 156, 100, W - 120), 310, WHITE)
center(d, "LWF", font(58), 492, GREEN_SOFT)
center(d, "93", font(200), 566, GREEN)
y = 806
y = compact_row(d, "スヴェンソン", "RB", 93, y)
y = compact_row(d, "グルダ", "RMF", 93, y)
y = compact_row(d, "シュラーガー", "GK", 92, y)
footer(d, 4)
img.convert("RGB").save(f"{OUT}/page4.png")

# ---------- Page 5: closing ----------
img = bg(); d = ImageDraw.Draw(img)
center(d, "誰狙う？", font(190), 220, WHITE)
center(d, "ハーランド？ サラー？", fit_font(d, "ハーランド？ サラー？", 96, 60, W - 120), 560, WHITE)
center(d, "それとも中村敬斗？", fit_font(d, "それとも中村敬斗？", 96, 60, W - 120), 700, GREEN_SOFT)
d.rounded_rectangle([W/2 - 330, 960, W/2 + 330, 1080], radius=56, outline=GREEN, width=5)
s = "コメントで教えて！"
sf = fit_font(d, s, 64, 44, 600)
d.text(((W - text_w(d, s, sf)) / 2, 984), s, font=sf, fill=WHITE)
center(d, "期間は11/26まで", font(52), 1180, MUTED)
footer(d, 5)
img.convert("RGB").save(f"{OUT}/page5.png")

print("done")
