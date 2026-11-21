# draw.py - Variant E "THE GLOBAL WIRE" - News Image entry, Friday 20 Nov 2026.
# Wire-service monochrome: white page, ink black, grays, one red accent.
# Deterministic Pillow program (stdlib + PIL only, no network).
# Draws a 1024x1024 page and saves entry.png next to this file.
import os
from PIL import Image, ImageDraw, ImageFont
from mapdata import WORLD

BASE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(BASE, "fonts")


def PF(s):
    return ImageFont.truetype(os.path.join(FD, "PlayfairDisplay-900.ttf"), s)


def AB(s):
    return ImageFont.truetype(os.path.join(FD, "Archivo-Bold.ttf"), s)


def AM(s):
    return ImageFont.truetype(os.path.join(FD, "Archivo-Medium.ttf"), s)


INK = (17, 17, 17)
WHITE = (255, 255, 255)
LGRAY = (237, 237, 237)
MGRAY = (74, 74, 74)
GRAY2 = (198, 198, 198)
LAND = (207, 207, 207)
RED = (192, 57, 43)

REG = {
    "EUROPE": (176, 58, 46),
    "ASIA": (29, 111, 184),
    "MIDEAST": (125, 60, 152),
    "AFRICA": (30, 132, 73),
    "AMERICAS": (202, 111, 30),
    "OCEANIA": (20, 143, 119),
    "GLOBAL": (93, 109, 126),
}

