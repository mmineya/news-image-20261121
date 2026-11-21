"""Local, deterministic Pillow artwork builder. Not used by the entry runtime."""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont


S = 2
PAPER = (244, 237, 221)
INK = (40, 42, 41)
RED = (177, 47, 40)
MUTED = (132, 129, 117)
LIGHT = (215, 208, 190)
ROOT = Path(__file__).resolve().parent
rng = random.Random(20261121)
im = Image.new("RGB", (1024 * S, 1024 * S))
px = im.load()
for y in range(1024 * S):
    shade = 2.3 * y / (1024 * S)
    for x in range(1024 * S):
        grain = rng.choice((-1, 0, 0, 0, 1))
        px[x, y] = tuple(round(v - shade + grain) for v in PAPER)
d = ImageDraw.Draw(im)


def font(size, serif=False, regular=False):
    family = "DejaVuSerif" if serif else "DejaVuSans"
    name = family + ("" if regular else "-Bold") + ".ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, round(size * S))


def line(points, fill=INK, width=2):
    d.line([(round(x*S), round(y*S)) for x, y in points], fill=fill, width=round(width*S), joint="curve")


def rect(box, fill=None, outline=None, width=2, radius=0):
    box = tuple(round(v*S) for v in box)
    if radius:
        d.rounded_rectangle(box, radius=round(radius*S), fill=fill, outline=outline, width=round(width*S))
    else:
        d.rectangle(box, fill=fill, outline=outline, width=round(width*S))


def poly(points, fill=INK):
    d.polygon([(round(x*S), round(y*S)) for x, y in points], fill=fill)


def ellipse(box, fill=None, outline=None, width=2):
    d.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=round(width*S))


def text_center(text, x, y, size, fill=INK, serif=False, maxwidth=None, regular=False):
    f = font(size, serif, regular)
    box = d.textbbox((0, 0), text, font=f)
    if maxwidth is not None:
        assert box[2] - box[0] <= maxwidth*S, (text, box, maxwidth)
    left = x*S - (box[2]-box[0])/2 - box[0]
    top = y*S - box[1]
    d.text((round(left), round(top)), text, font=f, fill=fill)


# The masthead and rules establish an editorial newspaper grid.
text_center("21 NOVEMBER 2026", 512, 32, 65, serif=True, maxwidth=952)
line([(36, 110), (988, 110)], width=4)
line([(36, 119), (988, 119)], width=1)
line([(512, 140), (512, 986)], fill=MUTED, width=1)
for y in (416, 704):
    line([(36, y), (988, y)], fill=INK, width=1)
line([(36, 992), (988, 992)], width=3)


def headline(words, cx, y):
    # Fixed minimum 32 pt; measured separately for every rendered line.
    for i, word in enumerate(words):
        text_center(word, cx, y + i*37, 34, maxwidth=438)


tops = [140, 428, 716]
labels = [
    ["AI STOCK ROUT"],
    ["400 DRONES", "ON UKRAINE"],
    ["FBI HACKED AGAIN"],
    ["COP31 IN OVERTIME"],
    ["UN DEADLOCK"],
    ["HORMUZ ATTACKS"],
]
for i, words in enumerate(labels):
    row, col = divmod(i, 2)
    x, y = (36 if col == 0 else 530), tops[row]
    headline(words, x+229, y+9)
    text_center("NOV 21", x+229, y+249, 15, fill=RED, maxwidth=438)

# 1: collapsing market, circuit chip and unmistakable downward arrow.
x, y = 36, tops[0]
for gy in (y+84, y+126, y+168, y+210):
    line([(x+24, gy), (x+294, gy)], LIGHT, 1)
line([(x+24, y+65), (x+24, y+223), (x+310, y+223)], INK, 2)
points = [(x+38,y+78),(x+86,y+103),(x+122,y+91),(x+164,y+143),(x+203,y+131),(x+246,y+186),(x+280,y+210)]
poly(points+[(x+280,y+222),(x+38,y+222)], (226, 207, 188))
line(points, RED, 8)
poly([(x+264,y+210),(x+295,y+221),(x+290,y+187)], RED)
rect((x+326,y+110,x+414,y+199), fill=INK, radius=8)
rect((x+344,y+129,x+396,y+180), outline=PAPER, width=2)
for n in range(5):
    a = x+337+n*16
    line([(a,y+99),(a,y+110)], INK, 3)
    line([(a,y+199),(a,y+211)], INK, 3)
    a = y+122+n*16
    line([(x+315,a),(x+326,a)], INK, 3)
    line([(x+414,a),(x+426,a)], INK, 3)
