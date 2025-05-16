// CipherForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { Container, Form, Button, Row, Col, Alert } from 'react-bootstrap';

export default function CipherForm() {
  const [plain, setPlain] = useState('');
  const [key, setKey] = useState('');
  const [cipherText, setCipherText] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');
  const [mapping, setMapping] = useState({});

  const handleEncrypt = async () => {
    try {
      setError('');
      const response = await axios.post('http://127.0.0.1:5000/encrypt', { text: plain, key });
setCipherText(response.data.encrypted);
setResult(response.data.encrypted);
setMapping(response.data.mapping); 
    } catch (err) {
      console.error(err);
      setError('Encryption failed. Please check your input and try again.');
    }
  };

  const handleDecrypt = async () => {
    try {
      setError('');
      const response = await axios.post('http://127.0.0.1:5000/decrypt', {
        text: cipherText,
        mapping: mapping,
      });
      setResult(response.data.decrypted);      
    } catch (err) {
      console.error(err);
      setError('Decryption failed. Please ensure ciphertext and mapping are valid.');
    }
  };

  return (
    <Container className="mt-5">
      <Form>
        <Form.Group controlId="plainText">
          <Form.Label>Enter Text</Form.Label>
          <Form.Control
            type="text"
            value={plain}
            onChange={(e) => setPlain(e.target.value)}
            placeholder="Plaintext"
          />
        </Form.Group>

        <Form.Group controlId="keyText" className="mt-3">
          <Form.Label>Enter Key</Form.Label>
          <Form.Control
            type="text"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="Key"
          />
        </Form.Group>

        <Row className="mt-4">
          <Col>
            <Button variant="primary" onClick={handleEncrypt} className="w-100">
              Encrypt
            </Button>
          </Col>
          <Col>
            <Button
              variant="secondary"
              onClick={handleDecrypt}
              disabled={!cipherText || Object.keys(mapping).length === 0}
              className="w-100"
            >
              Decrypt
            </Button>
          </Col>
        </Row>
      </Form>

      {cipherText && (
        <Alert variant="info" className="mt-4">
          <strong>Ciphertext:</strong> {cipherText}
        </Alert>
      )}

      {result && (
        <Alert variant="success" className="mt-2">
          <strong>Result:</strong> {result}
        </Alert>
      )}

      {error && (
        <Alert variant="danger" className="mt-2">
          {error}
        </Alert>
      )}
    </Container>
  );
}
