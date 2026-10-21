from PIL import Image, ImageDraw
U='/mnt/user-data/uploads/koolestpro-cowork-v2/outputs/cro-fixes/'
O='#FF9500'
def box(img, rects, w=7, r=18):
    d=ImageDraw.Draw(img)
    for (x0,y0,x1,y1) in rects:
        d.rounded_rectangle((x0,y0,x1,y1), radius=r, outline=O, width=w)
    return img
def save(img,name): img.convert('RGB').save('ev/'+name, quality=88); print(name, img.size)
# MK before/after
save(Image.open(U+'materialkitchen_before_popup.png').crop((0,0,780,1560)),'mk_before.jpg')
save(Image.open(U+'materialkitchen_after_phone.png').crop((0,0,780,1700)),'mk_after.jpg')
# Gainful leak 1: two 25% offers
g=Image.open(U+'_gainful_before_raw.png').convert('RGB')
c=g.crop((0,0,780,470)); box(c,[(6,4,774,72),(6,210,774,272)]); save(c,'gainful_offers.jpg')
# Gainful leak 4: tiny price
c=g.crop((0,290,780,720)); box(c,[(452,400-290-6,728,462-290)]); save(c,'gainful_price.jpg')
# Obvi leak 2: headline
o=Image.open(U+'_obvi_before_raw.png').convert('RGB')
c=o.crop((0,260,780,700)); box(c,[(120,388-260,660,468-260)]); save(c,'obvi_headline.jpg')
# Obvi leak 3: widget on CTA
c=o.crop((0,690,560,960)); d=ImageDraw.Draw(c); d.ellipse((90-56,843-690-56,90+56,843-690+56),outline=O,width=7); save(c,'obvi_widget.jpg')
# Allbirds found page
a=Image.open('/home/claude/work/found/allbirds_v2.png').convert('RGB')
print(a.size)
c=a.crop((0,110,1170,1034)); box(c,[(205,655,585,746)],w=9,r=40); save(c,'allbirds_price.jpg')  # 2026-10-09 v2: taller crop fills the freed label space
# NOTE: mk_after.jpg is then redrawn with numbered markers by mk_markers.py
