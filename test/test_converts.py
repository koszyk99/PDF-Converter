from PIL import Image
from pdfconv.converters import convert_image, convert_text

def test_convert_image_creates_pdf(tmp_path):
    # Create a temporary image file
    img_path = tmp_path / "test_image.png"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(img_path)

    # Convert the image to PDF
    out_dir = tmp_path / "output"
    pdf_path = convert_image(img_path, out_dir)

    # Check if the PDF file was created
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"

    # Check that the file really is a PDF
    assert pdf_path.read_bytes().startswith(b"%PDF")

def test_convert_text_creates_pdf(tmp_path):
    # Create a temporary XML file
    xml_path = tmp_path / "test_file.xml"
    xml_path.write_text("<a><b>zażółć</b></a>", encoding="utf-8")

    # Convert it to PDF
    out_dir = tmp_path / "output"
    pdf_path = convert_text(xml_path, out_dir)

    # Check the result
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"
    assert pdf_path.read_bytes().startswith(b"%PDF")


def test_convert_image_handles_transparency(tmp_path):
    # Create a temporary image file
    img_path = tmp_path / "test_image.png"
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))  # Red color with transparency
    img.save(img_path)

    # Convert the image to PDF
    out_dir = tmp_path / "output"
    pdf_path = convert_image(img_path, out_dir)

    # Check if the PDF file was created
    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"

    # Check that the file really is a PDF
    assert pdf_path.read_bytes().startswith(b"%PDF")