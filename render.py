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
text_boxes = []
PANEL_TOPS = (140, 428, 716)


def font(size, serif=False, regular=False):
    family = "DejaVuSerif" if serif else "DejaVuSans"
    name = family + ("" if regular else "-Bold") + ".ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, round(size * S))


def line(points, fill=INK, width=2):
    d.line([(round(x*S), round(y*S)) for x, y in points], fill=fill, width=round(width*S), joint="curve")


def dashed_line(start, end, fill=MUTED, width=1, dash=5, gap=5):
    dx, dy = end[0]-start[0], end[1]-start[1]
    length = math.hypot(dx, dy)
    for step in range(0, math.ceil(length), dash+gap):
        stop = min(step+dash, length)
        line([(start[0]+dx*step/length, start[1]+dy*step/length),
              (start[0]+dx*stop/length, start[1]+dy*stop/length)], fill, width)


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
    actual = d.textbbox((round(left), round(top)), text, font=f)
    bounds = (36, 10, 988, 120)
    if y >= PANEL_TOPS[0]:
        panel_top = max(t for t in PANEL_TOPS if t <= y)
        panel_left = 36 if x < 512 else 530
        bounds = (panel_left+8, panel_top+4, panel_left+450, panel_top+276)
    assert actual[0] >= bounds[0]*S and actual[1] >= bounds[1]*S, (text, actual, bounds)
    assert actual[2] <= bounds[2]*S and actual[3] <= bounds[3]*S, (text, actual, bounds)
    text_boxes.append((text, actual, bounds))
    d.text((round(left), round(top)), text, font=f, fill=fill)


# The masthead and rules establish an editorial newspaper grid.
text_center("SATURDAY EDITION", 112, 17, 12, maxwidth=152)
text_center("WORLD BULLETIN", 916, 17, 12, maxwidth=144)
text_center("21 NOVEMBER 2026", 512, 43, 61, serif=True, maxwidth=952)
rect((36, 107, 988, 111), INK)
rect((36, 117, 988, 118), INK)
line([(512, 140), (512, 986)], fill=MUTED, width=1)
for y in (416, 704):
    line([(36, y), (988, y)], fill=INK, width=1)
line([(36, 992), (988, 992)], width=3)


def headline(words, cx, y):
    # Fixed minimum 32 pt; measured separately for every rendered line.
    for i, word in enumerate(words):
        text_center(word, cx, y + i*37, 34, maxwidth=438)


tops = PANEL_TOPS
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
text_center("-3.7%", x+370, y+54, 25, fill=RED, maxwidth=122)
text_center("S&P 500", x+370, y+85, 13, maxwidth=122)
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
ellipse((x+345,y+87,x+425,y+167), RED)
ellipse((x+371,y+76,x+437,y+142), PAPER)
for start, end in [((69,121),(112,194)), ((158,130),(193,190)),
                   ((247,142),(273,192)), ((305,156),(327,205))]:
    dashed_line((x+start[0],y+start[1]), (x+end[0],y+end[1]), width=1, dash=4, gap=5)
swarm = [(39,102,.48),(89,101,.65),(153,99,.4),(206,101,.75),(279,99,.45),
         (57,123,1.02),(124,120,.5),(171,128,.95),(247,124,.56),(302,129,.72),
         (35,156,.62),(104,151,.85),(143,167,.44),(222,159,.75),(283,172,.45),
         (323,162,.7)]
for dx, dy, scale in swarm:
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
text_center("FBI", x+171,y+142,46,maxwidth=150)
d.arc(tuple(round(v*S) for v in (x+280,y+97,x+344,y+174)),180,355,fill=RED,width=8*S)
rect((x+271,y+145,x+353,y+211), RED, radius=5)
poly([(x+319,y+141),(x+304,y+166),(x+321,y+176),(x+305,y+193),(x+314,y+217),(x+327,y+190),(x+316,y+177),(x+328,y+161)], PAPER)
line([(x+348,y+112),(x+361,y+101)], RED, 3)
line([(x+359,y+130),(x+378,y+128)], RED, 3)

