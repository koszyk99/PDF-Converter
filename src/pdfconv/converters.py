import subprocess
import shutil
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

def convert_office(src: Path, out_dir: Path) -> Path:
    soffice_path = shutil.which("soffice")
    if soffice_path is None:
        raise RuntimeError("LibreOffice 'soffice' command not found. Please install LibreOffice.")
    if not src.exists():
        raise FileNotFoundError(f"Source file '{src}' does not exist.")
    out_path = out_dir / (src.stem + ".pdf")
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [soffice_path, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(src)],
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"LibreOffice conversion failed: {e.stderr.strip()}") from e
    if not out_path.exists():  
        raise RuntimeError(f"LibreOffice conversion did not produce output file '{out_path}'.")
    return out_path

CONVERTERS = {
    ".png": convert_image,
    ".jpg": convert_image,
    ".jpeg": convert_image,
    ".txt": convert_text,
    ".docx": convert_office,
}

def convert_file(src: Path, out_dir: Path) -> Path:
    suffix = src.suffix.lower()
    converter = CONVERTERS.get(suffix)
    if converter is None:
        raise ValueError(f"No converter available for file type '{suffix}'")
    return converter(src, out_dir)