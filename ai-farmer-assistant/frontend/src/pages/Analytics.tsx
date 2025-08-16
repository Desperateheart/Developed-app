import React from 'react';
import { Box, Typography, Paper, Grid } from '@mui/material';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Analytics: React.FC = () => {
  const data = [
    { month: 'Jan', yield: 400, revenue: 2400 },
    { month: 'Feb', yield: 300, revenue: 1398 },
    { month: 'Mar', yield: 200, revenue: 9800 },
    { month: 'Apr', yield: 278, revenue: 3908 },
    { month: 'May', yield: 189, revenue: 4800 },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Analytics & Reports
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Yield Trends</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="yield" stroke="#4caf50" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Revenue Analysis</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="revenue" fill="#2196f3" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;