import React, { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Paper,
  IconButton,
  LinearProgress,
  Chip,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Agriculture,
  LocalFlorist,
  Store,
  Cloud,
  Warning,
  CheckCircle,
  ArrowForward,
} from '@mui/icons-material';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  // Mock data for charts
  const revenueData = [
    { month: 'Jan', revenue: 4000, expenses: 2400 },
    { month: 'Feb', revenue: 3000, expenses: 1398 },
    { month: 'Mar', revenue: 2000, expenses: 9800 },
    { month: 'Apr', revenue: 2780, expenses: 3908 },
    { month: 'May', revenue: 1890, expenses: 4800 },
    { month: 'Jun', revenue: 2390, expenses: 3800 },
  ];

  const cropYieldData = [
    { crop: 'Tomato', yield: 85 },
    { crop: 'Potato', yield: 72 },
    { crop: 'Wheat', yield: 90 },
    { crop: 'Rice', yield: 65 },
  ];

  const marketPriceData = [
    { name: 'Tomato', value: 2.5, change: 0.3 },
    { name: 'Potato', value: 1.8, change: -0.2 },
    { name: 'Wheat', value: 0.35, change: 0.05 },
    { name: 'Rice', value: 0.85, change: 0.1 },
  ];

  const diseaseData = [
    { name: 'Healthy', value: 65, color: '#4caf50' },
    { name: 'Diseased', value: 25, color: '#ff9800' },
    { name: 'Critical', value: 10, color: '#f44336' },
  ];

  const statsCards = [
    {
      title: 'Total Yield',
      value: '450 kg',
      change: '+15%',
      trend: 'up',
      icon: <Agriculture />,
      color: '#4caf50',
    },
    {
      title: 'Disease Detections',
      value: '12',
      change: '-8%',
      trend: 'down',
      icon: <LocalFlorist />,
      color: '#ff9800',
    },
    {
      title: 'Market Revenue',
      value: '$2,450',
      change: '+22%',
      trend: 'up',
      icon: <Store />,
      color: '#2196f3',
    },
    {
      title: 'Weather Alerts',
      value: '3',
      change: 'Active',
      trend: 'neutral',
      icon: <Cloud />,
      color: '#9c27b0',
    },
  ];

  const recentAlerts = [
    { type: 'weather', message: 'Heavy rain expected tomorrow', severity: 'warning' },
    { type: 'disease', message: 'Early blight detected in Section A', severity: 'error' },
    { type: 'market', message: 'Tomato prices up by 15%', severity: 'success' },
    { type: 'advice', message: 'Optimal planting time for wheat', severity: 'info' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Farm Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {statsCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Box
                    sx={{
                      backgroundColor: `${stat.color}20`,
                      borderRadius: 2,
                      p: 1,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mr: 2,
                    }}
                  >
                    {React.cloneElement(stat.icon, { sx: { color: stat.color } })}
                  </Box>
                  <Box sx={{ flexGrow: 1 }}>
                    <Typography color="textSecondary" variant="body2">
                      {stat.title}
                    </Typography>
                    <Typography variant="h5" sx={{ fontWeight: 600 }}>
                      {stat.value}
                    </Typography>
                  </Box>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {stat.trend === 'up' && <TrendingUp sx={{ color: '#4caf50', mr: 1 }} />}
                  {stat.trend === 'down' && <TrendingDown sx={{ color: '#f44336', mr: 1 }} />}
                  <Typography
                    variant="body2"
                    sx={{
                      color: stat.trend === 'up' ? '#4caf50' : stat.trend === 'down' ? '#f44336' : 'text.secondary',
                    }}
                  >
                    {stat.change}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Revenue & Expenses
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="revenue" stackId="1" stroke="#4caf50" fill="#4caf50" />
                <Area type="monotone" dataKey="expenses" stackId="1" stroke="#ff9800" fill="#ff9800" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Crop Health Status
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={diseaseData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: ${entry.value}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {diseaseData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Market Prices and Alerts */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Current Market Prices</Typography>
              <Button
                size="small"
                endIcon={<ArrowForward />}
                onClick={() => navigate('/marketplace')}
              >
                View All
              </Button>
            </Box>
            {marketPriceData.map((item, index) => (
              <Box key={index} sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                  <Typography variant="body1">{item.name}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography variant="h6" sx={{ mr: 1 }}>
                      ${item.value}/kg
                    </Typography>
                    <Chip
                      label={`${item.change > 0 ? '+' : ''}${item.change}`}
                      size="small"
                      color={item.change > 0 ? 'success' : 'error'}
                    />
                  </Box>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(item.value / 3) * 100}
                  sx={{ height: 6, borderRadius: 3 }}
                />
              </Box>
            ))}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Recent Alerts</Typography>
              <Button
                size="small"
                endIcon={<ArrowForward />}
                onClick={() => navigate('/weather')}
              >
                View All
              </Button>
            </Box>
            {recentAlerts.map((alert, index) => (
              <Box
                key={index}
                sx={{
                  mb: 2,
                  p: 2,
                  borderRadius: 2,
                  backgroundColor:
                    alert.severity === 'error'
                      ? '#ffebee'
                      : alert.severity === 'warning'
                      ? '#fff3e0'
                      : alert.severity === 'success'
                      ? '#e8f5e9'
                      : '#e3f2fd',
                  display: 'flex',
                  alignItems: 'center',
                }}
              >
                {alert.severity === 'error' && <Warning sx={{ color: '#f44336', mr: 2 }} />}
                {alert.severity === 'warning' && <Warning sx={{ color: '#ff9800', mr: 2 }} />}
                {alert.severity === 'success' && <CheckCircle sx={{ color: '#4caf50', mr: 2 }} />}
                {alert.severity === 'info' && <Cloud sx={{ color: '#2196f3', mr: 2 }} />}
                <Typography variant="body2">{alert.message}</Typography>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>

      {/* Crop Yield Chart */}
      <Grid container spacing={3} sx={{ mt: 1 }}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Crop Yield Performance
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={cropYieldData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="crop" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="yield" fill="#4caf50" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;