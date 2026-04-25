import React from 'react';
import { CssBaseline, Container, Box } from '@mui/material';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <>
      <CssBaseline />
      <Navbar />
      <Container maxWidth="md">
        <Box mt={4}>
          <Dashboard />
        </Box>
      </Container>
    </>
  );
}

export default App;