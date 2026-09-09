# Miscellaneous Tools

A collection of small, standalone Python utilities.

## Tools

| Script | Description | Dependencies |
|--------|-------------|--------------|
| `qr_reader.py` | Decode QR codes from images or PDFs (OpenCV-based, supports multi-QR) | `opencv-python-headless`, `PyMuPDF`, `numpy` |
| `qr_reader_lite.py` | Lightweight QR decoder (~8MB vs ~200MB) | `pyzbar`, `pypdfium2`, `pillow` |
| `QRCodeGen.py` | Generate QR code PNGs from text/URLs | `qrcode[pil]` |
| `compress_images.py` | Batch-compress images to WebP with optional downscaling | `pillow` |
| `TeamGen.py` | Randomly split people into teams of a given size | None |
| `SubEncrypt.py` | Monoalphabetic substitution cipher (encrypt/decrypt) | None |
| `nfctest.py` | Verify an NFC reader is detected | `nfcpy` |

## Setup

```bash
uv sync          # install all deps from pyproject.toml
# or
pip install -r requirements.txt
```

Each script also lists its own dependencies in its docstring header.
