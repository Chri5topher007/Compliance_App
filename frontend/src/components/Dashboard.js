import React from 'react';
import { Paper, Typography, Button, Box } from '@material-ui/core';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  return (
    <div style={{ padding: 20 }}>
      <Typography variant="h4" gutterBottom>Compliance Dashboard</Typography>
      <Box display="flex" gap={2}>
        <Paper style={{ padding: 20, width: '30%' }}>
          <Typography variant="h6">Documents</Typography>
          <Button component={Link} to="/department" variant="contained" color="primary" style={{ marginTop: 10 }}>
            Manage Documents
          </Button>
        </Paper>
        <Paper style={{ padding: 20, width: '30%' }}>
          <Typography variant="h6">Audit Scheduler</Typography>
          <Button component={Link} to="/scheduler" variant="contained" color="secondary" style={{ marginTop: 10 }}>
            Schedule Audit
          </Button>
        </Paper>
      </Box>
    </div>
  );
};

export default Dashboard;