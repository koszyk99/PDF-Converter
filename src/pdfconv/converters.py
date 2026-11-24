from pathlib import Path
from PIL import Image
from xml.dom import minidom
from xml.parsers.expat import ExpatError

def convert_image(src: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (src.stem + ".pdf")
    Image.open(src).convert("RGB").save(out_path)
    return out_path

def _format_xml(text: str) -> str:
    try:
        return minidom.parseString(text.encode("utf-8")).toprettyxml(indent="  ")
    except ExpatError:
        return text