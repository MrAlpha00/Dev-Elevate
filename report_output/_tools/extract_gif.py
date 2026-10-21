import os, sys
from PIL import Image, ImageSequence

outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)

for src in sys.argv[2:]:
    im = Image.open(src)
    n = getattr(im, "n_frames", 1)
    print(os.path.basename(src), "frames:", n, "size:", im.size)
    if n == 1:
        im.convert("RGB").save(os.path.join(outdir, os.path.splitext(os.path.basename(src))[0] + "_f0.png"))
        continue
    # sample up to 8 frames evenly
    idxs = sorted(set([0, n//8, n//4, 3*n//8, n//2, 5*n//8, 3*n//4, 7*n//8, n-1]))
    for k, i in enumerate(idxs):
        im.seek(i)
        fr = im.convert("RGB")
        fr.save(os.path.join(outdir, f"{os.path.splitext(os.path.basename(src))[0]}_{i:04d}.png"))
    print("  saved samples:", idxs)
