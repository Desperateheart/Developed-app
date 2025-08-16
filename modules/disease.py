"""Disease classification module

This module provides a simple wrapper around a PyTorch model to classify crop diseases.
For demonstration purposes, it loads a generic pretrained model and maps outputs to a
small set of example crop diseases. Replace with a fine-tuned model for production.
"""

from typing import Tuple, List

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image


class DiseaseClassifier:
    """Wrapper class for disease classification"""

    def __init__(self, device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.class_names = self._load_model()
        self.transforms = self._get_transforms()

    def _load_model(self) -> Tuple[nn.Module, List[str]]:
        """Load a pretrained model and adapt the classifier head (placeholder)."""
        # Example class names – replace with actual dataset classes
        class_names = [
            "healthy",
            "bacterial_blight",
            "powdery_mildew",
            "leaf_rust",
            "early_blight",
        ]

        # Use an ImageNet pretrained model as a starting point
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
        # Replace classifier to match number of classes
        in_features = model.classifier[1].in_features  # type: ignore[attr-defined]
        model.classifier[1] = nn.Linear(in_features, len(class_names))  # type: ignore[attr-defined]
        model.eval()
        model.to(self.device)

        # NOTE: Model weights are random for the custom head, so predictions are not meaningful.
        # You should load fine-tuned weights here.
        return model, class_names

    def _get_transforms(self):
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])

    def predict(self, image: Image.Image) -> Tuple[str, float]:
        """Predict disease label and confidence for an input PIL image."""
        input_tensor = self.transforms(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(input_tensor)
            probabilities = torch.softmax(output, dim=1).cpu().squeeze()
        confidence, predicted_idx = torch.max(probabilities, 0)
        label = self.class_names[predicted_idx]
        return label, float(confidence)