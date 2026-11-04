import cv2, numpy as np
from rembg import remove, new_session
from PIL import Image
sess=new_session('isnet-general-use')
for i in (1,2):
    im=Image.open(f'sr{i}.png').convert('RGB')
    a=np.array(remove(im,session=sess,only_mask=True,post_process_mask=True)).astype(np.float32)/255
    # clean: keep largest component, smooth edge slightly, tighten
    m=(a>0.5).astype(np.uint8); n,l,st,_=cv2.connectedComponentsWithStats(m)
    k=1+np.argmax(st[1:,4]); keep=(l==k).astype(np.uint8)
    keep=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))
    # fill holes
    ff=keep.copy(); h,w=ff.shape; mm=np.zeros((h+2,w+2),np.uint8); cv2.floodFill(ff,mm,(0,0),1); keep=keep|(1-ff)
    keep=cv2.erode(keep,np.ones((3,3),np.uint8),iterations=1)
    alpha=cv2.GaussianBlur(keep.astype(np.float32),(0,0),1.1)
    rgb=np.array(im)
    # decontaminate edge colour: replace semi-transparent edge pixels with inner colour
    inner=cv2.erode(keep,np.ones((5,5),np.uint8))
    blur=cv2.GaussianBlur(rgb.astype(np.float32)*inner[...,None],(0,0),3); wgt=cv2.GaussianBlur(inner.astype(np.float32),(0,0),3)[...,None]
    fill=blur/np.maximum(wgt,1e-3); edge=((keep>0)&(inner==0))[...,None]
    rgb=np.where(edge,fill*0.6+rgb*0.4,rgb).clip(0,255).astype(np.uint8)
    rgba=np.dstack([rgb,(alpha*255).astype(np.uint8)])
    ys,xs=np.where(alpha>0.02); rgba=rgba[ys.min():ys.max()+1,xs.min():xs.max()+1]
    Image.fromarray(rgba).save(f'cut{i}.png'); print(i,rgba.shape)