# A separately measured transparent stamp retains clean type after rotation.
stamp_font = font(17)
stamp_box = d.textbbox((0, 0), "BREACHED", font=stamp_font)
sw, sh = stamp_box[2]-stamp_box[0]+24*S, stamp_box[3]-stamp_box[1]+14*S
stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
stamp_pos = (12*S-stamp_box[0], 7*S-stamp_box[1])
measured = sd.textbbox(stamp_pos, "BREACHED", font=stamp_font)
assert 0 < measured[0] < measured[2] < sw and 0 < measured[1] < measured[3] < sh
sd.rectangle((1*S, 1*S, sw-2*S, sh-2*S), outline=RED, width=2*S)
sd.text(stamp_pos, "BREACHED", font=stamp_font, fill=RED)
stamp = stamp.rotate(10, resample=Image.Resampling.BICUBIC, expand=True)
stamp_left, stamp_top = round((x+172)*S-stamp.width/2), round((y+205)*S-stamp.height/2)
assert stamp_left >= (x+8)*S and stamp_left+stamp.width <= (x+450)*S
assert stamp_top >= (y+55)*S and stamp_top+stamp.height < (y+240)*S
im.paste(stamp, (stamp_left, stamp_top), stamp)
text_boxes.append(("BREACHED", measured, (0, 0, sw, sh)))

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
poly([(x+69,y+95),(x+69,y+69),(x+86,y+73),(x+94,y+62),
      (x+138,y+62),(x+146,y+73),(x+162,y+69),(x+162,y+95)], INK)
rect((x+83,y+84,x+148,y+139), outline=LIGHT, width=1, radius=6)
rect((x+63,y+163,x+168,y+177), fill=INK, radius=4)
line([(x+80,y+177),(x+73,y+229)], INK, 6)
line([(x+152,y+177),(x+159,y+229)], INK, 6)
line([(x+70,y+147),(x+57,y+147),(x+57,y+170)], INK, 5)
line([(x+161,y+147),(x+177,y+147),(x+177,y+170)], INK, 5)
rect((x+52,y+188,x+182,y+212), fill=PAPER, outline=INK, width=1)
text_center("NEXT SG?",x+117,y+194,15,maxwidth=116)
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
for dx in (156,202,248):
    line([(x+dx,y+137),(x+dx,y+127),(x+dx+25,y+127)], INK, 2)
line([(x+143,y+153),(x+143,y+133),(x+357,y+133),(x+357,y+153)], INK, 1)
for dx in range(153, 355, 14):
    line([(x+dx,y+133),(x+dx,y+139)], INK, 1)
for dx in (88,102,116):
    ellipse((x+dx,y+181,x+dx+5,y+186),fill=PAPER)
poly([(x+365,y+179),(x+374,y+179),(x+374,y+185),(x+380,y+185),
      (x+370,y+197),(x+360,y+185),(x+365,y+185)], PAPER)
line([(x+102,y+90),(x+129,y+90)], INK, 2)
line([(x+129,y+90),(x+129,y+103)], INK, 2)
# Radiating red fragments frame the fire without entering the headline.
for start,end in [((280,104),(268,95)),((287,87),(282,75)),
                  ((346,99),(359,89)),((354,118),(371,115))]:
    line([(x+start[0],y+start[1]),(x+end[0],y+end[1])], RED, 3)
poly([(x+294,y+145),(x+279,y+123),(x+291,y+100),(x+299,y+119),(x+313,y+77),(x+330,y+101),(x+324,y+115),(x+342,y+105),(x+349,y+128),(x+335,y+146)], RED)
poly([(x+307,y+145),(x+303,y+130),(x+318,y+109),(x+317,y+132),(x+330,y+125),(x+326,y+146)], PAPER)
for dx,dy,r in [(330,91,8),(345,80,10),(360,70,11)]:
    ellipse((x+dx-r,y+dy-r,x+dx+r,y+dy+r),fill=MUTED)
for start, dy, count in [(30,210,6),(62,222,5),(32,231,6)]:
    for n in range(count):
        dx = start+n*64
        wave = [(x+dx+j*5, y+dy-2*math.sin(j*math.pi/4)) for j in range(9)]
        line(wave, PAPER if dy != 222 else LIGHT, 1)

im = im.resize((1024, 1024), Image.Resampling.LANCZOS)
im.save(ROOT / "entry.png", format="PNG", optimize=True, compress_level=9)
assert (ROOT / "entry.png").stat().st_size <= 1024*1024
print(f"Verified {len(text_boxes)} textbbox checks; saved 1024x1024 entry.png")
