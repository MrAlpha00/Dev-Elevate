import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1])
print("PAGES", len(r.pages))
for i, p in enumerate(r.pages):
    try:
        mb = p.mediabox
        print(f"--- page {i+1} size {float(mb.width):.0f}x{float(mb.height):.0f}")
    except Exception as e:
        print("size err", e)
    try:
        t = p.extract_text() or ""
    except Exception as e:
        t = f"[extract error {e}]"
    print(t[:4000])