W = H = 1024
M = 16            # page margin
CW = W - 2 * M    # content width = 992


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, maxw):
    """Greedy word wrap; returns list of lines that each fit maxw."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if tw(d, trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, s, maker, size, maxw, minsize=8):
    """Largest maker(size) font, stepping down, whose text fits maxw."""
    f = maker(size)
    while size > minsize and tw(d, s, f) > maxw:
        size -= 1
        f = maker(size)
    return f


def T(d, x, y, s, f, fill=INK, anchor="la"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def rule(d, x0, x1, y, fill=INK, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def vrule(d, x, y0, y1, fill=INK, wdt=1):
    d.line([(x, y0), (x, y1)], fill=fill, width=wdt)

# ---------------------------------------------------------------- data ----
NUMBERS = [
    ("3", "bridges over the Dnipro damaged in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-6.2%", "Taiwan's share index, Friday's close"),
    ("100,000", "youth visas a year in the UK-EU deal"),
    ("$120bn", "adaptation finance gap left open at COP31"),
    ("118", "runs by Glenn Phillips against India"),
]

TIMELINE = [
    ("Overnight", "Kyiv barrage: seven waves from 01:25 local"),
    ("02:30 UTC", "Cyclone Akvan makes landfall in Odisha"),
    ("06:00 UTC", "Tokyo close: Nikkei -5.1% in the AI sell-off"),
    ("Midday", 'Brussels: UK and EU seal the "reset" deal'),
    ("Evening", "Wellington: Phillips completes 118 vs India"),
]

REGION_COUNTS = [
    ("EUROPE", 9), ("ASIA", 10), ("MIDEAST", 3), ("AFRICA", 5),
    ("AMERICAS", 5), ("OCEANIA", 3), ("GLOBAL", 5),
]

# no, place, region, topic, headline, deck (verbatim + sources), source tag,
# data label, caption band, pin lon, pin lat
CARDS = [
    (1, "KYIV, UKRAINE", "EUROPE", "WAR",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of about 110 missiles and 400 drones killed at "
     "least nine people across Ukraine and cut power and water in the "
     "capital. (Kyiv Independent, BBC)",
     "Officials' count", "3 BRIDGES HIT", "KYIV - OVERNIGHT BARRAGE",
     30.5, 50.4),
    (2, "ODISHA, INDIA", "ASIA", "WEATHER",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am after more "
     "than 300,000 people were moved to shelters. No deaths were reported. "
     "(IMD, Deccan Herald)",
     "Weather office", "LANDFALL - 8 AM", "GOPALPUR, ODISHA - LANDFALL",
     84.9, 19.3),
    (3, "TAIPEI - SEOUL - TOKYO", "ASIA", "MARKETS",
     "AI sell-off sinks Asia's stock markets",
     "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul lost "
     "5.2% and Tokyo 5.1% as chipmakers led the slide. (Al Jazeera, Anadolu)",
     "Closing prices",
     "TAIPEI -6.2% - SEOUL -5.2%\nTOKYO -5.1% - HONG KONG -1.9%",
     "TAIPEI - SEOUL - TOKYO - CLOSING PRICES",
     121.0, 25.0),
    (4, "BRUSSELS", "EUROPE", "DIPLOMACY",
     'UK and EU seal a "reset" deal',
     "Food trade, youth visas, carbon link. The youth scheme alone covers "
     "100,000 visas a year. (Reuters)",
     "Agreed - Reuters", "AGREED", "BRUSSELS - THE RESET DEAL",
     4.3, 50.8),
    (5, "ANTALYA", "GLOBAL", "CLIMATE",
     "COP31 reaches its last day with no deal",
     "Draft text omits fossil fuels; a $120bn adaptation gap stays "
     "unresolved on the final day. (UN News)",
     "Ongoing - UN News", "NO DEAL - FINAL DAY", "ANTALYA - COP31 FINAL DAY",
     30.7, 36.9),
    (6, "EASTERN POLAND", "EUROPE", "WAR",
     "Russian cruise missile lands in Poland",
     "Fell in a field; two airports paused. It crossed during the Kyiv "
     "barrage, the minister said. (Reuters)",
     "Minister says - Reuters", "FELL IN A FIELD",
     "EASTERN POLAND - FIELD LANDING",
     22.5, 51.2),
    (7, "CENTRAL IRAQ", "MIDEAST", "WAR",
     "Iraqi army enters militia stronghold",
     "Troops deploy to Jurf al-Sakhar in the first push into the town in "
     "years. (Reuters)",
     "Witnessed - Reuters", "JURF AL-SAKHAR", "JURF AL-SAKHAR - CENTRAL IRAQ",
     44.2, 32.9),
    (8, "ITALY", "EUROPE", "LABOUR",
     "General strike over Italy's budget",
     "Workers and students march in about 100 squares in a 24-hour "
     "stoppage called by CGIL. (Reuters, AFP)",
     "Reported - Reuters", "SCIOPERO - 24H", "ITALY - 100 SQUARES MARCH",
     12.5, 41.9),
    (9, "TOKYO", "ASIA", "ECONOMY",
     "Japan's inflation picks up to 2.3%",
     "Inflation rose to 2.3% in October from 2.1%, above target a second "
     "month, December rate rise in view. (Reuters)",
     "Official data - Reuters", "CPI +2.3% OCT", "TOKYO - OCTOBER CPI",
     139.7, 35.7),
    (10, "SEOUL", "ASIA", "POLITICS",
     "Korea's ruling party to impeach top judge",
     "The party voted to impeach Chief Justice Cho Hee-dae, after an "
     "overturned conviction. (Korea Herald)",
     "Party decision - Korea Herald", "CAUCUS VOTE", "SEOUL - CAUCUS VOTE",
     127.0, 37.6),
    (11, "TURKANA, KENYA", "AFRICA", "OIL",
     "Kenya starts drilling its first oil well",
     "The ceremony opened the Turkana field. First crude is due on "
     "1 December. (allAfrica)",
     "Ceremony held - allAfrica", "FIRST CRUDE 1 DEC",
     "TURKANA - FIRST WELL",
     35.9, 3.1),
    (12, "SAN SALVADOR", "AMERICAS", "VOTE",
     "Bukele files to run for a third term",
     "He filed with the electoral tribunal on Friday. The vote is on "
     "28 February 2027. (AP)",
     "Filed - AP", "VOTE 28 FEB 2027", "SAN SALVADOR - FILING DAY",
     -89.2, 13.7),
    (13, "WELLINGTON", "OCEANIA", "SPORT",
     "Phillips hits 118 against India",
     "Glenn Phillips made 118 and Henry Nicholls 175 in a stand of 216. "
     "Hundreds in all three formats. (ICC)",
     "Scorecard - ICC", "118 - RECORD", "WELLINGTON - DAY'S PLAY",
     174.8, -41.3),
]

# no, text (verbatim from POOL, source in parens), region, pin lon, pin lat
# (lon/lat None = no dot; brief 40 is the Mercury exit-arrow item)
BRIEFS = [
    (14, "Lviv A strike on a railway station kills two (BBC)",
     "EUROPE", 24.0, 49.8),
    (15, "Moscow Russia decries Estonia's border closure (Reuters)",
     "EUROPE", 37.6, 55.8),
    (16, "Berlin School pupils strike against military service (Al Jazeera)",
     "EUROPE", 13.4, 52.5),
    (17, "London General says UK runs cyber attacks abroad (Sky News)",
     "EUROPE", -0.1, 51.5),
    (18, "Beijing China holds its loan rates for an 18th month (Xinhua)",
     "ASIA", 116.4, 39.9),
    (19, "Tokyo SoftBank shares fall more than 14% in a day (Al Jazeera)",
     "ASIA", 139.7, 35.7),
    (20, "Seoul Kospi index ends the week 7.9% lower (Anadolu)",
     "ASIA", 127.0, 37.6),
    (21, "Ganjam 209 mm of rain falls as Akvan crosses Odisha (PTI)",
     "ASIA", 84.9, 19.3),
    (22, "Lebanon Israeli air strikes hit the south and the east (Anadolu)",
     "MIDEAST", 35.5, 33.3),
    (23, "Yemen Gunmen fire on a cargo ship off the coast (UKMTO)",
     "MIDEAST", 43.3, 11.8),
    (24, "Abuja Court bars new evidence against Tinubu (Channels TV)",
     "AFRICA", 7.5, 9.1),
    (25, "Kampala Police told to enforce Ebola ban on rallies (allAfrica)",
     "AFRICA", 32.6, 0.3),
    (26, "Malawi Fuel crisis brings night-long petrol queues (Al Jazeera)",
     "AFRICA", 33.8, -13.9),
    (27, "Africa AfDB says 22 countries are in debt distress (allAfrica)",
     "AFRICA", 20.0, 5.0),
    (28, "Las Vegas Russell fastest in wet Grand Prix practice (Autosport)",
     "AMERICAS", -115.1, 36.2),
    (29, "New York Nasdaq futures fall 1.6% before the bell (24/7 Wall St)",
     "AMERICAS", -74.0, 40.7),
    (30, "Washington Democrats query law firm's free work (Al Jazeera)",
     "AMERICAS", -77.0, 38.9),
    (31, "Sydney Australian shares fall 1.6% in the sell-off (Reuters)",
     "OCEANIA", 151.2, -33.9),
    (32, "Antalya Panama asks COP31 to cap world oil output (Al Jazeera)",
     "GLOBAL", 30.7, 36.9),
    (33, "Antalya EU official calls the climate draft unacceptable (RTE)",
     "GLOBAL", 30.7, 36.9),
    (34, "Turin ATP backs a plan to lift player pay past $350m (Anadolu)",
     "GLOBAL", 7.7, 45.1),
    (35, "Bougainville Rio Tinto pledges $370m for Panguna mine cleanup "
     "(Reuters)", "OCEANIA", 155.9, -6.3),
    (36, "Iowa US Army sets noon detonation of 68 unstable explosive "
     "barrels (AP)", "AMERICAS", -93.6, 41.9),
    (37, "Hormuz Four attacks on vessels in 96 hours, maritime centre "
     "says (UKMTO)", "ASIA", 56.3, 26.6),
    (38, "Jakarta Indonesia's parliament passes asset-forfeiture bill "
     "(Reuters)", "ASIA", 106.8, -6.2),
    (39, "Barcelona Pancreatic cancer pill shrinks tumours 60.7% in early "
     "trial (Reuters)", "EUROPE", 2.2, 41.4),
    (40, "Mercury BepiColombo reaches Mercury after 8 years; orbit "
     "insertion set for Saturday (ESA, BBC)", "GLOBAL", None, None),
]

DATECHECK = (
    "Left out as Thursday 19 November's news: the World Court's ruling on "
    "Myanmar, the three-leader declaration in Shenzhen, the migrant boat "
    "lost off Senegal, Anthropic's $83bn IPO pricing, the GTA VI midnight "
    "launch, the $190.4m Van Gogh sale and the Senate's 48-51 Iran "
    "war-powers vote. Not yet happened, so not shown: COP31's final text "
    "and BepiColombo's entry into orbit around Mercury (set for Saturday)."
)

FOOTER_L = ("Every story here happened, or was first reported, on Friday "
            "20 November 2026. Contested claims are attributed.")
FOOTER_R = "Sources named beside each story - original drawings"

# ------------------------------------------------------------- scenes -----
# Each scene draws inside (x, y, w, h): flat gray shapes; red is reserved
# for the data element of the story.
def scene1(d, x, y, w, h):  # Kyiv: river, three bridges, red missile arcs
    d.polygon([(x, y + h * 0.62), (x + w * 0.45, y + h * 0.45),
               (x + w, y + h * 0.72), (x + w, y + h), (x, y + h)],
              fill=GRAY2)
    for i, bx in enumerate((0.14, 0.47, 0.78)):
        by = y + h * (0.52 + 0.07 * i)
        d.line([(x + w * bx, by), (x + w * (bx + 0.2), by)], fill=INK, width=3)
        d.line([(x + w * (bx + 0.04), by), (x + w * (bx + 0.04), by + h * 0.3)],
               fill=INK, width=2)
        d.line([(x + w * (bx + 0.16), by), (x + w * (bx + 0.16), by + h * 0.3)],
               fill=INK, width=2)
        sx, sy = x + w * (bx - 0.06), y + h * 0.06
        ex, ey = x + w * (bx + 0.1), by - 2
        for t in range(9):
            tt = t / 8.0
            px = sx + (ex - sx) * tt
            py = sy + (ey - sy) * tt * tt
            if t:
                d.line([(ox, oy), (px, py)], fill=RED, width=2)
            ox, oy = px, py


def scene2(d, x, y, w, h):  # Akvan: spiral storm, coast, red landfall dot
    cx, cy = x + w * 0.38, y + h * 0.52
    for r in (0.42, 0.3, 0.18):
        d.arc([cx - w * r, cy - h * r * 1.6, cx + w * r, cy + h * r * 1.6],
              start=20, end=320, fill=MGRAY, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=INK)
    coast = [(x + w * 0.78 + 6 * ((i % 2) * 2 - 1), y + i * h / 6.0)
             for i in range(7)]
    d.line(coast, fill=INK, width=2)
    d.polygon(coast + [(x + w, y + h), (x + w, y)], fill=(214, 214, 214))
    d.line(coast, fill=INK, width=2)
    lx, ly = x + w * 0.79, y + h * 0.52
    d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], outline=RED, width=3)


def scene3(d, x, y, w, h):  # Markets: gridlines, red falling line
    for i in range(3):
        gy = y + h * (0.25 + 0.25 * i)
        d.line([(x + 4, gy), (x + w - 4, gy)], fill=GRAY2, width=1)
    pts = [(x + w * (0.05 + 0.15 * i),
            y + h * (0.18 + 0.13 * i + (0.05 if i % 2 else 0)))
           for i in range(7)]
    d.line(pts, fill=RED, width=3)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 9, ey - 3), (ex - 4, ey + 7)], fill=RED)


def scene4(d, x, y, w, h):  # UK-EU: two flags, red link between
    fx, fy, fw, fh = x + w * 0.08, y + h * 0.2, w * 0.3, h * 0.55
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=MGRAY, width=2)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=MGRAY, width=2)
    d.rectangle([fx + fw * 0.4, fy, fx + fw * 0.6, fy + fh], fill=MGRAY)
    d.rectangle([fx, fy + fh * 0.38, fx + fw, fy + fh * 0.62], fill=MGRAY)
    ex, ey, ew, eh = x + w * 0.62, y + h * 0.2, w * 0.3, h * 0.55
    d.rectangle([ex, ey, ex + ew, ey + eh], outline=INK, width=2)
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12
        px = ex + ew / 2 + ew * 0.32 * math.cos(a)
        py = ey + eh / 2 + eh * 0.32 * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
    my = y + h * 0.47
    d.line([(fx + fw + 3, my), (ex - 3, my)], fill=RED, width=3)
    d.polygon([(ex - 3, my), (ex - 11, my - 4), (ex - 11, my + 4)], fill=RED)


def scene5(d, x, y, w, h):  # COP31: globe, thermometer with red column
    cx, cy, r = x + w * 0.34, y + h * 0.52, h * 0.4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=MGRAY,
              width=1)
    d.line([(cx - r, cy - r * 0.45), (cx + r, cy - r * 0.45)], fill=MGRAY)
    d.line([(cx - r, cy + r * 0.45), (cx + r, cy + r * 0.45)], fill=MGRAY)
    tx = x + w * 0.78
    d.rectangle([tx - 3, y + h * 0.14, tx + 3, y + h * 0.72], outline=INK,
                width=2)
    d.rectangle([tx - 2, y + h * 0.34, tx + 2, y + h * 0.72], fill=RED)
    d.ellipse([tx - 8, y + h * 0.66, tx + 8, y + h * 0.66 + 16], outline=INK,
              width=2)
    d.ellipse([tx - 5, y + h * 0.66 + 3, tx + 5, y + h * 0.66 + 13], fill=RED)


def scene6(d, x, y, w, h):  # Poland: field furrows, missile, red burst
    for i in range(4):
        gy = y + h * (0.55 + 0.12 * i)
        d.line([(x + 3, gy), (x + w - 3, gy)], fill=MGRAY, width=1)
    mx, my = x + w * 0.58, y + h * 0.34
    d.polygon([(mx - 26, my - 8), (mx + 14, my + 6), (mx + 26, my + 16),
               (mx + 10, my + 20), (mx - 20, my + 4)], fill=MGRAY)
    d.polygon([(mx + 14, my + 6), (mx + 30, my + 10), (mx + 18, my + 20)],
              fill=INK)
    bx, by = mx + 30, my + 14
    for dx, dy in ((0, -9), (7, -6), (9, 2), (5, 8), (-4, 7), (-8, -2)):
        d.line([(bx, by), (bx + dx, by + dy)], fill=RED, width=2)


def scene7(d, x, y, w, h):  # Iraq: desert, two vehicles, sun
    d.ellipse([x + w * 0.06, y + h * 0.08, x + w * 0.06 + 14,
               y + h * 0.08 + 14], outline=MGRAY, width=2)
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=GRAY2)
    for vx in (0.3, 0.62):
        bx, by = x + w * vx, y + h * 0.52
        d.rectangle([bx, by, bx + w * 0.2, by + h * 0.2], fill=MGRAY)
        d.rectangle([bx + w * 0.12, by - h * 0.12, bx + w * 0.19,
                     by], fill=MGRAY)
        for wx in (0.04, 0.15):
            cx = bx + w * wx
            d.ellipse([cx - 5, by + h * 0.18, cx + 5, by + h * 0.18 + 10],
                      fill=INK)
    d.line([(x + w * 0.05, y + h * 0.9), (x + w * 0.4, y + h * 0.9)],
           fill=MGRAY, width=1)

def scene8(d, x, y, w, h):  # Italy: banner over a crowd
    bx, by, bw, bh = x + w * 0.22, y + h * 0.08, w * 0.56, h * 0.3
    d.line([(bx + 3, by - 2), (bx + 3, by + bh + h * 0.3)], fill=INK, width=2)
    d.line([(bx + bw - 3, by - 2), (bx + bw - 3, by + bh + h * 0.3)],
           fill=INK, width=2)
    d.rectangle([bx, by, bx + bw, by + bh], fill=WHITE, outline=INK, width=2)
    for i in range(9):
        hx = x + w * (0.08 + 0.1 * i)
        hy = y + h * 0.72
        d.ellipse([hx - 5, hy - 10, hx + 5, hy], fill=MGRAY)
        d.rectangle([hx - 7, hy, hx + 7, hy + h * 0.24], fill=MGRAY)


def scene9(d, x, y, w, h):  # Japan: rising bars, red trend line
    base = y + h * 0.88
    tops = []
    for i, fr in enumerate((0.3, 0.45, 0.58, 0.78)):
        bx = x + w * (0.12 + 0.2 * i)
        bw = w * 0.13
        top = base - h * fr
        d.rectangle([bx, top, bx + bw, base], fill=MGRAY if i < 3 else INK)
        tops.append((bx + bw / 2, top - 3))
    d.line(tops, fill=RED, width=3)
    ex, ey = tops[-1]
    d.polygon([(ex, ey), (ex - 9, ey + 1), (ex - 3, ey + 8)], fill=RED)
    d.line([(x + 3, base), (x + w - 3, base)], fill=INK, width=1)


def scene10(d, x, y, w, h):  # Seoul: courthouse
    cx = x + w / 2
    top = y + h * 0.1
    d.polygon([(cx - w * 0.34, top + h * 0.22), (cx + w * 0.34, top + h * 0.22),
               (cx, top)], fill=INK)
    for i in range(4):
        cxx = x + w * (0.24 + 0.17 * i)
        d.rectangle([cxx - 3, top + h * 0.3, cxx + 3, top + h * 0.78],
                    fill=MGRAY)
    d.rectangle([x + w * 0.14, top + h * 0.82, x + w * 0.86, top + h * 0.9],
                fill=INK)


def scene11(d, x, y, w, h):  # Kenya: oil derrick, red droplet
    ax, ay = x + w * 0.34, y + h * 0.06
    bx, by = x + w * 0.14, y + h * 0.92
    d.line([(bx, by), (ax, ay)], fill=INK, width=3)
    d.line([(x + w * 0.54, by), (ax, ay)], fill=INK, width=3)
    for t in (0.3, 0.55, 0.8):
        yy = ay + (by - ay) * t
        half = w * 0.2 * t
        d.line([(ax - half, yy), (ax + half, yy)], fill=MGRAY, width=2)
    d.line([(x + 3, by), (x + w - 3, by)], fill=INK, width=1)
    dx, dy = ax, y + h * 0.52
    d.polygon([(dx, dy - 10), (dx - 6, dy + 4), (dx + 6, dy + 4)], fill=RED)
    d.ellipse([dx - 6, dy, dx + 6, dy + 11], fill=RED)


def scene12(d, x, y, w, h):  # San Salvador: ballot box and paper
    bx, by, bw, bh = x + w * 0.3, y + h * 0.38, w * 0.42, h * 0.52
    d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=3)
    d.line([(bx + bw * 0.25, by + 5), (bx + bw * 0.75, by + 5)], fill=INK,
           width=3)
    d.polygon([(bx + bw * 0.38, by - h * 0.26), (bx + bw * 0.66, by - h * 0.2),
               (bx + bw * 0.6, by + 4), (bx + bw * 0.34, by - 2)], fill=WHITE,
              outline=INK)
    d.ellipse([bx + bw * 0.42, by + bh * 0.42, bx + bw * 0.58,
               by + bh * 0.42 + (bx + bw * 0.58) - (bx + bw * 0.42)],
              outline=RED, width=2)


def scene13(d, x, y, w, h):  # Wellington: stumps, bat, red ball
    sx = x + w * 0.6
    for i in range(3):
        d.line([(sx + i * 9, y + h * 0.2), (sx + i * 9, y + h * 0.85)],
               fill=INK, width=3)
    d.line([(sx - 2, y + h * 0.17), (sx + 8, y + h * 0.17)], fill=INK, width=2)
    d.line([(sx + 10, y + h * 0.17), (sx + 20, y + h * 0.17)], fill=INK,
           width=2)
    d.polygon([(x + w * 0.2, y + h * 0.85), (x + w * 0.3, y + h * 0.85),
               (x + w * 0.42, y + h * 0.2), (x + w * 0.34, y + h * 0.14)],
              fill=MGRAY)
    bx, by = x + w * 0.47, y + h * 0.38
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=RED)


SCENES = {1: scene1, 2: scene2, 3: scene3, 4: scene4, 5: scene5, 6: scene6,
          7: scene7, 8: scene8, 9: scene9, 10: scene10, 11: scene11,
          12: scene12, 13: scene13}


def draw_strip(d, x, y, w, h, card, lead):
    no, place, region, topic = card[0], card[1], card[2], card[3]
    tag, label, caption = card[6], card[7], card[8]
    d.rectangle([x, y, x + w, y + h], fill=LGRAY)
    d.rectangle([x, y, x + w, y + 3], fill=REG[region])
    SCENES[no](d, x, y + 3, w, h - 19)
    # source tag: white pill, top-right, its own clear zone
    ftag = AB(9)
    pw = tw(d, tag, ftag) + 10
    px, py = x + w - pw - 4, y + 6
    d.rectangle([px, py, px + pw, py + 14], fill=WHITE, outline=INK, width=1)
    T(d, px + 5, py + 2, tag, ftag)
    # data label: red bold, bottom-left above the caption band, white backing
    flab = AB(13 if lead else 10)
    lines = label.split("\n")
    lh = 16 if lead else 12
    lab_h = lh * len(lines)
    lab_w = max(tw(d, ln, flab) for ln in lines)
    ly = y + h - 16 - lab_h - 3
    d.rectangle([x + 3, ly - 1, x + 3 + lab_w + 6, ly + lab_h + 1], fill=WHITE)
    for i, ln in enumerate(lines):
        T(d, x + 6, ly + i * lh, ln, flab, fill=RED)
    # caption band at the strip's bottom edge
    d.rectangle([x, y + h - 16, x + w, y + h], fill=INK)
    fcap = fit_font(d, caption, AB, 9, w - 8, 7)
    T(d, x + (w - tw(d, caption, fcap)) / 2, y + h - 12, caption, fcap,
      fill=WHITE)


def draw_card(d, x, y, w, strip_h, card, lead):
    no, place, region, topic = card[0], card[1], card[2], card[3]
    headline, deck = card[4], card[5]
    draw_strip(d, x, y, w, strip_h, card, lead)
    rline = "%d %s - %s - %s" % (no, place, region, topic)
    if lead:
        fr = fit_font(d, rline, AB, 10, w)
        T(d, x, y + strip_h + 4, rline, fr, fill=REG[region])
        fh, lh_h = AB(21), 22
        hy = y + strip_h + 19
        fd, lh_d = AM(12), 14
    else:
        fr = fit_font(d, rline, AB, 9, w, 7)
        T(d, x, y + strip_h + 3, rline, fr, fill=REG[region])
        fh, lh_h = AB(15), 16
        hy = y + strip_h + 15
        fd, lh_d = AM(11), 12
    for i, ln in enumerate(wrap(d, headline, fh, w)):
        T(d, x, hy + i * lh_h, ln, fh)
    dy = hy + 2 * lh_h + 3
    for i, ln in enumerate(wrap(d, deck, fd, w)):
        T(d, x, dy + i * lh_d, ln, fd, fill=(34, 34, 34))

# ------------------------------------------------------------- header -----
def draw_header(d):
    # kicker bar
    T(d, M, 8, "THE GLOBAL WIRE", AB(15))
    bx = M + tw(d, "THE GLOBAL WIRE", AB(15)) + 12
    T(d, bx, 11, "THE WORLD IN ONE DAY", AM(11), fill=MGRAY)
    kr = "40 STORIES - 7 REGIONS - EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    T(d, W - M - tw(d, kr, AB(10)), 11, kr, AB(10))
    rule(d, M, W - M, 27, wdt=2)
    rule(d, M, W - M, 30, wdt=1)
    # masthead (ink of PF(58) drawn at y=33 ends at y=107; deckline at 108)
    T(d, M, 33, "Friday 20 November 2026", PF(58))
    T(d, M, 108,
      "Kyiv bridges hit in the night barrage - Cyclone Akvan ashore in "
      "Odisha - AI sell-off sinks Asia's markets - UK and EU seal the "
      "reset deal", AM(12), fill=MGRAY)
    rule(d, M, W - M, 126)
    # UTC timeline: five divided slots
    sw = CW / 5.0
    for i, (lab, ev) in enumerate(TIMELINE):
        sx = M + i * sw
        if i:
            vrule(d, sx, 132, 166, fill=GRAY2)
        T(d, sx + 6, 131, lab, AB(11), fill=RED)
        for j, ln in enumerate(wrap(d, ev, AM(10), sw - 12)):
            T(d, sx + 6, 145 + j * 11, ln, AM(10))
    rule(d, M, W - M, 172)
    # THE DAY IN NUMBERS: a ruled table, figures in red
    rule(d, M, W - M, 176)
    lab = "THE DAY IN NUMBERS"
    lw = tw(d, lab, AB(11))
    d.rectangle([W / 2 - lw / 2 - 8, 170, W / 2 + lw / 2 + 8, 182],
                fill=WHITE)
    T(d, W / 2 - lw / 2, 171, lab, AB(11))
    cw6 = CW / 6.0
    for i, (fig, cap) in enumerate(NUMBERS):
        cx = M + i * cw6
        if i:
            vrule(d, cx, 180, 234, fill=GRAY2)
        ff = fit_font(d, fig, AB, 25, cw6 - 12)
        T(d, cx + (cw6 - tw(d, fig, ff)) / 2, 183, fig, ff, fill=RED)
        for j, ln in enumerate(wrap(d, cap, AM(10), cw6 - 12)):
            T(d, cx + (cw6 - tw(d, ln, AM(10))) / 2, 213 + j * 11, ln,
              AM(10), fill=MGRAY)
    rule(d, M, W - M, 237)
    # region count strip: white chips, black border, color bullet
    T(d, M, 246, "40 STORIES BY REGION", AB(11))
    cx = M + tw(d, "40 STORIES BY REGION", AB(11)) + 14
    for name, cnt in REGION_COUNTS:
        s = "%s %d" % (name, cnt)
        chw = tw(d, s, AB(11)) + 26
        d.rectangle([cx, 242, cx + chw, 262], fill=WHITE, outline=INK,
                    width=1)
        d.rectangle([cx + 6, 248, cx + 14, 256], fill=REG[name])
        T(d, cx + 19, 246, s, AB(11))
        cx += chw + 7

# -------------------------------------------------------------- cards -----
def draw_cards(d):
    # lead row: cards 1-3, 325 wide
    for i, card in enumerate(CARDS[:3]):
        draw_card(d, M + i * 333, 266, 325, 92, card, True)
    # feature grid: cards 4-13, 2 rows x 5 cols, 196 wide
    for k, card in enumerate(CARDS[3:]):
        r, c = divmod(k, 5)
        draw_card(d, M + c * 199, 472 + r * 134, 196, 44, card, False)


# ---------------------------------------------------------------- map -----
def draw_map(d):
    T(d, M, 752, "WHERE IT HAPPENED", AB(12))
    x0, y0, x1, y1 = M, 768, M + 330, 892
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=INK, width=1)
    ix0, iy0, iw, ih = x0 + 1, y0 + 1, 328, 122

    def proj(lon, lat):
        return (ix0 + (lon + 180) / 360.0 * iw,
                iy0 + (82 - lat) / 140.0 * ih)

    for s in WORLD.values():
        for ring in s.split("|"):
            pts = []
            for pair in ring.split(","):
                lo, la = pair.split(":")
                pts.append(proj(float(lo), float(la)))
            if len(pts) >= 3:
                d.polygon(pts, fill=LAND, outline=INK)
    for no, txt, region, lon, lat in BRIEFS:
        if lon is None:
            continue
        px, py = proj(lon, lat)
        d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=REG[region])
    for card in CARDS:
        px, py = proj(card[9], card[10])
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=REG[card[2]],
                  outline=RED, width=2)
    for card in CARDS:
        px, py = proj(card[9], card[10])
        s = str(card[0])
        T(d, px - tw(d, s, AB(9)) / 2, py - 5, s, AB(9), fill=WHITE)
    ay = y1 - 9
    for xx in range(x0 + 6, x0 + 33, 6):
        d.line([(xx, ay), (xx + 3, ay)], fill=RED, width=2)
    d.polygon([(x0 + 38, ay), (x0 + 30, ay - 3), (x0 + 30, ay + 3)], fill=RED)
    T(d, x0 + 44, ay - 5, "40 -> to Mercury", AB(9), fill=RED)
    T(d, M, 897,
      "Numbered pins = the 13 pictured stories - small dots = the briefs",
      AM(9), fill=MGRAY)

# ------------------------------------------------------------- bottom -----
def draw_bottom_right(d):
    x0 = 358
    T(d, x0, 752, "ALSO ON FRIDAY 20 NOVEMBER - 27 MORE STORIES", AB(12))
    colw = 319
    cols = [BRIEFS[:15], BRIEFS[15:]]
    wrapped = []
    for col in cols:
        lines = []
        for no, txt, region, lon, lat in col:
            lines.extend(wrap(d, "%d %s" % (no, txt), AM(10), colw))
        wrapped.append(lines)
    lh = min(11.5, 234.0 / max(len(lines) for lines in wrapped))
    for ci, lines in enumerate(wrapped):
        cx = x0 + ci * (colw + 12)
        for j, ln in enumerate(lines):
            T(d, cx, 774 + j * lh, ln, AM(10))


def draw_datecheck(d):
    d.rectangle([M, 910, M + 330, 1008], outline=RED, width=2)
    T(d, M + 8, 916, "DATE CHECK", AB(11), fill=RED)
    for j, ln in enumerate(wrap(d, DATECHECK, AM(10), 314)):
        T(d, M + 8, 932 + j * 11, ln, AM(10))


def draw_footer(d):
    rule(d, M, W - M, 1012, fill=GRAY2)
    T(d, M, 1014, FOOTER_L, AM(10), fill=MGRAY)
    T(d, W - M - tw(d, FOOTER_R, AM(10)), 1014, FOOTER_R, AM(10), fill=MGRAY)


def compose():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_cards(d)
    draw_map(d)
    draw_bottom_right(d)
    draw_datecheck(d)
    draw_footer(d)
    out = os.path.join(BASE, "entry.png")
    img.save(out)
    print("saved", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    compose()
