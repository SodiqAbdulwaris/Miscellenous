"""
qr_reader.py

Reads an image (PNG/JPG/etc.) or a PDF, checks whether it contains a QR code,
decodes any QR codes found, and (optionally) opens the decoded value in a
web browser if it looks like a URL.

Usage:
    python3 qr_reader.py path_to_file.png
    python3 qr_reader.py path_to_file.pdf
    python3 qr_reader.py path_to_file.pdf --no-open      # decode only, don't open browser
    python3 qr_reader.py path_to_file.pdf --dpi 300      # higher render quality for PDFs

Dependencies:
    uv pip install opencv-python-headless PyMuPDF numpy
"""

import argparse
import sys
import webbrowser
from pathlib import Path

import cv2
import numpy as np

try:
    import pymupdf as fitz  # PyMuPDF, only needed for PDF input
except ImportError:
    fitz = None

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}
PDF_EXTENSIONS = {".pdf"}


def pdf_to_images(pdf_path: Path, dpi: int = 200) -> list[np.ndarray]:
    """Render every page of a PDF to an OpenCV (BGR) image array."""
    if fitz is None:
        raise RuntimeError(
            "PyMuPDF is required to read PDFs. Install it with: pip install PyMuPDF"
        )

    images = []
    zoom = dpi / 72  # PDF default is 72 DPI
    matrix = fitz.Matrix(zoom, zoom)

    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap(matrix=matrix)
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n
            )
            # Convert RGB/RGBA -> BGR for OpenCV
            if pix.n == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            elif pix.n == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images.append(img)

    return images


def load_images(path: Path, dpi: int) -> list[np.ndarray]:
    """Return a list of OpenCV images to scan, whether input is an image or PDF."""
    suffix = path.suffix.lower()

    if suffix in PDF_EXTENSIONS:
        return pdf_to_images(path, dpi=dpi)

    if suffix in IMAGE_EXTENSIONS:
        img = cv2.imread(str(path))
        if img is None:
            raise ValueError(f"Could not read image file: {path}")
        return [img]

    raise ValueError(
        f"Unsupported file type '{suffix}'. Supported: {sorted(IMAGE_EXTENSIONS | PDF_EXTENSIONS)}"
    )


def decode_qr_codes(image: np.ndarray) -> list[str]:
    """Detect and decode all QR codes in a single image. Returns list of decoded strings."""
    detector = cv2.QRCodeDetector()

    # Multi-QR detection (handles 0, 1, or many codes in one image)
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(image)

    results = []
    if retval:
        for text in decoded_info:
            if text:  # skip empty strings for codes that were located but failed to decode
                results.append(text)

    # Fallback: single-QR detector, in case multi-detect missed something
    if not results:
        text, points, _ = detector.detectAndDecode(image)
        if text:
            results.append(text)

    return results


def looks_like_url(text: str) -> bool:
    return text.strip().lower().startswith(("http://", "https://"))


def main():
    parser = argparse.ArgumentParser(description="Detect, decode, and (optionally) open QR codes from an image or PDF.")
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