line([(x+370,y+140),(x+370,y+163)], RED, 7)
poly([(x+357,y+156),(x+383,y+156),(x+370,y+172)], RED)

# 2: drone swarm, skyline and a red crescent.
x, y = 530, tops[0]
ellipse((x+350,y+90,x+404,y+144), RED)
ellipse((x+367,y+83,x+413,y+130), PAPER)
for dx, dy, scale in [(50,104,.9),(128,115,1),(206,98,.8),(286,123,.9),(86,150,.7),(175,158,.9),(256,165,.6),(329,170,.6)]:
    a,b = x+dx,y+dy
    line([(a-19*scale,b-6*scale),(a+19*scale,b+6*scale)], INK, 2)
    line([(a-19*scale,b+6*scale),(a+19*scale,b-6*scale)], INK, 2)
    for sx in (-1,1):
        for sy in (-1,1):
            ellipse((a+sx*19*scale-7*scale,b+sy*6*scale-3*scale,a+sx*19*scale+7*scale,b+sy*6*scale+3*scale), outline=INK, width=1)
    poly([(a,b-6*scale),(a+9*scale,b),(a,b+10*scale),(a-9*scale,b)], INK)
for dx,w,h in [(22,38,28),(63,27,46),(94,42,34),(141,31,57),(177,35,41),(217,43,31),(266,32,49),(304,41,37),(350,28,60),(383,49,30)]:
    rect((x+dx,y+231-h,x+dx+w,y+233), INK)
    if h>40:
        line([(x+dx+w/2,y+231-h-10),(x+dx+w/2,y+231-h)], INK, 2)
    for wy in range(int(y+239-h), int(y+222), 12):
        rect((x+dx+9,wy,x+dx+13,wy+4), PAPER)

# 3: case folder with a broken security lock.
x,y=36,tops[1]
poly([(x+67,y+102),(x+67,y+78),(x+172,y+78),(x+194,y+99),(x+385,y+99),(x+385,y+220),(x+67,y+220)], INK)
poly([(x+63,y+117),(x+396,y+117),(x+371,y+228),(x+78,y+228)], LIGHT)
line([(x+63,y+117),(x+396,y+117),(x+371,y+228),(x+78,y+228),(x+63,y+117)], INK, 3)
text_center("FBI", x+171,y+151,46,maxwidth=150)
d.arc(tuple(round(v*S) for v in (x+280,y+97,x+344,y+174)),180,355,fill=RED,width=8*S)
rect((x+271,y+145,x+353,y+211), RED, radius=5)
poly([(x+319,y+141),(x+304,y+166),(x+321,y+176),(x+305,y+193),(x+314,y+217),(x+327,y+190),(x+316,y+177),(x+328,y+161)], PAPER)
line([(x+348,y+112),(x+361,y+101)], RED, 3)
line([(x+359,y+130),(x+378,y+128)], RED, 3)

# 4: a struck-out draft, conference seal, and an overtime clock.
x,y=530,tops[1]
poly([(x+61,y+66),(x+261,y+66),(x+287,y+93),(x+287,y+228),(x+61,y+228)], fill=(231,224,208))
line([(x+61,y+66),(x+261,y+66),(x+287,y+93),(x+287,y+228),(x+61,y+228),(x+61,y+66)], INK, 2)
line([(x+261,y+66),(x+261,y+93),(x+287,y+93)], INK, 2)
text_center("FOSSIL FUELS", x+175,y+113,21,maxwidth=218)
line([(x+76,y+137),(x+275,y+107)], RED, 5)
for w,gy in [(156,157),(169,175),(132,193)]:
    line([(x+82,y+gy),(x+82+w,y+gy)], MUTED, 3)
