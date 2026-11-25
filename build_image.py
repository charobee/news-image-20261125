#!/usr/bin/env python3
"""Build entry.png for make.fun bounty 'Sum up 25 November's world news in one image'.

News verified 2026-11-26 JST from Just Security Early Edition 25 Nov 2026,
SCMP world headlines 25 Nov 2026, and the 25 Nov evening news roundup.
Deterministic: same input -> same bytes (no timestamps, no randomness).
Output: 1024x1024 PNG, well under the 1 MiB limit.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (179, 38, 30)
GREY = (90, 86, 78)
LINE = (17, 17, 17)
ACCENT = (27, 67, 110)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, w, kicker, headline, deck, hsize=34, dsize=21):
    draw.text((x, y), kicker, font=font(SANS_B, 20), fill=RED)
    y += 30
    hl = font(SERIF_B, hsize)
    for ln in wrap(draw, headline, hl, w):
        draw.text((x, y), ln, font=hl, fill=INK)
        y += hsize + 6
    y += 4
    df = font(SANS, dsize)
    for ln in wrap(draw, deck, df, w):
        draw.text((x, y), ln, font=df, fill=GREY)
        y += dsize + 7
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 118], fill=INK)
d.text((36, 22), "THE WORLD IN ONE IMAGE", font=font(SERIF_B, 52), fill=(247, 243, 234))
d.text((36, 82), "WEDNESDAY  25  NOVEMBER  2026", font=font(SANS_B, 22),
       fill=(212, 175, 55))
d.text((700, 82), "8 STORIES  ·  1 DAY", font=font(SANS_B, 22), fill=(247, 243, 234))

# ---- hero: Hormuz ----
y = draw_block(
    d, 36, 140, 952,
    "1  ·  STRAIT OF HORMUZ",
    "Two oil tankers hit mines and catch fire",
    "Iran's Revolutionary Guard says the tankers struck naval mines while using an "
    "unauthorised route through the strait, the world's most important oil chokepoint.",
    hsize=46, dsize=24)
d.line([36, y + 14, 988, y + 14], fill=INK, width=3)

# ---- grid 2x2 ----
gy = y + 34
col_w, gap = 464, 24
x2 = 36 + col_w + gap
row_h = 252

def panel(x, yy, num, kicker, headline, deck):
    draw_block(d, x, yy, col_w, f"{num}  ·  {kicker}", headline, deck,
               hsize=32, dsize=20)

panel(36, gy, "2", "RIYADH & THE GULF",
      "Houthis strike Saudi refinery and a Riyadh tower",
      "Attacks hit the Ras Tanura refinery and a skyscraper in the capital; 11 people were hurt.")
panel(x2, gy, "3", "GAZA",
      "Israeli strike kills Hamas security chief",
      "Mohammad Abuelouf, his wife and two children were killed in Gaza City, medics said.")
panel(36, gy + row_h, "4", "UKRAINE",
      "Drones set two Russian refineries ablaze",
      "Ukraine hit Rosneft plants in Samara overnight; a Russian strike on Odesa killed two.")
panel(x2, gy + row_h, "5", "MARKETS",
      "Asia tumbles; Dow tops 50,000 for the first time",
      "KOSPI -6.2%, Nikkei -2.8% as chip stocks fell; the Dow closed above 50,000.")

fy = gy + 2 * row_h + 6
d.line([36, fy, 988, fy], fill=INK, width=3)
# ---- footer strip: 3 mini stories ----
fy += 18
fw = 304
fxs = [36, 36 + fw + 20, 36 + 2 * (fw + 20)]
minis = [
    ("6 · TECH", "Huawei convicted", "US jury finds Huawei guilty on 10 counts, incl. bank fraud."),
    ("7 · SPACE", "Shenzhou-24 docks", "Shenzhou-24 docks at Tiangong with Pakistan's first astronaut."),
    ("8 · PACIFIC", "Solomons pact signed", "Australia–Solomons treaty bars any foreign military base in the islands."),
]
for fx, (kick, head, deck) in zip(fxs, minis):
    d.text((fx, fy), kick, font=font(SANS_B, 18), fill=RED)
    d.text((fx, fy + 26), head, font=font(SERIF_B, 23), fill=INK)
    df = font(SANS, 16)
    yy = fy + 58
    for ln in wrap(d, deck, df, fw)[:2]:
        d.text((fx, yy), ln, font=df, fill=GREY)
        yy += 22

# ---- source line ----
d.text((36, 1001), "Sources: Just Security Early Edition · SCMP · AP — 25 Nov 2026",
       font=font(SANS, 15), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
