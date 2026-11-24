from pathlib import Path
from PIL import Image
from xml.dom import minidom
from xml.parsers.expat import ExpatError
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Preformatted, SimpleDocTemplate

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

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

def convert_text(src: Path, out_dir: Path) -> Path:
    text = src.read_text(encoding="utf-8", errors="replace")
    if src.suffix.lower() == ".xml":
        text = _format_xml(text)
    pdfmetrics.registerFont(TTFont("DejaVuMono", FONT_PATH))
    style = ParagraphStyle("mono", fontName="DejaVuMono", fontSize=10, leading=12)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / (src.stem + ".pdf")
    doc = SimpleDocTemplate(str(out_path), pagesize=A4)
    doc.build([Preformatted(text, style)])
    return out_path