ellipse((x+256,y+157,x+386,y+236), outline=RED, width=3)
ellipse((x+261,y+162,x+381,y+231), outline=RED, width=1)
text_center("COP31",x+321,y+185,26,fill=RED,maxwidth=116)
ellipse((x+324,y+65,x+421,y+162),fill=PAPER,outline=INK,width=4)
cx,cy=x+372.5,y+113.5
for n in range(12):
    a=n*math.pi/6
    line([(cx+math.sin(a)*37,cy-math.cos(a)*37),(cx+math.sin(a)*41,cy-math.cos(a)*41)], INK, 2)
line([(cx,cy-26),(cx,cy),(cx+21,cy+14)], RED, 4)
ellipse((cx-4,cy-4,cx+4,cy+4), RED)

# 5: the empty chair and UN globe at a vacant lectern.
x,y=36,tops[2]
rect((x+69,y+75,x+162,y+152), fill=INK, radius=10)
rect((x+63,y+163,x+168,y+177), fill=INK, radius=4)
line([(x+80,y+177),(x+73,y+229)], INK, 6)
line([(x+152,y+177),(x+159,y+229)], INK, 6)
line([(x+70,y+147),(x+57,y+147),(x+57,y+170)], INK, 5)
line([(x+161,y+147),(x+177,y+147),(x+177,y+170)], INK, 5)
poly([(x+221,y+132),(x+389,y+132),(x+371,y+227),(x+239,y+227)], INK)
rect((x+207,y+119,x+402,y+134), INK)
ellipse((x+277,y+150,x+335,y+208),outline=PAPER,width=2)
ellipse((x+291,y+150,x+321,y+208),outline=PAPER,width=1)
line([(x+277,y+179),(x+335,y+179)], PAPER, 1)
for yy in (166,192):
    line([(x+282,y+yy),(x+330,y+yy)], PAPER, 1)
d.arc(tuple(round(v*S) for v in (x+266,y+148,x+345,y+217)),30,150,fill=PAPER,width=2*S)
line([(x+274,y+116),(x+274,y+98),(x+284,y+89)], INK, 3)
ellipse((x+281,y+84,x+290,y+92), INK)
text_center("?",x+343,y+60,48,fill=RED,maxwidth=55)
line([(x+42,y+232),(x+422,y+232)], MUTED, 1)

# 6: a tanker burning in dark water; waves stay flat and readable.
x,y=530,tops[2]
rect((x+22,y+192,x+436,y+234), INK)
poly([(x+44,y+159),(x+399,y+159),(x+368,y+204),(x+85,y+204)], INK)
line([(x+59,y+174),(x+388,y+174)], PAPER, 2)
rect((x+84,y+115,x+133,y+157), INK)
rect((x+74,y+108,x+140,y+120), INK)
for dx in (87,106,124):
    rect((x+dx,y+124,x+dx+8,y+133), PAPER)
line([(x+108,y+108),(x+108,y+88)], INK, 3)
for dx in (165,211,257,303):
    rect((x+dx,y+143,x+dx+37,y+158), INK, radius=6)
line([(x+148,y+138),(x+354,y+138)], INK, 3)
poly([(x+294,y+145),(x+279,y+123),(x+291,y+100),(x+299,y+119),(x+313,y+77),(x+330,y+101),(x+324,y+115),(x+342,y+105),(x+349,y+128),(x+335,y+146)], RED)
poly([(x+307,y+145),(x+303,y+130),(x+318,y+109),(x+317,y+132),(x+330,y+125),(x+326,y+146)], PAPER)
for dx,dy,r in [(330,91,8),(345,80,10),(360,70,11)]:
    ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=MUTED)
for dx,dy in [(38,211),(113,221),(201,213),(289,224),(365,213)]:
    line([(x+dx,y+dy),(x+dx+18,y+dy-3),(x+dx+38,y+dy)], PAPER, 2)

im = im.resize((1024, 1024), Image.Resampling.LANCZOS)
im.save(ROOT / "entry.png", format="PNG", optimize=True, compress_level=9)
assert (ROOT / "entry.png").stat().st_size <= 1024*1024
