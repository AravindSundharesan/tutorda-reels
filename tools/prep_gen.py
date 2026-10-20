"""Turn generated portrait images (assets/gen/<name>.png|webp, 864x1536) into 1080x1920 plates:
<name>_plate.jpg (graded), <name>_grey.jpg (desaturated, for the 'sameness' scenes), <name>_thumb.jpg (270x480)."""
import os, sys, glob
from PIL import Image, ImageFilter, ImageEnhance
G = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "gen")
BR = {"hook": 0.62, "class": 0.7, "midnight": 0.95}
for f in sorted(glob.glob(os.path.join(G, "*.png")) + glob.glob(os.path.join(G, "*.webp"))):
    n = os.path.splitext(os.path.basename(f))[0]
    im = Image.open(f).convert("RGB").resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    g = ImageEnhance.Brightness(im).enhance(BR.get(n, 0.85)); g.save(os.path.join(G, n + "_plate.jpg"), quality=94)
    ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.15)).enhance(0.6).save(os.path.join(G, n + "_grey.jpg"), quality=92)
    g.resize((270, 480), Image.LANCZOS).save(os.path.join(G, n + "_thumb.jpg"), quality=90)
    ImageEnhance.Color(im).enhance(0.15).resize((270, 480), Image.LANCZOS).save(os.path.join(G, n + "_greythumb.jpg"), quality=90)
    print(n)
