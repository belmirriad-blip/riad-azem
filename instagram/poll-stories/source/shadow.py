import cv2, numpy as np
from PIL import Image
P=60
for i in (1,2):
    c=np.array(Image.open(f'cut{i}.png')).astype(np.float32)
    h,w=c.shape[:2]; H,Wd=h+2*P,w+2*P
    a=np.zeros((H,Wd),np.float32); a[P:P+h,P:P+w]=c[...,3]/255
    M=np.float32([[1,0,0],[0,1,14]]); s1=cv2.warpAffine(a,M,(Wd,H)); s1=cv2.GaussianBlur(s1,(0,0),18)*0.30
    M2=np.float32([[1,0,0],[0,1,4]]); s2=cv2.GaussianBlur(cv2.warpAffine(a,M2,(Wd,H)),(0,0),4)*0.22
    sh=1-(1-s1)*(1-s2)
    rgb=np.zeros((H,Wd,3),np.float32); rgb[:]=(0x15,0x12,0x0F)
    rgb[P:P+h,P:P+w]=np.where(c[...,3:]>0,c[...,:3],rgb[P:P+h,P:P+w])
    fa=a+sh*(1-a)
    # composite colour: premult
    col=(c_:=np.zeros_like(rgb)); col[:]=(0x15,0x12,0x0F)
    full=np.zeros_like(rgb); full[P:P+h,P:P+w]=c[...,:3]
    out=(full*a[...,None]+col*(sh*(1-a))[...,None])/np.maximum(fa,1e-4)[...,None]
    Image.fromarray(np.dstack([out,fa*255]).clip(0,255).astype(np.uint8)).save(f'hoodie{i}.png')
# preview on bone
imgs=[Image.open(f'hoodie{i}.png') for i in (1,2)]
Wt=sum(x.width for x in imgs)+60; Ht=max(x.height for x in imgs)+40
bg=Image.new('RGBA',(Wt,Ht),(0xF1,0xEB,0xE0,255)); x=20
for im in imgs: bg.alpha_composite(im,(x,20)); x+=im.width+20
bg.convert('RGB').save('cleaned_preview.png')
