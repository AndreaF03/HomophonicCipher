// src/App.js
import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import CipherForm from './CipherForm';  
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <div>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="#">Homophonic Cipher</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container className="mt-4">
        <CipherForm />
      </Container>
    </div>
  );
}

export default App;
