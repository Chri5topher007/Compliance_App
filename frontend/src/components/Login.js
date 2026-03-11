import React, { useState, useContext } from 'react';
import { AuthContext } from '../AuthContext';
import { Paper, TextField, Button, Typography, Box } from '@material-ui/core';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useContext(AuthContext);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      window.location.href = "/"; // Redirect on success
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', marginTop: '100px' }}>
      <Paper style={{ padding: 40, width: 400 }}>
        <Typography variant="h5" align="center">EHR Compliance Portal</Typography>
        <form onSubmit={handleSubmit}>
          <Box mt={3}>
            <TextField label="Username" fullWidth value={username} onChange={(e) => setUsername(e.target.value)} />
          </Box>
          <Box mt={2}>
            <TextField label="Password" type="password" fullWidth value={password} onChange={(e) => setPassword(e.target.value)} />
          </Box>
          {error && <Typography color="error" variant="body2">{error}</Typography>}
          <Box mt={3}>
            <Button type="submit" variant="contained" color="primary" fullWidth>Sign In</Button>
          </Box>
        </form>
      </Paper>
    </div>
  );
};

export default Login;