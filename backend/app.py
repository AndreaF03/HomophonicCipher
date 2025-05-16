import random
import string
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)

def generate_mapping(key):
    """
    Generates a deterministic homophonic mapping based on the user-provided key.
    Each letter gets one number, derived from key and position.
    """
    key = key.lower()
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    mapping = {}

    # Remove duplicates while preserving order
    seen = set()
    filtered_key = ''.join([ch for ch in key if ch in alphabet and not (ch in seen or seen.add(ch))])

    # Generate mapping using key + rest of alphabet
    ordered = filtered_key + ''.join([ch for ch in alphabet if ch not in filtered_key])

    for idx, letter in enumerate(ordered):
        # Use index + 1 as the code (or base it on ASCII/position for more complexity)
        mapping[letter] = [str(10 + idx)]  # Single code per letter (can be extended to multiple codes)
    
    return mapping


def reverse_mapping(mapping):
    return {code: letter for letter, codes in mapping.items() for code in codes}

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    text = data.get('text', '').lower()
    key = data.get('key', '').lower()

    mapping = generate_mapping(key)
    cipher_nums = []

    for char in text:
        if char in mapping:
            cipher_nums.append(mapping[char][0])  # Deterministic, no randomness
        else:
            cipher_nums.append(char)  # Keep non-alphabet characters as-is

    return jsonify({
        "encrypted": ' '.join(cipher_nums),
        "mapping": mapping
    })
@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    cipher_text = data.get('text', '')
    mapping = data.get('mapping', {})

    # Create reverse mapping
    rev_mapping = {}
    for char, nums in mapping.items():
        for num in nums:
            rev_mapping[num] = char

    tokens = cipher_text.strip().split()
    decrypted = ''.join([rev_mapping.get(tok, '?') for tok in tokens])

    return jsonify({"decrypted": decrypted})

@app.route('/encrypt', methods=['POST'])
def encrypt_msg():
    data = request.json
    text = data.get('text', '')
    key  = data.get('key', '')
    cipher, mapping = encrypt(text, key)
    return jsonify(encrypted=cipher, mapping=mapping)


@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    ciphertext = data.get('text', '').strip()
    mapping = data.get('mapping')  # <-- Accept mapping directly

    if not mapping:
        # Fallback to key if mapping not provided
        key = data.get('key', '')
        mapping = generate_full_mapping(key)

    rev_map = reverse_mapping(mapping)

    tokens = ciphertext.split() if ' ' in ciphertext else [
        ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)
    ]

    plaintext = ''.join(rev_map.get(tok, tok) for tok in tokens)
    return jsonify({"decrypted": plaintext})


if __name__ == '__main__':
    app.run(debug=True)
