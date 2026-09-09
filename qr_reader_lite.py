#!/usr/bin/env python3
"""
qr_reader_lite.py

Lightweight version: reads an image or PDF, checks for a QR code, decodes it,
and opens it if it's a URL.

Why this is lighter than an OpenCV-based approach:
    - pyzbar (~200KB) instead of opencv-python-headless (~90MB) for decoding
    - pypdfium2 (~600KB) instead of PyMuPDF (~65MB) for PDF page rendering
    - Pillow (~7MB) instead of numpy (~40MB) for image handling
    Total: ~8MB vs ~200MB, with no accuracy trade-off for typical QR use cases.

Dependencies:
    uv pip install pyzbar pypdfium2 pillow

Note: pyzbar needs the system zbar shared library. It's preinstalled on many
Linux systems; if you get an import error, install it with:
    Ubuntu/Debian: sudo apt-get install libzbar0
    macOS:         brew install zbar
    Windows:       usually bundled with the pyzbar wheel already

Usage:
    python3 qr_reader_lite.py path/to/file.png
    python3 qr_reader_lite.py path/to/file.pdf
    python3 qr_reader_lite.py path/to/file.pdf --no-open
    python3 qr_reader_lite.py path/to/file.pdf --dpi 300
"""

import argparse
import sys
import webbrowser
from pathlib import Path

from PIL import Image
from pyzbar.pyzbar import decode as zbar_decode

try:
    import pypdfium2 as pdfium
except ImportError:
    pdfium = None

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}
PDF_EXTENSIONS = {".pdf"}


def pdf_to_images(pdf_path: Path, dpi: int = 200) -> list[Image.Image]:
    """Render every page of a PDF to a PIL Image."""
    if pdfium is None:
        raise RuntimeError(
            "pypdfium2 is required to read PDFs. Install it with: pip install pypdfium2"
        )

    scale = dpi / 72  # PDF default is 72 DPI
    images = []
    pdf = pdfium.PdfDocument(pdf_path)
    for page in pdf:
        bitmap = page.render(scale=scale)
        images.append(bitmap.to_pil())
    return images


def load_images(path: Path, dpi: int) -> list[Image.Image]:
    suffix = path.suffix.lower()

    if suffix in PDF_EXTENSIONS:
        return pdf_to_images(path, dpi=dpi)

    if suffix in IMAGE_EXTENSIONS:
        return [Image.open(path)]

    raise ValueError(
        f"Unsupported file type '{suffix}'. Supported: {sorted(IMAGE_EXTENSIONS | PDF_EXTENSIONS)}"
    )


def decode_qr_codes(image: Image.Image) -> list[str]:
    """Detect and decode all QR (and other 1D/2D barcode) symbols in an image."""
    results = zbar_decode(image)
    # Only keep QR codes; drop other barcode symbologies zbar also detects
    return [r.data.decode("utf-8", errors="replace") for r in results if r.type == "QRCODE"]


def looks_like_url(text: str) -> bool:
    return text.strip().lower().startswith(("http://", "https://"))


def main():
    parser = argparse.ArgumentParser(description="Lightweight QR code detector/decoder for images and PDFs.")
    parser.add_argument("file", type=str, help="Path to an image or PDF file")
    parser.add_argument("--dpi", type=int, default=200, help="Render DPI for PDF pages (default: 200)")
    parser.add_argument("--no-open", action="store_true", help="Don't open decoded URLs in a browser")
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        images = load_images(path, dpi=args.dpi)
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)

    found_any = False
    for page_num, image in enumerate(images, start=1):
        decoded_values = decode_qr_codes(image)

        if not decoded_values:
            continue

        found_any = True
        page_label = f" (page {page_num})" if len(images) > 1 else ""
        for value in decoded_values:
            print(f"[QR FOUND{page_label}] {value}")

            if looks_like_url(value):
                if args.no_open:
                    print(f"  -> URL detected (not opening, --no-open set)")
                else:
                    print(f"  -> Opening in browser...")
                    webbrowser.open(value)
            else:
                print(f"  -> Not a URL, printed above as decoded text")

    if not found_any:
        print("No QR code detected in the file.")
        sys.exit(2)


if __name__ == "__main__":
    main()
