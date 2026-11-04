import cv2, numpy as np, torch, torch.nn as nn, torch.nn.functional as F, sys
S='/tmp/claude-0/-home-user-riad-azem/f19ce704-8ef0-5812-85c2-f289dfb8a7eb/'
W=S+'scratchpad/work/'
class RDB(nn.Module):
    def __init__(s,f=64,g=32):
        super().__init__()
        s.conv1=nn.Conv2d(f,g,3,1,1);s.conv2=nn.Conv2d(f+g,g,3,1,1);s.conv3=nn.Conv2d(f+2*g,g,3,1,1)
        s.conv4=nn.Conv2d(f+3*g,g,3,1,1);s.conv5=nn.Conv2d(f+4*g,f,3,1,1);s.l=nn.LeakyReLU(0.2,True)
    def forward(s,x):
        x1=s.l(s.conv1(x));x2=s.l(s.conv2(torch.cat((x,x1),1)));x3=s.l(s.conv3(torch.cat((x,x1,x2),1)))
        x4=s.l(s.conv4(torch.cat((x,x1,x2,x3),1)));x5=s.conv5(torch.cat((x,x1,x2,x3,x4),1));return x5*0.2+x
class RRDB(nn.Module):
    def __init__(s):
        super().__init__();s.rdb1=RDB();s.rdb2=RDB();s.rdb3=RDB()
    def forward(s,x): return s.rdb3(s.rdb2(s.rdb1(x)))*0.2+x
class RRDBNet(nn.Module):
    def __init__(s):
        super().__init__()
        s.conv_first=nn.Conv2d(3,64,3,1,1);s.body=nn.Sequential(*[RRDB() for _ in range(23)])
        s.conv_body=nn.Conv2d(64,64,3,1,1);s.conv_up1=nn.Conv2d(64,64,3,1,1);s.conv_up2=nn.Conv2d(64,64,3,1,1)
        s.conv_hr=nn.Conv2d(64,64,3,1,1);s.conv_last=nn.Conv2d(64,3,3,1,1);s.l=nn.LeakyReLU(0.2,True)
    def forward(s,x):
        f=s.conv_first(x);f=f+s.conv_body(s.body(f))
        f=s.l(s.conv_up1(F.interpolate(f,scale_factor=2,mode='nearest')))
        f=s.l(s.conv_up2(F.interpolate(f,scale_factor=2,mode='nearest')))
        return s.conv_last(s.l(s.conv_hr(f)))
net=RRDBNet();sd=torch.load(S+'scratchpad/RealESRGAN_x4plus.pth',map_location='cpu');net.load_state_dict(sd['params_ema']);net.eval()
torch.set_num_threads(8)
def sr(bgr):
    x=torch.from_numpy(bgr[:,:,::-1].astype(np.float32)/255).permute(2,0,1)[None]
    with torch.no_grad(): y=net(x).clamp(0,1)[0].permute(1,2,0).numpy()
    return (y[:,:,::-1]*255).round().astype(np.uint8)

cfg={1:dict(crop=(12,12,237,306),box=(105,137,146,160)),2:dict(crop=(6,36,229,388),box=(105,182,132,198))}
for i,c in cfg.items():
    im=cv2.imread(S+f'images/{i}.png')
    # logo mask: bright pixels in bbox vs local fabric
    x0,y0,x1,y1=c['box']; g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY).astype(int)
    reg=g[y0:y1,x0:x1]; base=np.median(reg)
    m=np.zeros(g.shape,np.uint8); m[y0:y1,x0:x1]=(reg>base+14).astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((3,3),np.uint8),iterations=2)
    clean=cv2.inpaint(im,m,5,cv2.INPAINT_TELEA)
    cv2.imwrite(W+f'mask{i}.png',m); cv2.imwrite(W+f'inpaint{i}.png',clean)
    cx0,cy0,cx1,cy1=c['crop']; clean=clean[cy0:cy1,cx0:cx1]
    up=sr(clean)
    # light unsharp
    bl=cv2.GaussianBlur(up,(0,0),1.2); up=cv2.addWeighted(up,1.35,bl,-0.35,0)
    cv2.imwrite(W+f'sr{i}.png',up); print(i,up.shape)
