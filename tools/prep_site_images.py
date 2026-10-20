"""Crop TutorDA's own website images (assets/site) to 1080x1920 portrait plates for the brand reel.
Each plate: crop centre (fraction of width), vertical span, exposure; mild sharpen after the upscale."""
from PIL import Image, ImageFilter, ImageEnhance
import os
S = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "site")
PLATES = {  # name: (file, centre_x, y0, y1, brightness)
    "hook":    ("tutorda_image_13.jpeg", 0.30, 0.09, 0.91, 0.55),
    "sphere":  ("tutorda_image_1.jpeg",  0.30, 0.0, 1.0, 0.75),
    "teacher": ("tutorda_image_2.jpeg",  0.33, 0.0, 1.0, 0.85),
    "phone":   ("tutorda_image_11.jpeg", 0.29, 0.0, 1.0, 0.75),
    "medal":   ("tutorda_image_15.jpeg", 0.31, 0.0, 1.0, 0.5),
    "lectures":("tutorda_image_14.jpeg", 0.30, 0.0, 1.0, 0.6),
}
for name, (f, cx, y0, y1, br) in PLATES.items():
    im = Image.open(os.path.join(S, f)).convert("RGB"); W, H = im.size
    top, bot = int(y0 * H), int(y1 * H); h = bot - top; w = int(h * 9 / 16)
    left = int(min(max(cx * W - w / 2, 0), W - w))
    im = im.crop((left, top, left + w, bot)).resize((1080, 1920), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    im = ImageEnhance.Brightness(im).enhance(br)
    im.save(os.path.join(S, "crops", name + ".jpg"), quality=93)
    print(name, f"{w}x{h} -> 1080x1920 (x{1080 / w:.2f})")
