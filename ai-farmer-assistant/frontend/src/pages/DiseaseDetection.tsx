import React, { useState, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Chip,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  CloudUpload,
  CheckCircle,
  Warning,
  ExpandMore,
  LocalHospital,
  Eco,
  Science,
  Timeline,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-toastify';
import axios from 'axios';

const DiseaseDetection: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onload = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
      setResult(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
    },
    maxFiles: 1,
  });

  const handleDetection = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('crop_type', 'tomato'); // You can make this dynamic

    try {
      // Mock result for demonstration
      // In production, this would call the actual API
      await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate API delay
      
      const mockResult = {
        disease_detected: true,
        disease_name: "Early Blight",
        confidence: 0.89,
        severity_analysis: {
          level: "Moderate",
          affected_percentage: 35,
          recommended_action: "Immediate treatment required"
        },
        treatment: {
          organic: [
            "Remove affected leaves immediately",
            "Apply neem oil spray (2-3 ml/liter)",
            "Use baking soda solution (1 tbsp/gallon)",
            "Mulch around plants to prevent splash"
          ],
          chemical: [
            "Apply chlorothalonil fungicide",
            "Use mancozeb spray",
            "Apply azoxystrobin as directed"
          ],
          prevention: [
            "Water at soil level, avoid overhead watering",
            "Provide adequate spacing between plants",
            "Remove plant debris regularly",
            "Rotate crops yearly"
          ]
        },
        affected_area: {
          image_dimensions: { width: 1920, height: 1080 },
          affected_regions: [
            { x: 100, y: 200, width: 300, height: 250, area: 75000 }
          ],
          total_affected_pixels: 75000
        }
      };
      
      setResult(mockResult);
      
      if (mockResult.disease_detected) {
        toast.warning(`Disease detected: ${mockResult.disease_name}`);
      } else {
        toast.success('No disease detected - Plant is healthy!');
      }
    } catch (error) {
      console.error('Detection error:', error);
      toast.error('Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'low': return 'success';
      case 'moderate': return 'warning';
      case 'high': return 'error';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 600 }}>
        Crop Disease Detection
      </Typography>

      <Grid container spacing={3}>
        {/* Upload Section */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Upload Crop Image
            </Typography>
            
            <Box
              {...getRootProps()}
              sx={{
                border: '2px dashed',
                borderColor: isDragActive ? 'primary.main' : 'grey.300',
                borderRadius: 2,
                p: 4,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? 'action.hover' : 'background.default',
                transition: 'all 0.3s',
                '&:hover': {
                  borderColor: 'primary.main',
                  backgroundColor: 'action.hover',
                },
              }}
            >
              <input {...getInputProps()} />
              <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                {isDragActive ? 'Drop the image here' : 'Drag & drop or click to upload'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Supported formats: JPG, PNG (Max size: 5MB)
              </Typography>
            </Box>

            {selectedImage && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Selected Image:
                </Typography>
                <Card>
                  <CardMedia
                    component="img"
                    height="300"
                    image={selectedImage}
                    alt="Selected crop"
                    sx={{ objectFit: 'contain' }}
                  />
                </Card>
                <Button
                  variant="contained"
                  color="primary"
                  fullWidth
                  sx={{ mt: 2 }}
                  onClick={handleDetection}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <Science />}
                >
                  {loading ? 'Analyzing...' : 'Detect Disease'}
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          {result ? (
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Detection Results
              </Typography>
              
              {/* Disease Status */}
              <Alert 
                severity={result.disease_detected ? 'warning' : 'success'}
                sx={{ mb: 2 }}
              >
                {result.disease_detected 
                  ? `Disease Detected: ${result.disease_name}`
                  : 'No disease detected - Plant is healthy!'}
              </Alert>

              {result.disease_detected && (
                <>
                  {/* Confidence Score */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="body2" color="textSecondary" gutterBottom>
                      Confidence Score
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LinearProgress
                        variant="determinate"
                        value={result.confidence * 100}
                        sx={{ flexGrow: 1, height: 8, borderRadius: 4, mr: 2 }}
                      />
                      <Typography variant="h6">
                        {(result.confidence * 100).toFixed(1)}%
                      </Typography>
                    </Box>
                  </Box>

                  {/* Severity Analysis */}
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      Severity Analysis
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Chip
                          label={`Severity: ${result.severity_analysis.level}`}
                          color={getSeverityColor(result.severity_analysis.level)}
                          sx={{ width: '100%' }}
                        />
                      </Grid>
                      <Grid item xs={6}>
                        <Chip
                          label={`Affected: ${result.severity_analysis.affected_percentage}%`}
                          variant="outlined"
                          sx={{ width: '100%' }}
                        />
                      </Grid>
                    </Grid>
                    <Alert severity="info" sx={{ mt: 2 }}>
                      {result.severity_analysis.recommended_action}
                    </Alert>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  {/* Treatment Recommendations */}
                  <Typography variant="subtitle1" gutterBottom>
                    Treatment Recommendations
                  </Typography>
                  
                  <Accordion defaultExpanded>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Eco sx={{ mr: 1 }} />
                      <Typography>Organic Treatment</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List dense>
                        {result.treatment.organic.map((item: string, index: number) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <CheckCircle color="success" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={item} />
                          </ListItem>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>

                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Science sx={{ mr: 1 }} />
                      <Typography>Chemical Treatment</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List dense>
                        {result.treatment.chemical.map((item: string, index: number) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <Warning color="warning" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={item} />
                          </ListItem>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>

                  <Accordion>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <LocalHospital sx={{ mr: 1 }} />
                      <Typography>Prevention Tips</Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <List dense>
                        {result.treatment.prevention.map((item: string, index: number) => (
                          <ListItem key={index}>
                            <ListItemIcon>
                              <CheckCircle color="primary" fontSize="small" />
                            </ListItemIcon>
                            <ListItemText primary={item} />
                          </ListItem>
                        ))}
                      </List>
                    </AccordionDetails>
                  </Accordion>
                </>
              )}
            </Paper>
          ) : (
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Timeline sx={{ fontSize: 64, color: 'grey.400', mb: 2 }} />
              <Typography variant="h6" color="textSecondary">
                No Results Yet
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Upload an image and click "Detect Disease" to see results
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>

      {/* History Section */}
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Detections
        </Typography>
        <Grid container spacing={2}>
          {[1, 2, 3].map((item) => (
            <Grid item xs={12} sm={6} md={4} key={item}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="subtitle2" color="textSecondary">
                      {new Date().toLocaleDateString()}
                    </Typography>
                    <Chip 
                      label="Tomato" 
                      size="small" 
                      color="primary" 
                      variant="outlined" 
                    />
                  </Box>
                  <Typography variant="h6">
                    {item === 1 ? 'Early Blight' : item === 2 ? 'Healthy' : 'Late Blight'}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Confidence: {item === 1 ? '89%' : item === 2 ? '95%' : '76%'}
                  </Typography>
                  <Chip
                    label={item === 2 ? 'Healthy' : 'Treated'}
                    size="small"
                    color={item === 2 ? 'success' : 'warning'}
                    sx={{ mt: 1 }}
                  />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Box>
  );
};

export default DiseaseDetection;