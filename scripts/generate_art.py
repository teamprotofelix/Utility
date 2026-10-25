"""Create original futuristic artwork locally and store it as optimized WebP.
Requires: pillow, numpy. No external assets or network usage.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np
import math, random
random.seed(2026)
BASE = Path(__file__).resolve().parents[1] / 'assets'
BASE.mkdir(parents=True,exist_ok=True)


def background(w,h,seed=0,bright=1):
    rng=np.random.default_rng(seed)
    y,x=np.mgrid[0:h,0:w].astype(np.float32)
    arr=np.zeros((h,w,3),dtype=np.float32)
    for i,v in enumerate((6,15,28)):arr[:,:,i]=v
    for cx,cy,r,rgba in [(w*.51,h*.52,w*.55,(11,69,87)),(w*.81,h*.19,w*.46,(27,16,74)),(w*.1,h*.75,w*.3,(5,38,59))]:
        f=np.maximum(0,1-np.sqrt(((x-cx)/r)**2+((y-cy)/r)**2))**2*bright
        for i in range(3):arr[:,:,i]+=f*rgba[i]
    noise=rng.normal(0,.9,(h,w,1))
    arr=np.clip(arr+noise,0,255).astype('uint8')
    return Image.fromarray(arr,'RGB').convert('RGBA')

def strokes(img, lines, color, width=2, blur=11, alpha=110):
    L=Image.new('RGBA',img.size);d=ImageDraw.Draw(L)
    for pts in lines: d.line(pts,fill=(*color,alpha),width=width,joint='curve')
    g=L.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(g);img.alpha_composite(L)

def light_circle(img,box,color,width=2,glow=9,start=0,end=360,rot=0):
    layer=Image.new('RGBA',img.size)
    d=ImageDraw.Draw(layer)
    d.arc(box,start,end,fill=(*color,215),width=width)
    if rot:layer=layer.rotate(rot,Image.Resampling.BICUBIC,center=((box[0]+box[2])/2,(box[1]+box[3])/2))
    blur=layer.filter(ImageFilter.GaussianBlur(glow)); blur.putalpha(blur.getchannel('A').point(lambda x:int(x*.52)))
    img.alpha_composite(blur);img.alpha_composite(layer)

def dot(img,x,y,r,color,opacity=220):
    dr=ImageDraw.Draw(img)
    dr.ellipse((x-r,y-r,x+r,y+r), fill=(*color,opacity))

def starfield(img,n=100):
    w,h=img.size;d=ImageDraw.Draw(img)
    for i in range(n):
        x=random.randrange(w);y=random.randrange(h);r=random.choice([0,0,0,1]);v=random.randrange(40,120)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(91,198,229,v))

def grid(img,space=46):
    w,h=img.size;d=ImageDraw.Draw(img)
    for x in range(0,w,space): d.line([(x,0),(x,h)],fill=(53,147,173,17))
    for y in range(0,h,space): d.line([(0,y),(w,y)],fill=(53,147,173,17))

def panel(img,poly,fill=(22,52,68,185),line=(94,219,220,160)):
    d=ImageDraw.Draw(img);d.polygon(poly,fill=fill);d.line(poly+[poly[0]],fill=line,width=2)

def save(img,name,q=58):
    img.convert('RGB').save(BASE/name,'WEBP',quality=q,method=6)
    print(name,(BASE/name).stat().st_size)

def hero():
    w,h=780,730;im=background(w,h,11,1.4);grid(im,52);starfield(im,125)
    cx,cy=385,365
    for r,c in [(274,(37,96,118)),(232,(55,153,167)),(190,(69,162,205))]:
        light_circle(im,(cx-r,cy-r,cx+r,cy+r),c,1,2,0,360)
    light_circle(im,(cx-300,cy-200,cx+300,cy+200),(81,226,219),4,14,15,156,-19)
    light_circle(im,(cx-300,cy-200,cx+300,cy+200),(120,125,245),3,10,181,290,-19)
    light_circle(im,(cx-210,cy-325,cx+210,cy+325),(85,196,255),2,7,44,250,31)
    light_circle(im,(cx-260,cy-93,cx+260,cy+93),(80,229,210),2,5,12,148,-22)
    light_circle(im,(cx-196,cy-196,cx+196,cy+196),(99,169,240),3,8,35,152)
    light_circle(im,(cx-196,cy-196,cx+196,cy+196),(132,100,255),3,8,187,311)
    # ambient halo and opaque central dark optical lens
    lens=Image.new('RGBA',im.size); ld=ImageDraw.Draw(lens)
    ld.ellipse((cx-151,cy-151,cx+151,cy+151),fill=(6,25,45,220),outline=(66,156,188,205),width=3)
    im.alpha_composite(lens)
    for k in range(5):light_circle(im,(cx-146+k*14,cy-146+k*14,cx+146-k*14,cy+146-k*14),(39+6*k,92+14*k,131+15*k),2,3,25,345)
    # isometric frame central: impossible polygon hologram
    p1=[(cx,cy-103),(cx+104,cy-50),(cx+104,cy+63),(cx,cy+116),(cx-104,cy+63),(cx-104,cy-50)]
    panel(im,p1,fill=(11,38,63,175),line=(90,227,230,230))
    strokes(im, [[p1[i],p1[(i+1)%6]] for i in range(6)],(64,232,223),3,12)
    for step in range(5):
        f=1-step*.145
        pts=[(int(cx+(x-cx)*f),int(cy+(y-cy)*f)) for x,y in p1]
        ImageDraw.Draw(im).line(pts+[pts[0]],fill=(91,172,230,170-step*20),width=1)
    ds=ImageDraw.Draw(im)
    ds.line([(cx,cy-103),(cx,cy+116)],fill=(105,218,230,140),width=2)
    ds.line([(cx-104,cy-50),(cx+104,cy+63)],fill=(117,219,249,85),width=2)
    ds.line([(cx+104,cy-50),(cx-104,cy+63)],fill=(117,219,249,85),width=2)
    for rad in (43,66):
        light_circle(im,(cx-rad,cy-rad,cx+rad,cy+rad),(83,245,227),2,8,80,330)
    # central energetic spark
    strokes(im,[[(cx-12,cy),(cx+12,cy)],[(cx,cy-12),(cx,cy+12)]],(134,249,248),2,14,220)
    d=ImageDraw.Draw(im); d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=(199,255,247,255))
    for ang,rad in [(36,260),(126,213),(217,277),(303,226)]:
        x=cx+math.cos(math.radians(ang))*rad;y=cy+math.sin(math.radians(ang))*rad
        dot(im,x,y,4,(113,248,236));d.line([(x,y),(x+20,y-21)],fill=(92,199,211,140),width=1)
        d.line([(x+20,y-21),(x+61,y-21)],fill=(92,199,211,90),width=1)
    for x in (67,689):
        for y in range(102,620,24):d.line([(x,y),(x+8,y)],fill=(89,192,229,75),width=1)
    save(im,'hero-core.webp',56)

def card():
    w,h=880,500;im=background(w,h,13,1.4);grid(im,50);starfield(im,85)
    d=ImageDraw.Draw(im)
    # sweeping perspective traces
    for i in range(16):
        x=25+i*48;d.line([(x,480),(440+(x-440)*.25,95)],fill=(40,151,180,40),width=1)
    # multiple floating, tilted folder tiles
    def tile(cx,cy,scale,primary=False):
        tw=210*scale;th=235*scale
        pts=[(cx-tw*.5,cy-th*.5),(cx+tw*.5,cy-th*.5-28*scale),(cx+tw*.5,cy+th*.5-28*scale),(cx-tw*.5,cy+th*.5)]
        panel(im,pts,fill=(15,40,64,235),line=((103,229,230,220) if primary else (111,126,218,155)))
        dp=ImageDraw.Draw(im)
        inside=[(cx-tw*.42,cy-th*.37),(cx+tw*.42,cy-th*.41-21*scale),(cx+tw*.42,cy+th*.14-21*scale),(cx-tw*.42,cy+th*.18)]
        dp.polygon(inside,fill=(15,84,109,170))
        # miniature mountain/picture silhouettes
        dp.polygon([(cx-tw*.42,cy+th*.16),(cx-tw*.06,cy-th*.18),(cx+tw*.19,cy+th*.03),(cx+tw*.42,cy-th*.09),(cx+tw*.42,cy+th*.14)],fill=(69,173,198,200))
        dp.ellipse((cx+tw*.15,cy-th*.3,cx+tw*.3,cy-th*.18),fill=(133,225,231,220))
        for j in range(3):
            y=cy+th*(.29+j*.105)
            dp.line([(cx-tw*.36,y),(cx+tw*(.19 if j==2 else .36),y-15*scale)],fill=(94,176,206,140),width=max(1,int(2*scale)))
        return pts
    tile(223,225,.96)
    tile(478,205,1.1,True)
    tile(712,250,.8)
    # analysis links and floating small glowy badges
    strokes(im,[[(320,232),(363,232)],[(592,234),(643,234)]],(106,232,226),4,10,180)
    for x,y in [(343,232),(619,234)]:
        light_circle(im,(x-17,y-17,x+17,y+17),(94,247,219),3,8)
        d.ellipse((x-3,y-3,x+3,y+3),fill=(178,255,249,255))
    save(im,'imgcomp-media.webp',57)

def future_network():
    w,h=520,300;im=background(w,h,24,1.1);grid(im,44);d=ImageDraw.Draw(im)
    cx,cy=256,154
    nodes=[]
    for i in range(18):
        a=i*2*math.pi/18;rad=(92 if i%2 else 122)
        nodes.append((int(cx+math.cos(a)*rad*1.6),int(cy+math.sin(a)*rad*.93)))
    lines=[]
    for i,p in enumerate(nodes):
        lines.append([p,nodes[(i+5)%len(nodes)]])
        if i%2==0:lines.append([p,(cx,cy)])
    strokes(im,lines,(85,197,240),1,6,100)
    for i,(x,y) in enumerate(nodes):dot(im,x,y,3 if i%4 else 6,(91,233,228),180)
    light_circle(im,(cx-67,cy-67,cx+67,cy+67),(113,164,247),3,9,10,298)
    panel(im,[(cx,cy-55),(cx+52,cy-25),(cx+52,cy+32),(cx,cy+61),(cx-52,cy+32),(cx-52,cy-25)],fill=(12,50,77,212),line=(94,222,224,185))
    save(im,'future-network.webp',50)

def future_grid():
    w,h=520,300;im=background(w,h,29,1);d=ImageDraw.Draw(im)
    # isometric grid landscape
    for i in range(-7,16):
        dx=i*41
        d.line([(dx,-30),(dx+230,330)],fill=(90,171,209,65),width=1)
        d.line([(dx+250,-30),(dx,330)],fill=(70,162,200,41),width=1)
    for r in (44,75,109):
        light_circle(im,(260-r*1.65,147-r*.8,260+r*1.65,147+r*.8),(97,179,237),2,7,180,343)
    strokes(im,[[(160,150),(234,96),(343,165),(262,216),(160,150)]],(75,231,231),3,12,180)
    panel(im,[(260,53),(357,102),(357,191),(260,242),(163,191),(163,102)],fill=(15,39,65,160),line=(93,207,237,220))
    for j in range(1,5):
        yy=80+j*32
        d.line([(185,yy),(333,yy)],fill=(100,222,214,105),width=1)
    save(im,'future-grid.webp',50)

def og():
    im=background(1200,630,43,1.5)
    d=ImageDraw.Draw(im)
    hero_img=Image.open(BASE/'hero-core.webp').convert('RGBA').resize((620,580))
    im.alpha_composite(hero_img,(590,32))
    try:
        font_b=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',70)
        font_s=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
    except:font_b=font_s=ImageFont.load_default()
    d.text((68,165),'UTILITY',font=font_b,fill=(219,249,248))
    d.text((68,250),'NEXUS.',font=font_b,fill=(105,232,217))
    d.text((73,388),'DIGITAL TOOLS HUB',font=font_s,fill=(146,182,204))
    d.line([(70,448),(473,448)],fill=(73,200,203),width=2)
    d.text((73,467),'util.moip.ai.kr',font=font_s,fill=(120,222,224))
    save(im,'og-cover.webp',53)

if __name__ == '__main__':
    hero();card();future_network();future_grid();og()
