import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, Chip, Alert } from '@mui/material';
import { Cloud, WaterDrop, Air, WbSunny } from '@mui/icons-material';

const Weather: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Weather & Alerts
      </Typography>
      
      <Alert severity="warning" sx={{ mb: 3 }}>
        Heavy rain expected tomorrow - Consider harvesting mature crops
      </Alert>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <WbSunny sx={{ color: 'orange', mb: 1 }} />
              <Typography variant="h4">28°C</Typography>
              <Typography variant="body2" color="textSecondary">Temperature</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <WaterDrop sx={{ color: 'blue', mb: 1 }} />
              <Typography variant="h4">65%</Typography>
              <Typography variant="body2" color="textSecondary">Humidity</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Air sx={{ color: 'grey', mb: 1 }} />
              <Typography variant="h4">12 km/h</Typography>
              <Typography variant="body2" color="textSecondary">Wind Speed</Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Cloud sx={{ color: 'lightblue', mb: 1 }} />
              <Typography variant="h4">30%</Typography>
              <Typography variant="body2" color="textSecondary">Rain Chance</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>7-Day Forecast</Typography>
        <Typography variant="body2" color="textSecondary">
          Weather forecast will be displayed here
        </Typography>
      </Paper>
    </Box>
  );
};

export default Weather;