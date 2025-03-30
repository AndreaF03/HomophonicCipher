// src/CipherForm.js
import React, { useState } from 'react';
import { Container, Form, Button, Row, Col, Alert } from 'react-bootstrap';
import axios from 'axios';

function CipherForm() {
  const [mode, setMode] = useState('encrypt'); // 'encrypt' or 'decrypt'
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult('');
    setError('');
    try {
      
      const endpoint = mode === 'encrypt' ? 'encrypt' : 'decrypt';
      const response = await axios.post(`http://127.0.0.1:5000/${endpoint}`, { text: inputText });
      setResult(mode === 'encrypt' ? response.data.encrypted : response.data.decrypted);
    } catch (err) {
      setError('Error processing your request.');
      console.error(err);
    }
  };

  return (
    <Container className="mt-5">
      <h2 className="mb-4 text-center">
        Homophonic Cipher {mode === 'encrypt' ? 'Encryptor' : 'Decryptor'}
      </h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="cipherInput">
          <Form.Label>
            {mode === 'encrypt'
              ? 'Enter Text to Encrypt:'
              : 'Enter Cipher Text to Decrypt:'}
          </Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type here..."
            required
          />
        </Form.Group>
        <Row className="mt-3">
          <Col>
            <Button variant="primary" type="submit" block="true">
              {mode === 'encrypt' ? 'Encrypt' : 'Decrypt'}
            </Button>
          </Col>
          <Col>
            <Button
              variant="secondary"
              onClick={() => {
                setMode(mode === 'encrypt' ? 'decrypt' : 'encrypt');
                setInputText('');
                setResult('');
                setError('');
              }}
              block="true"
            >
              Switch to {mode === 'encrypt' ? 'Decryptor' : 'Encryptor'}
            </Button>
          </Col>
        </Row>
      </Form>
      {result && (
        <Alert variant="success" className="mt-4">
          <strong>Result:</strong> {result}
        </Alert>
      )}
      {error && (
        <Alert variant="danger" className="mt-4">
          {error}
        </Alert>
      )}
    </Container>
  );
}

export default CipherForm;
