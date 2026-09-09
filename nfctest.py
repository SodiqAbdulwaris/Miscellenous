"""
nfctest.py

Quick check that an NFC reader is detected by the nfcpy library.
Opens the first available NFC contactless frontend and prints it.

Usage:
    python nfctest.py

Dependencies:
    uv pip install nfcpy
    Also requires an NFC-capable reader attached to the system.
"""

import nfc

reader = nfc.ContactlessFrontend()
print(reader)