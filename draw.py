#!/usr/bin/env python3
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W = H = 1024
PAPER, INK, RED, MUTED, BORDER = '#FBF8F1', '#14213D', '#C1272D', '#5A6472', '#D8D2C4'
REGION_COLORS = {'ASIA-PACIFIC':'#1D7874','EUROPE':'#26547C','MIDDLE EAST':'#BC4B26','AMERICAS':'#6C4AB0','AFRICA':'#B8860B'}
ORDER = ['ASIA-PACIFIC','EUROPE','MIDDLE EAST','AMERICAS','AFRICA']
REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, size)

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)

def wrap(text, f, max_width):
    words, lines, line = text.split(), [], ''
    for word in words:
        trial = word if not line else line + ' ' + word
        if d.textlength(trial, font=f) <= max_width:
            line = trial
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines

def fit_lines(text, size, bold, width, max_lines, min_size):
    for px in range(size, min_size - 1, -1):
        f = font(px, bold)
        lines = wrap(text, f, width)
        if len(lines) <= max_lines:
            return f, lines
    f = font(min_size, bold)
    return f, wrap(text, f, width)[:max_lines]

def centered(text, y, f, fill):
    d.text(((W-d.textlength(text, font=f))/2, y), text, font=f, fill=fill)

def icon(kind, x, y):
    c, lw = INK, 2
    if kind == 'flags':
        for i, col in enumerate((RED, '#FFFFFF', '#1D7874')):
            xx=x+5+i*11; d.line((xx,y+5,xx,y+38), fill=c, width=2); d.rectangle((xx+1,y+6,xx+9,y+22), fill=col, outline=c)
    elif kind == 'gamepad':
        d.rounded_rectangle((x+3,y+11,x+43,y+35), radius=8, outline=c, width=lw); d.line((x+11,y+23,x+22,y+23),fill=c,width=3); d.line((x+16,y+18,x+16,y+29),fill=c,width=3); d.ellipse((x+30,y+19,x+34,y+23),fill=RED); d.ellipse((x+36,y+25,x+40,y+29),fill=c)
    elif kind == 'tank':
        d.polygon([(x+4,y+28),(x+39,y+28),(x+34,y+37),(x+9,y+37)], outline=c, fill='#E8E3D8'); d.rectangle((x+12,y+20,x+31,y+28),outline=c,width=2); d.rectangle((x+19,y+16,x+29,y+20),fill=c); d.line((x+29,y+18,x+44,y+18),fill=c,width=3)
        for xx in range(x+10,x+36,7): d.ellipse((xx,y+32,xx+5,y+37),outline=c,width=1)
    elif kind == 'bridge':
        d.line((x+3,y+33,x+44,y+33),fill=c,width=2); d.line((x+10,y+9,x+10,y+34),fill=c,width=3); d.line((x+37,y+9,x+37,y+34),fill=c,width=3); d.arc((x+10,y+7,x+37,y+34),180,360,fill=RED,width=2); d.line((x+3,y+33,x+44,y+33),fill=c,width=3)
    elif kind == 'cyclone':
        for box in [(x+4,y+4,x+42,y+42),(x+10,y+10,x+36,y+36),(x+16,y+16,x+30,y+30)]: d.arc(box,30,320,fill=c,width=2)
        d.ellipse((x+21,y+21,x+25,y+25),fill=RED)
    elif kind == 'chart':
        d.line((x+5,y+5,x+5,y+40,x+43,y+40),fill=c,width=2); d.line((x+9,y+12,x+20,y+17,x+28,y+15,x+39,y+31),fill=RED,width=3); d.polygon([(x+39,y+31),(x+32,y+28),(x+37,y+24)],fill=RED)
    elif kind == 'frame':
        d.rectangle((x+4,y+5,x+42,y+39),outline=c,width=3); d.ellipse((x+14,y+12,x+30,y+28),outline=RED,width=2); d.line((x+17,y+26,x+29,y+14),fill=RED,width=2); d.ellipse((x+29,y+9,x+33,y+13),fill=c)
    elif kind == 'satellite':
        d.rectangle((x+17,y+15,x+29,y+29),outline=c,width=2); d.rectangle((x+2,y+13,x+15,y+31),outline=RED,width=2); d.rectangle((x+31,y+13,x+44,y+31),outline=RED,width=2); d.line((x+29,y+22,x+39,y+7),fill=c,width=2); d.arc((x+33,y+3,x+45,y+15),180,300,fill=c,width=2)
    elif kind == 'vault':
        d.rectangle((x+4,y+4,x+42,y+42),outline=c,width=2); d.ellipse((x+18,y+18,x+28,y+28),fill=RED)
        for a in (0,120,240):
            import math
            cx,cy=x+23,y+23; pts=[]
            for off in (-48,48):
                ang=math.radians(a+off); pts.append((cx+15*math.cos(ang),cy+15*math.sin(ang)))
            d.pieslice((cx-15,cy-15,cx+15,cy+15),a-48,a+48,fill='#E8B4A9')
        d.ellipse((x+19,y+19,x+27,y+27),fill=INK)
    elif kind == 'rocket':
        d.ellipse((x+16,y+5,x+31,y+35),outline=c,width=2); d.ellipse((x+20,y+12,x+27,y+20),outline=RED,width=2); d.polygon([(x+16,y+26),(x+7,y+36),(x+18,y+33)],fill=RED); d.polygon([(x+30,y+26),(x+39,y+36),(x+28,y+33)],fill=RED); d.polygon([(x+20,y+35),(x+24,y+44),(x+27,y+35)],fill='#B8860B')
    elif kind == 'ballot':
        d.rectangle((x+4,y+17,x+42,y+40),outline=c,width=2); d.line((x+15,y+17,x+31,y+17),fill=RED,width=3); d.rectangle((x+18,y+5,x+29,y+22),fill='#FFFFFF',outline=c); d.line((x+20,y+13,x+23,y+16,x+28,y+9),fill=RED,width=2)
    elif kind == 'chip':
        d.rectangle((x+11,y+11,x+35,y+35),outline=c,width=2); d.rectangle((x+17,y+17,x+29,y+29),outline=RED,width=2)
        for p in (15,21,27,33):
            d.line((x+p-4,y+5,x+p-4,y+11),fill=c,width=2); d.line((x+p-4,y+35,x+p-4,y+41),fill=c,width=2); d.line((x+5,y+p-4,x+11,y+p-4),fill=c,width=2); d.line((x+35,y+p-4,x+41,y+p-4),fill=c,width=2)
    elif kind == 'scales':
        d.line((x+24,y+6,x+24,y+39),fill=c,width=2); d.line((x+12,y+12,x+36,y+12),fill=c,width=2)
        d.line((x+12,y+12,x+7,y+26),fill=c,width=2); d.line((x+36,y+12,x+41,y+26),fill=c,width=2)
        d.arc((x+2,y+22,x+12,y+31),0,180,fill=RED,width=2); d.arc((x+36,y+22,x+46,y+31),0,180,fill=RED,width=2)
        d.line((x+17,y+39,x+31,y+39),fill=c,width=3); d.line((x+20,y+35,x+28,y+35),fill=c,width=2)

