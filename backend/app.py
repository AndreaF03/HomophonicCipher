import string
from flask import Flask, request, jsonify
from flask_cors import CORS

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

    # Remove duplicates from key while preserving order
    seen = set()
    filtered_key = ''.join([ch for ch in key if ch in alphabet and not (ch in seen or seen.add(ch))])

    # Build the ordered alphabet based on key
    ordered = filtered_key + ''.join([ch for ch in alphabet if ch not in filtered_key])

    for idx, letter in enumerate(ordered):
        mapping[letter] = [str(10 + idx)]  # Assign unique numeric code to each letter

    return mapping

def reverse_mapping(mapping):
    """
    Reverses the character-to-code mapping for decryption.
    """
    return {code: letter for letter, codes in mapping.items() for code in codes}

@app.route('/encrypt', methods=['POST'])
def encrypt():
    """
    Encrypt endpoint: receives text and key, returns encrypted message and mapping.
    """
    data = request.json
    text = data.get('text', '').lower()
    key = data.get('key', '').lower()

    mapping = generate_mapping(key)
    cipher_nums = []

    for char in text:
        if char in mapping:
            cipher_nums.append(mapping[char][0])  # Use the unique code for the letter
        else:
            cipher_nums.append(char)  # Non-alphabet characters are kept as-is

    return jsonify({
        "encrypted": ' '.join(cipher_nums),
        "mapping": mapping
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    """
    Decrypt endpoint: receives cipher text and mapping, returns decrypted plain text.
    """
    data = request.json
    cipher_text = data.get('text', '')
    mapping = data.get('mapping', {})

    rev_map = reverse_mapping(mapping)
    tokens = cipher_text.strip().split()

    decrypted = ''.join([rev_map.get(tok, tok) for tok in tokens])  # Keep unknown tokens unchanged

    return jsonify({"decrypted": decrypted})
@app.route('/')
def index():
    return "Homophonic Cipher API is running."
if __name__ == '__main__':
    app.run(debug=True)
