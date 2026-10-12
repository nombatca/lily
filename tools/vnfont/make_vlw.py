#!/usr/bin/env python3
# Tao font smooth TFT_eSPI (.vlw) tu file TTF, chi chua ASCII + tieng Viet.
# Dinh dang .vlw (big-endian int32):
#   header: glyphCount, version(11), fontSize, 0, ascent, descent
#   moi glyph: codepoint, height, width, xAdvance, gdY(dinh tren so voi baseline), gdX(le trai), 0
#   sau do: bitmap 8-bit alpha (width*height) cho tung glyph theo thu tu codepoint tang dan
import struct, sys
from PIL import ImageFont, Image

def vn_chars():
    base = [chr(c) for c in range(0x20, 0x7F)]  # ASCII
    vn = ("àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
          "ÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ")
    seen=set(); out=[]
    for ch in base+list(vn):
        if ch not in seen:
            seen.add(ch); out.append(ch)
    return sorted(out, key=lambda c: ord(c))

def build(ttf, px, out_path):
    font = ImageFont.truetype(ttf, px)
    ascent, descent = font.getmetrics()
    chars = vn_chars()
    metrics=[]; bitmaps=[]
    for ch in chars:
        cp = ord(ch)
        adv = round(font.getlength(ch))
        try:
            core, (ox, oy) = font.getmask2(ch)
            w, h = core.size
        except Exception:
            w=h=0; ox=oy=0; core=None
        if w==0 or h==0:
            metrics.append((cp,0,0,adv,0,0,0)); bitmaps.append(b"")
            continue
        data = bytes(core)                 # 8-bit alpha, row-major w*h
        gdY = ascent - oy                  # dinh glyph so voi baseline (duong len)
        gdX = ox
        metrics.append((cp,h,w,adv,gdY,gdX,0))
        bitmaps.append(data)
    buf = bytearray()
    buf += struct.pack(">IIIIII", len(chars), 11, px, 0, ascent, descent)
    for m in metrics:
        buf += struct.pack(">iiiiiii", *m)
    for b in bitmaps:
        buf += b
    open(out_path,"wb").write(buf)
    return len(chars), ascent, descent, len(buf)

def verify(path):
    # Doc lai y nhu TFT_eSPI va ve thu 2 glyph
    d=open(path,"rb").read(); off=0
    def ri():
        nonlocal off
        v=struct.unpack(">i", d[off:off+4])[0]; off+=4; return v
    gcount=ri(); ver=ri(); fsize=ri(); _=ri(); asc=ri(); desc=ri()
    uni=[]; H=[]; W=[]; adv=[]; dY=[]; dX=[]
    for _ in range(gcount):
        uni.append(ri()); H.append(ri()); W.append(ri()); adv.append(ri()); dY.append(ri()); dX.append(ri()); ri()
    bmp_start=off
    offs=[]; run=0
    for i in range(gcount):
        offs.append(run); run += H[i]*W[i]
    print(f"  glyphs={gcount} ver={ver} size={fsize} ascent={asc} descent={desc} bytes={len(d)}")
    for ch in ["A","ế","g"]:
        cp=ord(ch)
        if cp not in uni: 
            print(f"  {ch!r} KHONG CO"); continue
        i=uni.index(cp); b=bmp_start+offs[i]
        print(f"  {ch!r} (U+{cp:04X}) w={W[i]} h={H[i]} adv={adv[i]} dY={dY[i]} dX={dX[i]}")
        for r in range(H[i]):
            line="".join("#" if d[b+r*W[i]+c]>96 else ("." if d[b+r*W[i]+c]>0 else " ") for c in range(W[i]))
            print("    |"+line+"|")

if __name__=="__main__":
    ttf, px, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    g,a,de,n = build(ttf,px,out)
    print(f"Da tao {out}: {g} glyph, {n} bytes")
    verify(out)
