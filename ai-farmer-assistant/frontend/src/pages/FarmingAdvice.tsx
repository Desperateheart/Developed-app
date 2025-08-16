import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, Button, Tab, Tabs } from '@mui/material';
import { Agriculture, WaterDrop, Eco, Grass } from '@mui/icons-material';

const FarmingAdvice: React.FC = () => {
  const [tabValue, setTabValue] = React.useState(0);

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Farming Advice
      </Typography>
      
      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Planting" icon={<Agriculture />} />
          <Tab label="Irrigation" icon={<WaterDrop />} />
          <Tab label="Soil" icon={<Eco />} />
          <Tab label="Fertilizer" icon={<Grass />} />
        </Tabs>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6">Get Personalized Farming Advice</Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                Select a category above to receive tailored recommendations for your crops
              </Typography>
              <Button variant="contained" sx={{ mt: 2 }}>
                Get Recommendations
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default FarmingAdvice;