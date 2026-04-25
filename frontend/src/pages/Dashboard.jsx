import React, { useEffect, useState } from 'react';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, Button, Box, Alert, Stack } from '@mui/material';
import api from '../services/api';

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [form, setForm] = useState({ description: '', amount: '', date: '' });
  const [mlFeatures, setMlFeatures] = useState('');
  const [mlResult, setMlResult] = useState(null);
  const [mlError, setMlError] = useState('');
  const [mlTrainMsg, setMlTrainMsg] = useState('');
  const [mlLoading, setMlLoading] = useState(false);

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = async () => {
    const res = await api.get('/expenses/');
    setExpenses(res.data);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAdd = async () => {
    if (!form.description || !form.amount || !form.date) return;
    await api.post('/expenses/', { ...form, amount: parseFloat(form.amount) });
    setForm({ description: '', amount: '', date: '' });
    fetchExpenses();
  };

  const handleDelete = async (id) => {
    await api.delete(`/expenses/${id}`);
    fetchExpenses();
  };

  // --- ML Prediction ---
  const handleMLPredict = async () => {
    setMlError('');
    setMlResult(null);
    setMlLoading(true);
    try {
      // Parse input: comma-separated numbers, e.g. "1.0,2.0"
      const features = mlFeatures
        .split(';')
        .map(row => row.split(',').map(Number))
        .filter(arr => arr.length > 1 && arr.every(n => !isNaN(n)));
      if (!features.length) throw new Error('Enter features as: 1.0,2.0;3.0,4.0');
      const res = await api.post('/ml/predict', { features });
      setMlResult(res.data.predictions);
    } catch (err) {
      setMlError(err.response?.data?.detail || err.message);
    }
    setMlLoading(false);
  };

  // --- ML Training ---
  const handleMLTrain = async () => {
    setMlTrainMsg('');
    setMlError('');
    setMlLoading(true);
    try {
      const features = [[1,2],[2,3],[3,4],[4,5],[5,6]];
      const targets = [100, 200, 300, 400, 500];
      await api.post('/ml/train', { features, targets });
      setMlTrainMsg('Model trained with example data! You can now predict.');
    } catch (err) {
      setMlError('Training failed: ' + (err.response?.data?.detail || err.message));
    }
    setMlLoading(false);
  };

  return (
    <Box sx={{ maxWidth: 900, mx: 'auto', p: 2 }}>
      <Typography variant="h3" align="center" gutterBottom color="primary">SavvySpend Dashboard</Typography>
      <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} mb={4} alignItems="center" justifyContent="center">
        <TextField label="Description" name="description" value={form.description} onChange={handleChange} />
        <TextField label="Amount" name="amount" type="number" value={form.amount} onChange={handleChange} />
        <TextField label="Date" name="date" type="date" value={form.date} onChange={handleChange} InputLabelProps={{ shrink: true }} />
        <Button variant="contained" color="primary" onClick={handleAdd}>Add</Button>
      </Stack>
      <TableContainer component={Paper} sx={{ mb: 4 }}>
        <Table>
          <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
            <TableRow>
              <TableCell><b>Description</b></TableCell>
              <TableCell><b>Amount</b></TableCell>
              <TableCell><b>Date</b></TableCell>
              <TableCell><b>Action</b></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {expenses.map((exp) => (
              <TableRow key={exp.id}>
                <TableCell>{exp.description}</TableCell>
                <TableCell>{exp.amount}</TableCell>
                <TableCell>{exp.date}</TableCell>
                <TableCell>
                  <Button color="error" onClick={() => handleDelete(exp.id)}>Delete</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Paper sx={{ p: 3, mb: 2, background: '#f0f4ff' }}>
        <Typography variant="h5" color="primary" gutterBottom>ML Budget Prediction</Typography>
        <Typography variant="body2" color="textSecondary" mb={2}>
          Enter features for prediction (e.g. <b>1.0,2.0;3.0,4.0</b> for batch, or <b>1.0,2.0</b> for real-time).<br/>
          <b>First, train the model with example data if you haven't already.</b>
        </Typography>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} mb={2}>
          <TextField
            label="Features (e.g. 1.0,2.0;3.0,4.0)"
            value={mlFeatures}
            onChange={e => setMlFeatures(e.target.value)}
            fullWidth
            disabled={mlLoading}
          />
          <Button variant="outlined" onClick={handleMLPredict} disabled={mlLoading}>Predict</Button>
          <Button variant="contained" color="secondary" onClick={handleMLTrain} disabled={mlLoading}>Train Model with Example Data</Button>
        </Stack>
        {mlTrainMsg && <Alert severity="success" sx={{ mt: 2 }}>{mlTrainMsg}</Alert>}
        {mlError && <Alert severity="error" sx={{ mt: 2 }}>{mlError}</Alert>}
        {mlResult && (
          <Alert severity="success" sx={{ mt: 2 }}>
            Predictions: {mlResult.join(', ')}
          </Alert>
        )}
      </Paper>
    </Box>
  );
};

export default Dashboard;