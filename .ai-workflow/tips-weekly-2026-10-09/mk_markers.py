"""Draw the 1-2-3 callout markers into the Material Kitchen after crop."""
from PIL import Image, ImageDraw, ImageFont
U='/mnt/user-data/uploads/koolestpro-cowork-v2/outputs/cro-fixes/'
im=Image.open(U+'materialkitchen_after_phone.png').convert('RGB').crop((0,0,780,1700))
d=ImageDraw.Draw(im); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',46)
for n,y in [(1,1145),(2,1290),(3,1600)]:
    x,r=735,38
    d.ellipse((x-r,y-r,x+r,y+r),fill='#FF9500',outline='#0B0B0D',width=6)
    d.text((x,y+2),str(n),font=f,fill='#0B0B0D',anchor='mm')
im.save('ev/mk_after.jpg',quality=90)
