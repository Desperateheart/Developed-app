const tabs = document.querySelectorAll('.tab');
const panels = document.querySelectorAll('.panel');

tabs.forEach(btn => {
  btn.addEventListener('click', () => {
    tabs.forEach(b => b.classList.remove('active'));
    panels.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});

// Diagnose
const diagnoseForm = document.getElementById('diagnoseForm');
const diagnoseResult = document.getElementById('diagnoseResult');

diagnoseForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  diagnoseResult.textContent = 'Analyzing...';
  const fileInput = document.getElementById('leafImage');
  if (!fileInput.files.length) return;
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  try {
    const res = await fetch('/api/disease/predict', { method: 'POST', body: formData });
    const data = await res.json();
    diagnoseResult.textContent = `Disease: ${data.disease_name}\nConfidence: ${(data.confidence*100).toFixed(1)}%\nRecommendations: ${data.recommendations}\nFeatures: ${JSON.stringify(data.features, null, 2)}`;
  } catch (err) {
    diagnoseResult.textContent = 'Error analyzing image.';
  }
});

// Advice
const adviceForm = document.getElementById('adviceForm');
const adviceResult = document.getElementById('adviceResult');

adviceForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  adviceResult.textContent = 'Fetching advice...';
  const payload = {
    crop: document.getElementById('crop').value,
    growth_stage: document.getElementById('growth_stage').value,
    area_m2: parseFloat(document.getElementById('area_m2').value || '50'),
    soil_type: document.getElementById('soil_type').value || null,
    soil_ph: document.getElementById('soil_ph').value ? parseFloat(document.getElementById('soil_ph').value) : null,
    soil_moisture_pct: document.getElementById('soil_moisture_pct').value ? parseFloat(document.getElementById('soil_moisture_pct').value) : null,
    latitude: document.getElementById('latitude').value ? parseFloat(document.getElementById('latitude').value) : null,
    longitude: document.getElementById('longitude').value ? parseFloat(document.getElementById('longitude').value) : null,
  };
  try {
    const res = await fetch('/api/advice/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const data = await res.json();
    adviceResult.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    adviceResult.textContent = 'Error getting advice.';
  }
});

// Market
const listingForm = document.getElementById('listingForm');
const listingsDiv = document.getElementById('listings');
const priceForm = document.getElementById('priceForm');
const priceResult = document.getElementById('priceResult');

async function loadListings() {
  try {
    const res = await fetch('/api/market/listings');
    const data = await res.json();
    listingsDiv.innerHTML = '';
    data.forEach(l => {
      const card = document.createElement('div');
      card.className = 'card';
      card.style.padding = '10px';
      card.style.border = '1px solid #e2e8f0';
      card.style.borderRadius = '8px';
      card.style.marginBottom = '8px';
      card.textContent = `${l.seller_name} selling ${l.quantity_kg} kg ${l.crop} @ $${l.price_per_kg}/kg (${l.region}) Contact: ${l.contact_info}`;
      listingsDiv.appendChild(card);
    });
  } catch {}
}

listingForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    seller_name: document.getElementById('seller_name').value,
    crop: document.getElementById('listing_crop').value,
    quantity_kg: parseFloat(document.getElementById('quantity_kg').value),
    price_per_kg: parseFloat(document.getElementById('price_per_kg').value),
    region: document.getElementById('region').value,
    contact_info: document.getElementById('contact_info').value,
    description: document.getElementById('description').value || null,
  };
  try {
    await fetch('/api/market/listings', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    listingForm.reset();
    await loadListings();
  } catch {}
});

priceForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const crop = document.getElementById('price_crop').value;
  const region = document.getElementById('price_region').value;
  try {
    const url = new URL(location.origin + '/api/market/fair_price');
    url.searchParams.set('crop', crop);
    if (region) url.searchParams.set('region', region);
    const res = await fetch(url.toString());
    const data = await res.json();
    priceResult.textContent = `Fair price for ${data.crop}${data.region ? ' in ' + data.region : ''}: $${data.median_price_per_kg}/kg (source: ${data.source}, ${data.data_points} pts)`;
  } catch {
    priceResult.textContent = 'Error fetching price.';
  }
});

loadListings();