"""Editorial grade for generated photos: gentle desaturation, warm mids, lifted blacks, fine grain.
Writes <name>_ed.jpg (colour) and <name>_edgrey.jpg (near-monochrome) and <name>_edgreythumb.jpg."""
import os, glob
import numpy as np
from PIL import Image, ImageFilter
G = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "gen")
rng = np.random.default_rng(1)
def grade(im, sat=0.82, grey=False):
    a = np.asarray(im).astype(np.float32) / 255
    l = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])[..., None]
    a = l + (a - l) * (0.08 if grey else sat)
    a = 0.035 + a * 0.95                                   # lift blacks, soften whites
    if not grey: a = a * np.array([1.03, 1.0, 0.96])       # warm
    a = a + rng.normal(0, 0.012, a.shape[:2])[..., None]  # fine monochrome grain
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
for f in sorted(glob.glob(os.path.join(G, "*.png")) + glob.glob(os.path.join(G, "*.webp"))):
    n = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert("RGB").resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.4, percent=45, threshold=2))
    grade(im).save(os.path.join(G, n + "_ed.jpg"), quality=94)
    g = grade(im, grey=True); g.save(os.path.join(G, n + "_edgrey.jpg"), quality=92)
    g.resize((270, 480), Image.LANCZOS).save(os.path.join(G, n + "_edgreythumb.jpg"), quality=90)
    print(n)
