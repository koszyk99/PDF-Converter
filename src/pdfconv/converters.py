from pathlib import Path

from PIL import Image


def convert_image(src: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (src.stem + ".pdf")
    Image.open(src).convert("RGB").save(out_path)
    return out_path