from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Define the homophonic cipher mapping
homophonic_mapping = {
    'A': [12, 45, 67], 'B': [23, 56], 'C': [34, 78], 'D': [13, 89], 'E': [11, 22, 33, 44],
    'F': [55, 66], 'G': [77, 88], 'H': [90, 12], 'I': [21, 31, 41], 'J': [51],
    'K': [61], 'L': [71, 81], 'M': [91, 14], 'N': [24, 35], 'O': [46, 57],
    'P': [68, 79], 'Q': [80], 'R': [92, 15], 'S': [25, 36], 'T': [47, 58],
    'U': [69, 82], 'V': [93], 'W': [16, 26], 'X': [37], 'Y': [48, 59], 'Z': [99]
}

# Reverse mapping for decryption
reverse_mapping = {str(num): letter for letter, values in homophonic_mapping.items() for num in values}

def encrypt(plaintext):
    ciphertext = []
    for char in plaintext.upper():
        if char in homophonic_mapping:
            ciphertext.append(str(random.choice(homophonic_mapping[char])))
        else:
            ciphertext.append(char)  # Keep spaces and special characters
    return ' '.join(ciphertext)

def decrypt(ciphertext):
    print("Received ciphertext:", ciphertext)  # Debugging step
    plaintext = []
    for symbol in ciphertext.split():
        if symbol in reverse_mapping:
            plaintext.append(reverse_mapping[symbol])
        else:
            plaintext.append("?")  
    print("Decrypted plaintext:", "".join(plaintext)) 
    return "".join(plaintext)


@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    data = request.json
    plaintext = data.get('text', '')
    encrypted_text = encrypt(plaintext)
    return jsonify({"encrypted": encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    data = request.json
    ciphertext = data.get('text', '')
    decrypted_text = decrypt(ciphertext)
    return jsonify({"decrypted": decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)
