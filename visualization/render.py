"""Render four tuple blocks and the exact three repair comparisons."""

import math
from itertools import combinations
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


HERE=Path(__file__).resolve().parent
W,H=704,835
BG,PANEL,EDGE="#101b32","#162640","#3b5577"
TEXT,MUTED="#f7faff","#c1cee2"
MINT,AMBER,BLUE="#6aead7","#ffd086","#adbffb"
FACTS=((1,"12"),(1,"13"),(2,"12"),(2,"23"),(3,"13"),(3,"23"),(4,"p"),(4,"q"))
CASES=((0,1,2,3,4),(0,1,2,3,6,7),(0,1,2,3,4,5))


def label(draw,xy,s,size,color=TEXT,anchor="lt"):
    draw.text(xy,s,font=ImageFont.load_default(size=size),fill=color,anchor=anchor)


def slot(draw,x,y,phase,key,selected):
    skew=13+7*math.cos(phase)
    base=[(x-36,y-22),(x+35,y-22),(x+35,y+22),(x-36,y+22)]
    cap=[(x-36,y-22),(x-36+skew,y-33),(x+35+skew,y-33),(x+35,y-22)]
    side=[(x+35,y-22),(x+35+skew,y-33),(x+35+skew,y+11),(x+35,y+22)]
    for poly,color in zip((cap,side,base),("#497b91","#365674","#254d69") if selected else ("#3a4d6a","#283a56","#24324d")):
        draw.polygon(poly,fill=color,outline="#152540")
    label(draw,(x,y),key,29,TEXT if selected else MUTED,"mm")


def plot(draw, phase, held):
    shift=7*math.sin(phase)
    xs=[122,271,420,569]
    coords=[(x+(1 if i==0 else -1)*shift,356+i*104+(j-1.5)*shift) for j,x in enumerate(xs) for i in range(2)]
    for (i,(b,c)),(j,(d,e)) in combinations(enumerate(FACTS),2):
        if c==e and i in held and j in held:
            (x,y),(u,v)=coords[i],coords[j]
            bend=34 if abs(i-j)>3 else 20
            path=[]
            for k in range(25):
                t=k/24
                path.append((x+t*(u-x),y+t*(v-y)-bend*math.sin(math.pi*t)))
            draw.line(path,fill=MINT,width=4)
    for i,(x,y) in enumerate(coords):
        slot(draw,x,y,phase,FACTS[i][1],i in held)
    for j,x in enumerate(xs):
        label(draw,(x,534),str(j+1),29,TEXT,"mt")


def frame(phase,index):
    held=CASES[index]
    selected=[FACTS[i] for i in held]
    b=sum(x[0]!=y[0] for x,y in combinations(selected,2))
    c=sum(x[1]!=y[1] for x,y in combinations(selected,2))
    deleted=640*(8-len(selected))
    total=deleted+128*b+c
    assert total==(2952,2830,2828)[index]
    im=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(im)
    label(d,(36,38),"SOFT FUNCTIONAL DEPENDENCIES",24,MINT)
    label(d,(34,83),"Which blocks win?",56)
    label(d,(36,159),"Each vertex has a two-fact block.",29,MUTED)
    d.rounded_rectangle((32,215,672,584),21,fill=PANEL,outline=EDGE,width=2)
    label(d,(55,240),"LINKS JOIN RETAINED EQUAL C VALUES",21,MINT)
    label(d,(55,284),"C labels inside blocks",25,MUTED)
    plot(d,phase,held)
    d.rounded_rectangle((32,604,672,804),21,fill=PANEL,outline=EDGE,width=2)
    name=("One block is partial","Three full blocks","Triangle blocks")[index]
    label(d,(55,624),name,32,MINT if index==2 else TEXT)
    label(d,(647,624),f"Cost {total:,}",32,MINT if index==2 else AMBER,"rt")
    label(d,(55,683),f"Deletion {deleted:,}  +  B cost {128*b:,}",27,MUTED)
    label(d,(55,747),f"C cost {c}  |  Shared labels {math.comb(len(held),2)-c}",27,TEXT)
    return im.convert("P",palette=Image.Palette.ADAPTIVE,colors=64)


def main():
    total=72
    frames=[frame(2*math.pi*i/total,i//24) for i in range(total)]
    frames[0].save(HERE/"soft-blocks.gif",save_all=True,append_images=frames[1:],
                   loop=0,duration=185,optimize=True)
    with ZipFile(HERE/"soft-blocks-explorer.zip","w") as archive:
        for name in ("README.md","index.html"):
            info=ZipInfo(name,(1980,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            archive.writestr(info,(HERE/name).read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__=="__main__":
    main()
