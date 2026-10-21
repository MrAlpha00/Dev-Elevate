import sys, io, pymupdf
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
for f in sys.argv[1:]:
    d = pymupdf.open(f)
    t = "\n".join(p.get_text() for p in d)
    print("=" * 20, f, "pages", d.page_count, "chars", len(t))
    print(t[:2500])
    print()
