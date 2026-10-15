# Makes the AskMed knee brace glow in the K panorama.
# usage: python3 glow.py <in.jpg> <out.jpg> <mask_preview.png>
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageDraw

src, out, mask_out = sys.argv[1:4]
im = Image.open(src).convert('RGB')
W, H = im.size

# work only inside a box around the brace
box = (440, 760, 680, 1020)
crop = im.crop(box)
a = np.asarray(crop).astype(np.int32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

navy = (b - r > 35) & (b - g > 10) & (lum < 150)          # the blue neoprene
hinge = (abs(r - g) < 18) & (abs(g - b) < 22) & (lum < 110)  # the dark grey hinge and straps
m = Image.fromarray(((navy | hinge) * 255).astype(np.uint8))

# close small gaps, then fill holes (the open kneecap stays open: it is a hole only in the fabric)
m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))

# keep the largest connected blob (flood fill from the brace centre)
seed = (m.width // 2, int(m.height * 0.55))
probe = m.copy()
cx, cy = seed
# nudge the seed onto the mask if it misses
if probe.getpixel(seed) == 0:
    arr = np.asarray(probe)
    ys, xs = np.nonzero(arr)
    k = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
    seed = (int(xs[k]), int(ys[k]))
ImageDraw.floodfill(probe, seed, 128)
blob = probe.point(lambda v: 255 if v == 128 else 0)
blob = blob.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3))

mask = Image.new('L', (W, H), 0)
mask.paste(blob, box[:2])
mask.save(mask_out)

sky = Image.new('RGB', (W, H), (47, 159, 228))
ice = Image.new('RGB', (W, H), (190, 232, 255))

# aura: a sky-blue cloud around the brace, laid over the bright room with normal blending
aura = mask.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(34))
aura = ImageChops.subtract(aura, mask)            # keep it off the product itself
aura = aura.point(lambda v: min(160, int(v * 1.55)))
outim = Image.composite(sky, im, aura)

# a tighter, brighter inner glow hugging the outline
inner = mask.filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(9))
inner = ImageChops.subtract(inner, mask).point(lambda v: min(255, int(v * 2.2)))
outim = ImageChops.screen(outim, Image.composite(ice, Image.new('RGB', (W, H), 0), inner))

# crisp rim light
rim = ImageChops.subtract(mask.filter(ImageFilter.MaxFilter(5)), mask).filter(ImageFilter.GaussianBlur(1.4))
outim = ImageChops.screen(outim, Image.composite(ice, Image.new('RGB', (W, H), 0), rim))

# lift the brace a touch so it reads as lit from within
lit = ImageChops.screen(outim, Image.composite(sky, Image.new('RGB', (W, H), 0), mask.point(lambda v: int(v * 0.28))))
outim = Image.composite(lit, outim, mask.filter(ImageFilter.GaussianBlur(1.5)))
outim.save(out, quality=93)
