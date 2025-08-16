import React from 'react';
import { Box, Typography, Grid, Card, CardContent, Button, Chip } from '@mui/material';
import { TrendingUp, Store } from '@mui/icons-material';

const Marketplace: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Marketplace
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Store sx={{ fontSize: 40, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6">Check Market Prices</Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1, mb: 2 }}>
                Get real-time prices and market trends for your crops
              </Typography>
              <Button variant="contained" fullWidth>View Prices</Button>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <TrendingUp sx={{ fontSize: 40, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h6">Find Buyers</Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1, mb: 2 }}>
                Connect with verified buyers for your produce
              </Typography>
              <Button variant="contained" color="secondary" fullWidth>Search Buyers</Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Marketplace;