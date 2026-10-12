#!/usr/bin/env python3
# Chuyen .vlw thanh header C (mang PROGMEM) cho TFT_eSPI loadFont(array)
import sys
vlw, name, out = sys.argv[1], sys.argv[2], sys.argv[3]
d=open(vlw,"rb").read()
with open(out,"w") as f:
    f.write('// Font tu dong sinh tu Be Vietnam Pro (OFL). Khong sua tay.\n')
    f.write('// Nguon: ofl/bevietnampro, tao bang tools/vnfont/make_vlw.py\n')
    f.write('#pragma once\n#include <pgmspace.h>\n#include <stdint.h>\n\n')
    f.write(f'const uint8_t {name}[] PROGMEM = {{\n')
    for i in range(0,len(d),16):
        f.write('  '+','.join(str(b) for b in d[i:i+16])+',\n')
    f.write('};\n')
    f.write(f'const uint32_t {name}_len = {len(d)};\n')
print(f"{out}: {len(d)} bytes -> {name}[]")