data = json.loads((ROOT/'stories.json').read_text(encoding='utf-8'))
total = len(data['cards']) + len(data['briefs'])
regions = {r: sum(x['region']==r for x in data['cards']+data['briefs']) for r in ORDER}
# Masthead
centered('THE WORLD IN ONE IMAGE', 8, font(21, True), INK)
date = 'THURSDAY 19 NOVEMBER 2026'; df = font(63, True)
while d.textlength(date, font=df) > 996: df = font(df.size-1, True)
centered(date, 34, df, INK)
sub = f"{total} STORIES · {sum(v > 0 for v in regions.values())} REGIONS · 10 FIELDS — everything below happened, or was first reported, today"
sf = font(16, False)
while d.textlength(sub, font=sf) > 996: sf = font(sf.size-1, False)
centered(sub, 103, sf, MUTED)
d.rectangle((13,128,1011,131),fill=RED)

# Twelve lead cards
for i, card in enumerate(data['cards']):
    col, row = i%4, i//4
    x, y, cw, ch = 13+col*251, 140+row*137, 240, 130
    d.rounded_rectangle((x,y,x+cw,y+ch),radius=5,fill='#FFFFFF',outline=BORDER,width=1)
    d.rectangle((x+1,y+1,x+cw-1,y+6),fill=REGION_COLORS[card['region']])
    icon(card['icon'],x+8,y+13)
    d.text((x+cw-27,y+9),str(card['n']),font=font(14,True),fill=RED)
    hf, hl = fit_lines(card['headline'],15,True,136,3,11)
    yy=y+14
    for line in hl: d.text((x+68,yy),line,font=hf,fill=INK); yy += hf.size+2
    detail_top=max(y+65, yy+3)
    df, dl = fit_lines(card['detail'],12,False,cw-16,4,9)
    line_h=df.size+2
    while len(dl)*line_h > y+ch-7-detail_top and df.size>9:
        df,dl=fit_lines(card['detail'],df.size-1,False,cw-16,4,9); line_h=df.size+2
    for line in dl[:4]: d.text((x+8,detail_top),line,font=df,fill=MUTED); detail_top += line_h

# Region summary
region_line = 'WHERE IT HAPPENED — ' + ' · '.join(f'{r} {regions[r]}' for r in ORDER)
rf=font(14,True)
while d.textlength(region_line,font=rf)>998: rf=font(rf.size-1,True)
d.text((13,550),region_line,font=rf,fill=INK)

# Briefs, filled down columns as specified
briefs=data['briefs']; cols=3; per=(len(briefs)+cols-1)//cols
d.text((13,579),f"MORE OF THE DAY — {len(briefs)} BRIEFS",font=font(17,True),fill=INK)
for col in range(cols):
    x=13+col*333
    for row in range(per):
        idx=col*per+row
        if idx>=len(briefs): continue
        item=briefs[idx]; number=13+idx
        y=607+row*20
        nf=font(11,True); d.text((x,y),str(number)+'.',font=nf,fill=RED)
        tf, lines=fit_lines(item['text'],10,False,294,2,9)
        line_h=10
        for j,line in enumerate(lines[:3]): d.text((x+24,y+j*line_h),line,font=tf,fill=INK)

# Numbers band
d.text((13,875),'THE DAY IN NUMBERS',font=font(15,True),fill=INK)
for i,(value,caption) in enumerate(data['numbers']):
    x=13+i*166
    d.text((x,893),value,font=font(19,True),fill=RED)
    cf=font(9,False)
    for j,line in enumerate(wrap(caption,cf,154)[:2]): d.text((x,917+j*11),line,font=cf,fill=MUTED)

# Date check panel
d.rectangle((13,949,1011,1014),fill='#FDF0EE',outline=RED,width=2)
d.text((21,954),'DATE CHECK — CHECKED AND LEFT OUT AS NOT 19 NOVEMBER NEWS:',font=font(12,True),fill=INK)
checkfont=font(10,False)
checklines=wrap(data['date_check'],checkfont,974)
while len(checklines)>3 and checkfont.size>9:
    checkfont=font(checkfont.size-1,False); checklines=wrap(data['date_check'],checkfont,974)
for j,line in enumerate(checklines[:3]): d.text((21,975+j*12),line,font=checkfont,fill=INK)

im.save(ROOT/'entry.png',format='PNG',optimize=True)
