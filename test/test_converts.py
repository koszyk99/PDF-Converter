from PIL import Image

from pdfconv.converters import convert_image

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