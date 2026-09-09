"""
SubEncrypt.py

Monoalphabetic substitution cipher. Generates a random shuffled alphabet
and uses it to encrypt a message via character mapping.

Note: Each run produces a different random key, so encrypted output from one
run cannot be decrypted by another run unless the key is shared.

Usage:
    python SubEncrypt.py
    # then type a message when prompted

Dependencies:
    None (stdlib only)
"""

import random
import string

CHARS = list(string.punctuation + string.digits + string.ascii_letters + " ")
KEY = CHARS.copy()
random.shuffle(KEY)


def encrypt(plaintext: str) -> str:
    ciphertext = ""
    for ch in plaintext:
        idx = CHARS.index(ch)
        ciphertext += KEY[idx]
    return ciphertext


def decrypt(ciphertext: str) -> str:
    plaintext = ""
    for ch in ciphertext:
        idx = KEY.index(ch)
        plaintext += CHARS[idx]
    return plaintext


def main():
    message = input("Enter a message to encrypt: ")
    encrypted = encrypt(message)
    decrypted = decrypt(encrypted)

    print(f"encrypted: {encrypted}")
    print(f"decrypted: {decrypted}")


if __name__ == "__main__":
    main()
