from pathlib import Path
from PIL import Image

img1 = Image.open("/home/krzkos/Pictures/Screenshots/1.png").convert("RGB")

img1.save("out.pdf")