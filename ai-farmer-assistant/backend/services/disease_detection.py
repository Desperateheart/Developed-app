import torch
import torchvision.transforms as transforms
from torchvision import models
import numpy as np
from PIL import Image
import io
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import cv2
import base64

class DiseaseDetectionService:
    """
    Service for detecting crop diseases using computer vision and deep learning
    """
    
    def __init__(self):
        self.model = None
        self.transform = None
        self.disease_classes = {
            0: "Healthy",
            1: "Bacterial Spot",
            2: "Early Blight",
            3: "Late Blight",
            4: "Leaf Mold",
            5: "Septoria Leaf Spot",
            6: "Spider Mites",
            7: "Target Spot",
            8: "Yellow Leaf Curl Virus",
            9: "Mosaic Virus",
            10: "Powdery Mildew",
            11: "Rust",
            12: "Scab",
            13: "Black Rot",
            14: "Bacterial Wilt"
        }
        
        self.treatment_recommendations = {
            "Bacterial Spot": {
                "organic": [
                    "Remove infected leaves immediately",
                    "Apply copper-based fungicide",
                    "Improve air circulation",
                    "Avoid overhead watering"
                ],
                "chemical": [
                    "Apply streptomycin sulfate",
                    "Use copper hydroxide spray",
                    "Apply mancozeb fungicide"
                ],
                "prevention": [
                    "Use disease-resistant varieties",
                    "Practice crop rotation",
                    "Maintain proper plant spacing"
                ]
            },
            "Early Blight": {
                "organic": [
                    "Remove affected leaves",
                    "Apply neem oil spray",
                    "Use baking soda solution",
                    "Mulch around plants"
                ],
                "chemical": [
                    "Apply chlorothalonil fungicide",
                    "Use mancozeb spray",
                    "Apply azoxystrobin"
                ],
                "prevention": [
                    "Water at soil level",
                    "Provide adequate spacing",
                    "Remove plant debris"
                ]
            },
            "Late Blight": {
                "organic": [
                    "Remove and destroy infected plants",
                    "Apply copper fungicide immediately",
                    "Use Bacillus subtilis spray"
                ],
                "chemical": [
                    "Apply metalaxyl fungicide",
                    "Use cymoxanil + mancozeb",
                    "Apply dimethomorph"
                ],
                "prevention": [
                    "Plant resistant varieties",
                    "Avoid overhead irrigation",
                    "Monitor weather conditions"
                ]
            },
            "Powdery Mildew": {
                "organic": [
                    "Apply milk spray (1:9 ratio)",
                    "Use sulfur dust",
                    "Apply potassium bicarbonate",
                    "Neem oil treatment"
                ],
                "chemical": [
                    "Apply trifloxystrobin",
                    "Use propiconazole",
                    "Apply myclobutanil"
                ],
                "prevention": [
                    "Ensure good air circulation",
                    "Avoid overcrowding",
                    "Water early in the day"
                ]
            }
        }
        
    async def load_model(self):
        """Load the pre-trained disease detection model"""
        try:
            # Using a pre-trained ResNet model for demonstration
            # In production, you would load a custom-trained model
            self.model = models.resnet50(pretrained=True)
            
            # Modify the final layer for our disease classes
            num_features = self.model.fc.in_features
            self.model.fc = torch.nn.Linear(num_features, len(self.disease_classes))
            
            # Set model to evaluation mode
            self.model.eval()
            
            # Define image transformations
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
            
            print("Disease detection model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            # Use a simpler fallback approach
            self.model = "fallback"
            return False
    
    async def detect_disease(self, image_data: bytes, crop_type: Optional[str] = None) -> Dict:
        """
        Detect disease from image data
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Perform detection
            if self.model == "fallback" or self.model is None:
                # Fallback: Use image analysis heuristics
                detection_result = await self._fallback_detection(image, crop_type)
            else:
                # Use deep learning model
                detection_result = await self._model_detection(image)
            
            # Add treatment recommendations
            disease_name = detection_result['disease_name']
            if disease_name in self.treatment_recommendations:
                detection_result['treatment'] = self.treatment_recommendations[disease_name]
            
            # Add severity analysis
            detection_result['severity_analysis'] = await self._analyze_severity(image)
            
            # Add affected area estimation
            detection_result['affected_area'] = await self._estimate_affected_area(image)
            
            # Store detection history
            detection_result['timestamp'] = datetime.now().isoformat()
            detection_result['crop_type'] = crop_type
            
            return detection_result
            
        except Exception as e:
            return {
                "error": str(e),
                "disease_detected": False,
                "message": "Failed to process image"
            }
    
    async def _model_detection(self, image: Image) -> Dict:
        """Perform detection using the deep learning model"""
        try:
            # Transform image
            input_tensor = self.transform(image)
            input_batch = input_tensor.unsqueeze(0)
            
            # Make prediction
            with torch.no_grad():
                output = self.model(input_batch)
                probabilities = torch.nn.functional.softmax(output[0], dim=0)
                
            # Get top predictions
            top_prob, top_class = torch.topk(probabilities, 3)
            
            # Format results
            predictions = []
            for i in range(3):
                predictions.append({
                    "disease": self.disease_classes[top_class[i].item()],
                    "confidence": float(top_prob[i].item())
                })
            
            # Primary detection
            primary = predictions[0]
            is_diseased = primary['disease'] != "Healthy"
            
            return {
                "disease_detected": is_diseased,
                "disease_name": primary['disease'],
                "confidence": primary['confidence'],
                "all_predictions": predictions,
                "analysis_method": "deep_learning"
            }
            
        except Exception as e:
            # Fallback to heuristic method
            return await self._fallback_detection(image, None)
    
    async def _fallback_detection(self, image: Image, crop_type: Optional[str]) -> Dict:
        """
        Fallback detection using image processing heuristics
        """
        # Convert PIL image to numpy array
        img_array = np.array(image)
        
        # Convert to HSV for color analysis
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Analyze color distributions
        brown_spots = self._detect_brown_spots(hsv)
        yellow_areas = self._detect_yellow_areas(hsv)
        white_patches = self._detect_white_patches(img_array)
        
        # Heuristic disease detection
        disease_indicators = {
            "brown_spots": brown_spots,
            "yellow_areas": yellow_areas,
            "white_patches": white_patches
        }
        
        # Determine most likely disease
        disease_name = "Healthy"
        confidence = 0.85
        
        if brown_spots > 0.15:
            disease_name = "Early Blight"
            confidence = min(0.7 + brown_spots, 0.95)
        elif yellow_areas > 0.20:
            disease_name = "Yellow Leaf Curl Virus"
            confidence = min(0.6 + yellow_areas, 0.90)
        elif white_patches > 0.10:
            disease_name = "Powdery Mildew"
            confidence = min(0.65 + white_patches, 0.92)
        
        return {
            "disease_detected": disease_name != "Healthy",
            "disease_name": disease_name,
            "confidence": confidence,
            "indicators": disease_indicators,
            "analysis_method": "heuristic",
            "crop_type": crop_type
        }
    
    def _detect_brown_spots(self, hsv_image: np.ndarray) -> float:
        """Detect brown spots in the image"""
        # Define brown color range in HSV
        lower_brown = np.array([10, 50, 50])
        upper_brown = np.array([20, 255, 200])
        
        # Create mask
        mask = cv2.inRange(hsv_image, lower_brown, upper_brown)
        
        # Calculate percentage
        total_pixels = hsv_image.shape[0] * hsv_image.shape[1]
        brown_pixels = np.sum(mask > 0)
        
        return brown_pixels / total_pixels
    
    def _detect_yellow_areas(self, hsv_image: np.ndarray) -> float:
        """Detect yellow areas in the image"""
        # Define yellow color range in HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        
        # Create mask
        mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        
        # Calculate percentage
        total_pixels = hsv_image.shape[0] * hsv_image.shape[1]
        yellow_pixels = np.sum(mask > 0)
        
        return yellow_pixels / total_pixels
    
    def _detect_white_patches(self, rgb_image: np.ndarray) -> float:
        """Detect white patches (powdery mildew indicator)"""
        # Convert to grayscale
        gray = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
        
        # Threshold for white areas
        _, white_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Calculate percentage
        total_pixels = gray.shape[0] * gray.shape[1]
        white_pixels = np.sum(white_mask > 0)
        
        return white_pixels / total_pixels
    
    async def _analyze_severity(self, image: Image) -> Dict:
        """Analyze disease severity"""
        img_array = np.array(image)
        
        # Simple severity estimation based on affected area
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Detect non-green areas (potential disease)
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        healthy_percentage = np.sum(green_mask > 0) / (hsv.shape[0] * hsv.shape[1])
        affected_percentage = 1 - healthy_percentage
        
        # Determine severity level
        if affected_percentage < 0.1:
            severity = "Low"
            action = "Monitor closely, preventive treatment recommended"
        elif affected_percentage < 0.25:
            severity = "Moderate"
            action = "Immediate treatment required"
        elif affected_percentage < 0.5:
            severity = "High"
            action = "Urgent intervention needed, consider removing heavily affected parts"
        else:
            severity = "Critical"
            action = "Emergency treatment or plant removal may be necessary"
        
        return {
            "level": severity,
            "affected_percentage": float(affected_percentage * 100),
            "recommended_action": action
        }
    
    async def _estimate_affected_area(self, image: Image) -> Dict:
        """Estimate the affected area of the plant"""
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # Simple contour detection for affected regions
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        affected_regions = []
        for contour in contours[:5]:  # Top 5 largest regions
            area = cv2.contourArea(contour)
            if area > 100:  # Filter small noise
                x, y, w, h = cv2.boundingRect(contour)
                affected_regions.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": float(area)
                })
        
        return {
            "image_dimensions": {"width": width, "height": height},
            "affected_regions": affected_regions,
            "total_affected_pixels": sum(r['area'] for r in affected_regions)
        }
    
    async def get_history(self, user_id: Optional[int], limit: int) -> List[Dict]:
        """Get disease detection history"""
        # In a real implementation, this would query a database
        # For now, return mock data
        return [
            {
                "id": 1,
                "timestamp": "2024-01-15T10:30:00",
                "crop_type": "Tomato",
                "disease_detected": True,
                "disease_name": "Early Blight",
                "confidence": 0.89,
                "severity": "Moderate",
                "treatment_applied": "Organic fungicide"
            },
            {
                "id": 2,
                "timestamp": "2024-01-10T14:20:00",
                "crop_type": "Potato",
                "disease_detected": False,
                "disease_name": "Healthy",
                "confidence": 0.95
            }
        ][:limit]