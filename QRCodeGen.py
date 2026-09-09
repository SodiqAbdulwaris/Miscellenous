"""
QRCodeGen.py

Generate a QR code image from a given string (URL, text, etc.) and save it
as a PNG file.

Usage:
    python QRCodeGen.py "https://example.com"
    python QRCodeGen.py "Hello World" -o hello.png
    python QRCodeGen.py "https://example.com" --fill red --back white

Dependencies:
   uv pip install qrcode[pil]
"""

import argparse

import qrcode


def generate(data: str, output: str, fill: str, back: str) -> None:
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill, back_color=back)
    img.save(output)
    print(f"Saved QR code to {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("data", type=str, help="Text or URL to encode")
    parser.add_argument("-o", "--output", default="QR.png", help="Output file path (default: QR.png)")
    parser.add_argument("--fill", default="black", help="Foreground color (default: black)")
    parser.add_argument("--back", default="white", help="Background color (default: white)")
    args = parser.parse_args()

    generate(args.data, args.output, args.fill, args.back)


if __name__ == "__main__":
    main()
