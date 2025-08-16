// AI Farmer Assistant Frontend JavaScript

let selectedFile = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeUpload();
    initializeForms();
    loadInitialCrops();
});

// Image upload functionality
function initializeUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const imageUpload = document.getElementById('imageUpload');
    const analyzeBtn = document.getElementById('analyzeBtn');

    // Click to upload
    uploadArea.addEventListener('click', () => {
        imageUpload.click();
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // File input change
    imageUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeDiseaseImage);
}

function handleFileSelect(file) {
    if (!file.type.startsWith('image/')) {
        showAlert('Please select a valid image file.', 'danger');
        return;
    }

    selectedFile = file;
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.disabled = false;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.innerHTML = `
            <img src="${e.target.result}" alt="Preview" style="max-width: 200px; max-height: 200px; border-radius: 10px;">
            <p class="mt-2 mb-0"><strong>${file.name}</strong></p>
            <small class="text-muted">Click to change image</small>
        `;
    };
    reader.readAsDataURL(file);
}

async function analyzeDiseaseImage() {
    if (!selectedFile) {
        showAlert('Please select an image first.', 'warning');
        return;
    }

    const loading = document.getElementById('diseaseLoading');
    const results = document.getElementById('diseaseResults');
    
    loading.classList.add('show');
    results.classList.add('d-none');

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('crop_name', document.getElementById('cropName').value);

    try {
        const response = await fetch('/api/detect-disease', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (response.ok) {
            displayDiseaseResults(data);
        } else {
            showAlert(data.error || 'Error analyzing image', 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Network error. Please try again.', 'danger');
    } finally {
        loading.classList.remove('show');
    }
}

function displayDiseaseResults(data) {
    const results = document.getElementById('diseaseResults');
    const content = document.getElementById('diseaseContent');
    
    const confidencePercent = Math.round(data.confidence * 100);
    const diseaseClass = data.disease === 'healthy' ? 'success' : 'warning';
    
    content.innerHTML = `
        <div class="mb-3">
            <h6><i class="fas fa-bug me-2"></i>Disease Detected: <span class="text-${diseaseClass}">${data.disease.replace('_', ' ').toUpperCase()}</span></h6>
            <div class="confidence-bar mb-2">
                <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
            </div>
            <small class="text-muted">Confidence: ${confidencePercent}%</small>
        </div>
        <div class="alert alert-${diseaseClass}">
            <h6><i class="fas fa-prescription-bottle-alt me-2"></i>Recommended Treatment:</h6>
            <p class="mb-0">${data.treatment}</p>
        </div>
    `;
    
    results.classList.remove('d-none');
}

// Farming advice functions
async function getPlantingAdvice() {
    const crop = prompt('Enter crop name:');
    if (!crop) return;

    try {
        const response = await fetch(`/api/farming-advice?type=planting&crop=${encodeURIComponent(crop)}`);
        const data = await response.json();
        
        if (response.ok) {
            displayAdviceResults(data, 'Planting Advice');
        } else {
            showAlert(data.error || 'Error getting advice', 'danger');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
    }
}

async function getSeasonalAdvice() {
    const season = prompt('Enter season (spring, summer, fall, winter):');
    if (!season) return;

    try {
        const response = await fetch(`/api/farming-advice?type=seasonal&season=${encodeURIComponent(season)}`);
        const data = await response.json();
        
        if (response.ok) {
            displaySeasonalAdvice(data);
        } else {
            showAlert(data.error || 'Error getting advice', 'danger');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
    }
}

function getIrrigationAdvice() {
    const advice = {
        title: 'Irrigation Best Practices',
        content: `
            <div class="row">
                <div class="col-md-6">
                    <h6><i class="fas fa-clock me-2"></i>Timing</h6>
                    <ul>
                        <li>Water early morning (6-8 AM)</li>
                        <li>Avoid midday watering</li>
                        <li>Evening watering if necessary</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h6><i class="fas fa-tint me-2"></i>Amount</h6>
                    <ul>
                        <li>Deep, infrequent watering</li>
                        <li>1-2 inches per week for most crops</li>
                        <li>Check soil moisture regularly</li>
                    </ul>
                </div>
            </div>
            <div class="alert alert-info mt-3">
                <strong>Tip:</strong> Use drip irrigation or soaker hoses for efficient water use.
            </div>
        `
    };
    
    displayAdviceResults(advice, 'Irrigation Guide');
}

function displayAdviceResults(data, title) {
    const results = document.getElementById('adviceResults');
    const content = document.getElementById('adviceContent');
    
    if (data.crop) {
        // Planting advice
        content.innerHTML = `
            <h6><i class="fas fa-seedling me-2"></i>Crop: ${data.crop}</h6>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <strong>Planting Season:</strong><br>
                    <span class="text-muted">${data.planting_season}</span>
                </div>
                <div class="col-md-6 mb-3">
                    <strong>Soil Requirements:</strong><br>
                    <span class="text-muted">pH ${data.soil_requirements}</span>
                </div>
                <div class="col-md-6 mb-3">
                    <strong>Irrigation:</strong><br>
                    <span class="text-muted">${data.irrigation}</span>
                </div>
                <div class="col-md-6 mb-3">
                    <strong>Fertilization:</strong><br>
                    <span class="text-muted">${data.fertilization}</span>
                </div>
                <div class="col-12">
                    <strong>Plant Spacing:</strong><br>
                    <span class="text-muted">${data.spacing}</span>
                </div>
            </div>
        `;
    } else {
        // Custom advice
        content.innerHTML = data.content || JSON.stringify(data, null, 2);
    }
    
    results.classList.remove('d-none');
    results.scrollIntoView({ behavior: 'smooth' });
}

function displaySeasonalAdvice(data) {
    const results = document.getElementById('adviceResults');
    const content = document.getElementById('adviceContent');
    
    content.innerHTML = `
        <h6><i class="fas fa-calendar-alt me-2"></i>${data.season.charAt(0).toUpperCase() + data.season.slice(1)} Farming Tips</h6>
        <ul class="list-group list-group-flush">
            ${data.tips.map(tip => `<li class="list-group-item border-0 px-0">${tip}</li>`).join('')}
        </ul>
    `;
    
    results.classList.remove('d-none');
    results.scrollIntoView({ behavior: 'smooth' });
}

// Price calculation
async function calculatePrice() {
    const crop = document.getElementById('priceCrop').value;
    const quantity = document.getElementById('priceQuantity').value;
    const quality = document.getElementById('priceQuality').value;

    if (!crop || !quantity) {
        showAlert('Please fill in all required fields.', 'warning');
        return;
    }

    try {
        const response = await fetch(`/api/price-suggestion?crop=${encodeURIComponent(crop)}&quantity=${quantity}&quality=${quality}`);
        const data = await response.json();
        
        if (response.ok) {
            displayPriceResults(data);
        } else {
            showAlert(data.error || 'Error calculating price', 'danger');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
    }
}

function displayPriceResults(data) {
    const results = document.getElementById('priceResults');
    const content = document.getElementById('priceContent');
    
    const trendIcon = data.market_trend === 'rising' ? 'fa-arrow-up trend-up' : 
                     data.market_trend === 'falling' ? 'fa-arrow-down trend-down' : 
                     'fa-minus trend-stable';
    
    content.innerHTML = `
        <div class="row">
            <div class="col-md-6 mb-3">
                <h6><i class="fas fa-tag me-2"></i>Suggested Price</h6>
                <div class="price-tag fs-4">$${data.suggested_price} per kg</div>
            </div>
            <div class="col-md-6 mb-3">
                <h6><i class="fas fa-chart-line me-2"></i>Market Trend</h6>
                <span class="${trendIcon.split(' ')[1]}">
                    <i class="fas ${trendIcon.split(' ')[0]} me-1"></i>
                    ${data.market_trend.charAt(0).toUpperCase() + data.market_trend.slice(1)}
                </span>
            </div>
            <div class="col-12">
                <h6>Price Range</h6>
                <div class="d-flex justify-content-between">
                    <span>Low: $${data.price_range.low}</span>
                    <span>High: $${data.price_range.high}</span>
                </div>
                <div class="progress mt-2">
                    <div class="progress-bar" style="width: ${((data.suggested_price - data.price_range.low) / (data.price_range.high - data.price_range.low)) * 100}%"></div>
                </div>
            </div>
        </div>
        <div class="alert alert-info mt-3">
            <small><strong>Note:</strong> Prices are adjusted for quality (${data.factors.quality_adjustment}x) and quantity (${data.factors.quantity_adjustment}x)</small>
        </div>
    `;
    
    results.classList.remove('d-none');
    results.scrollIntoView({ behavior: 'smooth' });
}

// Marketplace functions
async function searchCrops() {
    const searchTerm = document.getElementById('searchCrop').value;
    
    try {
        const response = await fetch(`/api/search-crops?crop_name=${encodeURIComponent(searchTerm)}`);
        const data = await response.json();
        
        if (response.ok) {
            displayCropListings(data.crops);
        } else {
            showAlert(data.error || 'Error searching crops', 'danger');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
    }
}

async function loadInitialCrops() {
    try {
        const response = await fetch('/api/search-crops');
        const data = await response.json();
        
        if (response.ok) {
            displayCropListings(data.crops.slice(0, 6)); // Show first 6 crops
        }
    } catch (error) {
        console.error('Error loading initial crops:', error);
    }
}

function displayCropListings(crops) {
    const container = document.getElementById('cropListings');
    
    if (crops.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center">
                <p class="text-muted">No crops found matching your search.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = crops.map(crop => `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="crop-listing">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h6 class="mb-0">${crop.crop_name}</h6>
                    <span class="badge bg-success">${crop.quality_grade}</span>
                </div>
                <p class="text-muted mb-2">
                    <i class="fas fa-user me-1"></i>${crop.farmer_name}<br>
                    <i class="fas fa-map-marker-alt me-1"></i>${crop.farmer_location || crop.location || 'Location not specified'}
                </p>
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${crop.quantity} kg</strong><br>
                        <small class="text-muted">Available</small>
                    </div>
                    <div class="text-end">
                        ${crop.price_per_unit ? `<div class="price-tag">$${crop.price_per_unit}/kg</div>` : '<span class="text-muted">Price on request</span>'}
                    </div>
                </div>
                ${crop.farmer_phone ? `
                    <div class="mt-3">
                        <button class="btn btn-sm btn-outline-primary" onclick="contactFarmer('${crop.farmer_phone}', '${crop.farmer_name}')">
                            <i class="fas fa-phone me-1"></i>Contact Farmer
                        </button>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function contactFarmer(phone, name) {
    const message = `Hello ${name}, I'm interested in your crop listing. Please contact me to discuss.`;
    window.open(`tel:${phone}`, '_blank');
    showAlert(`Contact ${name} at ${phone}`, 'info');
}

// Form handling
function initializeForms() {
    // Farmer registration form
    document.getElementById('farmerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/register-farmer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showAlert(`Registration successful! Your Farmer ID is: ${result.farmer_id}`, 'success');
                bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
                e.target.reset();
            } else {
                showAlert(result.error || 'Registration failed', 'danger');
            }
        } catch (error) {
            showAlert('Network error. Please try again.', 'danger');
        }
    });

    // Buyer registration form
    document.getElementById('buyerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/register-buyer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showAlert(`Registration successful! Your Buyer ID is: ${result.buyer_id}`, 'success');
                bootstrap.Modal.getInstance(document.getElementById('registerModal')).hide();
                e.target.reset();
            } else {
                showAlert(result.error || 'Registration failed', 'danger');
            }
        } catch (error) {
            showAlert('Network error. Please try again.', 'danger');
        }
    });

    // List crop form
    document.getElementById('listCropForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData.entries());
        
        // Convert numeric fields
        data.farmer_id = parseInt(data.farmer_id);
        data.quantity = parseFloat(data.quantity);
        if (data.price_per_unit) data.price_per_unit = parseFloat(data.price_per_unit);
        
        try {
            const response = await fetch('/api/list-crop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showAlert('Crop listed successfully!', 'success');
                bootstrap.Modal.getInstance(document.getElementById('listCropModal')).hide();
                e.target.reset();
                loadInitialCrops(); // Refresh listings
            } else {
                showAlert(result.error || 'Failed to list crop', 'danger');
            }
        } catch (error) {
            showAlert('Network error. Please try again.', 'danger');
        }
    });
}

// Utility functions
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add some sample data on page load for demonstration
window.addEventListener('load', () => {
    // Add a small delay to ensure everything is loaded
    setTimeout(() => {
        console.log('AI Farmer Assistant loaded successfully!');
    }, 1000);
});