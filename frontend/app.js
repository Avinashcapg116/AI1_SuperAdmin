/**
 * Ai1 Super App - Cross-Platform Frontend Controller & Presentation Logic
 * Fully optimized for iOS Safari, Android Chrome, and Desktop responsive viewports.
 */

const API_BASE = "/api/v1";

// Global App State
let state = {
  user: {
    id: "USR-DEMO-01",
    name: "Arjun Sundaram",
    phone: "+91 98765 43210",
    language: "en"
  },
  wallet: {
    balance: 3500.0,
    ai1_coins: 250,
    upi_vpa: "9876543210@ai1"
  },
  currentRole: "customer", // customer, partner, admin
  activeModule: "qc",
  language: "en",
  cart: [],
  activeRide: null,
  activeEvSession: {
    id: "EV-SES-DEMO1",
    station_name: "Tata Power EZ Charge - Indiranagar",
    connector_type: "CCS2 (60 kW)",
    energy_delivered_kwh: 4.2,
    soc_current_pct: 34,
    soc_target_pct: 85,
    total_cost: 81.9,
    status: "charging"
  },
  activeOrder: null,
  currentProposal: null,
  mapInstance: null,
  stations: [],
  hapticsEnabled: true,
  networkSpeed: "5g",
  deviceMode: "default"
};

// ==========================================
// 1. INITIALIZATION & LIFECYCLE
// ==========================================
document.addEventListener("DOMContentLoaded", async () => {
  setupSwipeToDismissSheets();
  setupTouchSoundAndHaptics();
  await fetchWallet();
  await selectModule("qc");
  await fetchSuggestions();
  setupWebSocketViewport();

  // Listen to viewport resize for Leaflet map recalculation
  window.addEventListener("resize", () => {
    if (state.mapInstance) {
      setTimeout(() => state.mapInstance.invalidateSize(), 200);
    }
  });
});

// Haptic & Tactile Feedback Simulation
function triggerHaptic(duration = 15) {
  if (state.hapticsEnabled && "vibrate" in navigator) {
    try {
      navigator.vibrate(duration);
    } catch (e) {
      // Ignored if permissions not active
    }
  }
}

function toggleHaptics() {
  state.hapticsEnabled = !state.hapticsEnabled;
  const btn = document.getElementById("hapticsToggleBtn");
  if (btn) {
    btn.innerText = state.hapticsEnabled ? "ON (Vibrate 15ms)" : "OFF";
    btn.classList.toggle("active", state.hapticsEnabled);
  }
  if (state.hapticsEnabled) triggerHaptic(30);
}

function setupTouchSoundAndHaptics() {
  document.addEventListener("touchstart", (e) => {
    if (e.target.closest("button") || e.target.closest(".module-card") || e.target.closest(".product-card") || e.target.closest(".nav-item")) {
      triggerHaptic(12);
    }
  }, { passive: true });
}

// Device Viewport Simulation Tools
function setDeviceMode(mode, btn) {
  triggerHaptic(20);
  state.deviceMode = mode;
  const container = document.getElementById("appContainer");
  if (!container) return;

  container.classList.remove("device-iphone", "device-samsung", "device-tablet", "device-full");
  if (mode === "samsung") {
    container.classList.add("device-samsung");
  } else if (mode === "tablet") {
    container.classList.add("device-tablet");
  } else if (mode === "full") {
    container.classList.add("device-full");
  } else {
    container.classList.add("device-iphone");
  }

  document.querySelectorAll(".desktop-toolbar .toolbar-pill").forEach(el => el.classList.remove("active"));
  if (btn) btn.classList.add("active");

  if (state.mapInstance) {
    setTimeout(() => state.mapInstance.invalidateSize(), 300);
  }
}

function simulateNetworkSpeed(speed) {
  state.networkSpeed = speed;
  triggerHaptic(20);
  if (speed === "2g") {
    alert("2G Lite Mode: Low bandwidth optimizations enabled. Asset caching active for slow networks.");
  }
}

// Swipe-to-Dismiss Bottom Sheets on iOS & Android
function setupSwipeToDismissSheets() {
  document.querySelectorAll(".sheet-content").forEach(sheet => {
    let startY = 0;
    let currentY = 0;
    let isDragging = false;

    sheet.addEventListener("touchstart", (e) => {
      // Only drag if scrolled to top
      if (sheet.scrollTop <= 0) {
        startY = e.touches[0].clientY;
        isDragging = true;
      }
    }, { passive: true });

    sheet.addEventListener("touchmove", (e) => {
      if (!isDragging) return;
      currentY = e.touches[0].clientY;
      const deltaY = currentY - startY;
      if (deltaY > 0) {
        sheet.style.transform = `translateY(${deltaY}px)`;
      }
    }, { passive: true });

    sheet.addEventListener("touchend", () => {
      if (!isDragging) return;
      isDragging = false;
      const deltaY = currentY - startY;
      if (deltaY > 120) {
        // Dismiss sheet
        const modal = sheet.closest(".modal-overlay");
        if (modal) closeModal(modal.id);
      }
      sheet.style.transform = "";
    });
  });
}

async function fetchWallet() {
  try {
    const res = await fetch(`${API_BASE}/wallet`);
    if (res.ok) {
      const data = await res.json();
      state.wallet = data;
      document.getElementById("headerWalletBalance").innerText = Math.round(data.balance).toLocaleString("en-IN");
      document.getElementById("headerAi1Coins").innerText = data.ai1_coins;
    }
  } catch (err) {
    console.error("Wallet fetch error:", err);
  }
}

function toggleDarkMode() {
  triggerHaptic(15);
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
}

function changeLanguage(lang) {
  triggerHaptic(15);
  state.language = lang;
  document.getElementById("assistantLangBadge").innerText = `${lang.toUpperCase()} • Voice & Chat Active`;
  const greetings = {
    en: "English activated. How can I help you?",
    hi: "हिंदी सक्रिय है। मैं आपकी क्या मदद कर सकता हूँ?",
    kn: "ಕನ್ನಡ ಸಕ್ರಿಯವಾಗಿದೆ. ನಿಮಗೆ ಏನು ಸಹಾಯ ಬೇಕು?",
    ta: "தமிழ் செயல்படுத்தப்பட்டது. நான் உங்களுக்கு எவ்வாறு உதவ முடியும்?",
    te: "తెలుగు సక్రియం చేయబడింది. నేను మీకు ఎలా సహాయపಡగలను?"
  };
  addChatMessage("assistant", greetings[lang] || greetings.en);
}

function toggleRoleApp() {
  triggerHaptic(20);
  if (state.currentRole === "customer") {
    state.currentRole = "partner";
    document.getElementById("customerView").style.display = "none";
    document.getElementById("partnerView").style.display = "block";
    document.getElementById("adminView").style.display = "none";
    document.getElementById("currentRoleText").innerText = "Partner Console";
    loadPartnerDashboard("rider");
  } else if (state.currentRole === "partner") {
    state.currentRole = "admin";
    document.getElementById("customerView").style.display = "none";
    document.getElementById("partnerView").style.display = "none";
    document.getElementById("adminView").style.display = "block";
    document.getElementById("currentRoleText").innerText = "Platform Admin";
    loadAdminDashboard();
  } else {
    state.currentRole = "customer";
    document.getElementById("customerView").style.display = "block";
    document.getElementById("partnerView").style.display = "none";
    document.getElementById("adminView").style.display = "none";
    document.getElementById("currentRoleText").innerText = "Customer";
  }
}

function navTo(tab) {
  triggerHaptic(15);
  if (tab === "home") {
    state.currentRole = "customer";
    document.getElementById("customerView").style.display = "block";
    document.getElementById("partnerView").style.display = "none";
    document.getElementById("adminView").style.display = "none";
    document.getElementById("currentRoleText").innerText = "Customer";
    selectModule("qc");
  }
}

// ==========================================
// 2. MODULE NAVIGATION & RENDERING
// ==========================================
async function selectModule(moduleKey) {
  triggerHaptic(15);
  state.activeModule = moduleKey;

  // Highlight active card
  document.querySelectorAll(".module-card").forEach(el => el.classList.remove("active"));
  const targetCard = document.getElementById(`mod-${moduleKey}`);
  if (targetCard) targetCard.classList.add("active");

  const container = document.getElementById("moduleContentArea");

  if (moduleKey === "qc") {
    await renderQuickCommerce(container);
  } else if (moduleKey === "rides") {
    await renderRides(container);
  } else if (moduleKey === "ev") {
    await renderEvCharging(container);
  } else if (moduleKey === "home") {
    await renderHomeServices(container);
  } else if (moduleKey === "mechanic") {
    await renderMechanic(container);
  } else if (moduleKey === "travel") {
    await renderTravel(container);
  } else if (moduleKey === "insurance") {
    await renderInsurance(container);
  } else if (moduleKey === "wallet") {
    await renderWalletModule(container);
  }
}

// ==========================================
// 3. QUICK COMMERCE MODULE
// ==========================================
async function renderQuickCommerce(container) {
  try {
    const res = await fetch(`${API_BASE}/qc/products`);
    const products = await res.json();
    const basketRes = await fetch(`${API_BASE}/qc/usual-basket`);
    const usualBasket = await basketRes.json();

    let html = `
      <div style="background: var(--primary-light); border-radius: var(--radius-md); padding: 12px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="font-size: 11px; font-weight: 800; color: var(--primary); text-transform: uppercase;">⚡ 11-Minute Promise</span>
          <div style="font-size: 13px; font-weight: 700;">Delivering to Indiranagar (560038)</div>
        </div>
        <button class="add-btn" onclick="openCartModal()">🛒 Cart (${state.cart.length})</button>
      </div>

      <!-- Usual Basket Card -->
      <div style="border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 12px; margin-bottom: 16px; background: var(--card-light);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-size: 13px; font-weight: 700;">🔄 ${usualBasket.basket_title}</span>
          <span class="badge" style="background:#DCFCE7; color:#15803D;">Save ₹${usualBasket.savings}</span>
        </div>
        <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 10px;">Milk, Whole Wheat Bread, Fresh Eggs</p>
        <button class="btn-primary" style="padding: 8px;" onclick="addUsualBasketToCart()">1-Tap Add Usual Basket (₹${usualBasket.estimated_total})</button>
      </div>

      <!-- Catalog -->
      <div class="section-header">
        <span class="section-title">Fresh Grocery Essentials</span>
        <span class="section-action">View All</span>
      </div>
      <div class="horizontal-scroll">
    `;

    products.forEach(p => {
      html += `
        <div class="product-card">
          <div class="product-image">${p.image_url}</div>
          <div class="product-name">${p.name}</div>
          <div class="product-unit">${p.unit}</div>
          <div class="product-price-row">
            <span class="product-price">₹${p.price}</span>
            <button class="add-btn" onclick="addToCart('${p.id}', '${p.name.replace(/'/g, "\\'")}', ${p.price}, '${p.unit}')">+ Add</button>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<p>Error loading quick commerce: ${err.message}</p>`;
  }
}

function addToCart(id, name, price, unit) {
  triggerHaptic(20);
  const existing = state.cart.find(i => i.product_id === id);
  if (existing) {
    existing.quantity += 1;
    existing.subtotal = existing.quantity * price;
  } else {
    state.cart.push({
      product_id: id,
      product_name: name,
      price: price,
      quantity: 1,
      unit: unit,
      subtotal: price
    });
  }
  fetchWallet();
  selectModule("qc");
}

function addUsualBasketToCart() {
  triggerHaptic(25);
  addToCart("qc-milk-01", "Amul Taaza Milk", 28.0, "500 ml");
  addToCart("qc-bread-01", "Whole Wheat Bread", 55.0, "350 g");
  addToCart("qc-eggs-01", "Fresh Eggs", 52.0, "6 pcs");
  openCartModal();
}

function openCartModal() {
  triggerHaptic(15);
  const body = document.getElementById("cartModalBody");
  if (state.cart.length === 0) {
    body.innerHTML = `
      <h3 style="font-weight: 800; margin-bottom: 8px;">Your Ai1 Cart is Empty</h3>
      <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">Add fresh milk, bread, or fruits to get delivery in 11 minutes.</p>
      <button class="btn-primary" onclick="closeModal('cartModal')">Browse Store</button>
    `;
  } else {
    let subtotal = state.cart.reduce((s, i) => s + i.subtotal, 0);
    let html = `
      <h3 style="font-weight: 800; margin-bottom: 12px;">Checkout (ETA 11 Mins)</h3>
      <div style="max-height: 200px; overflow-y: auto; margin-bottom: 12px;">
    `;
    state.cart.forEach(item => {
      html += `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; font-size:13px;">
          <div><b>${item.product_name}</b> <span style="color:var(--text-muted); font-size:11px;">(${item.unit}) x${item.quantity}</span></div>
          <div>₹${item.subtotal}</div>
        </div>
      `;
    });
    html += `
      </div>
      <div class="proposal-box">
        <div class="proposal-item"><span>Items Subtotal</span><span>₹${subtotal}</span></div>
        <div class="proposal-item"><span>Delivery Partner Fee (10-15m)</span><span style="color:var(--success);">FREE</span></div>
        <div class="proposal-total"><span>Total Payable</span><span>₹${subtotal}</span></div>
      </div>
      <button class="btn-primary" onclick="executeCheckout(${subtotal})">Confirm & Pay from Ai1 Wallet (₹${subtotal})</button>
    `;
    body.innerHTML = html;
  }
  openModal("cartModal");
}

async function executeCheckout(amount) {
  triggerHaptic(30);
  try {
    const res = await fetch(`${API_BASE}/qc/cart/checkout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pincode: "560038",
        delivery_address: "Flat 402, Prestige Palms, Indiranagar",
        items: state.cart,
        use_coins: false
      })
    });
    if (res.ok) {
      const order = await res.json();
      state.cart = [];
      state.activeOrder = order;
      closeModal("cartModal");
      await fetchWallet();
      
      // Update active tray
      document.getElementById("activeTrayIcon").innerText = "🛵";
      document.getElementById("activeTrayTitle").innerText = `Rider Assigned (ETA ${order.slot_eta_mins} mins)`;
      document.getElementById("activeTrayDesc").innerText = `${order.rider_name} (${order.rider_phone}) is on the way.`;
      
      alert(`Order ${order.id} placed successfully! Delivery partner dispatched from Indiranagar Dark Store.`);
      selectModule("qc");
    } else {
      const err = await res.json();
      alert(`Checkout failed: ${err.detail || "Insufficient funds"}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

// ==========================================
// 4. RIDE HAILING MODULE
// ==========================================
async function renderRides(container) {
  container.innerHTML = `
    <div style="background: var(--card-light); border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 14px; margin-bottom: 14px;">
      <h3 style="font-size: 15px; font-weight: 800; margin-bottom: 10px;">Where are you going?</h3>
      <div style="display:flex; flex-direction:column; gap:8px; margin-bottom: 12px;">
        <input type="text" id="ridePickupInput" value="Flat 402, Prestige Palms, Indiranagar" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border-light);" placeholder="Pickup Location">
        <input type="text" id="rideDropInput" value="Kempegowda International Airport (BLR)" style="padding: 10px; border-radius: 8px; border: 1px solid var(--border-light);" placeholder="Drop Destination">
      </div>
      <button class="btn-primary" onclick="calculateRideFares()">Get Fare Estimates</button>
    </div>
    <div id="rideOptionsContainer"></div>
  `;
  await calculateRideFares();
}

async function calculateRideFares() {
  triggerHaptic(15);
  const container = document.getElementById("rideOptionsContainer");
  if (!container) return;
  container.innerHTML = `<p style="font-size:12px; color:var(--text-muted);">Fetching driver network & surge pricing...</p>`;

  try {
    const res = await fetch(`${API_BASE}/rides/estimate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        pickup_address: "Indiranagar",
        pickup_lat: 12.9784,
        pickup_lng: 77.6408,
        drop_address: "Airport",
        drop_lat: 13.1986,
        drop_lng: 77.7066
      })
    });
    const options = await res.json();

    let html = `<div style="display:flex; flex-direction:column; gap:10px;">`;
    options.forEach(opt => {
      html += `
        <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; display:flex; justify-content:space-between; align-items:center; background:var(--card-light);">
          <div>
            <div style="font-size:14px; font-weight:800;">${opt.title} <span class="badge" style="background:#EBF3FF; color:#0066FF;">${opt.eta_mins} mins away</span></div>
            <div style="font-size:11px; color:var(--text-muted);">Capacity: ${opt.capacity} seats • CO2 Saved: ${opt.co2_saved_kg} kg</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:16px; font-weight:800;">₹${opt.final_fare}</div>
            <button class="btn-primary" style="padding:6px 14px; font-size:12px; margin-top:4px;" onclick="bookRide('${opt.category}', ${opt.final_fare})">Book</button>
          </div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<p>Error: ${err.message}</p>`;
  }
}

async function bookRide(category, fare) {
  triggerHaptic(30);
  try {
    const res = await fetch(`${API_BASE}/rides/book`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: category,
        pickup_address: "Indiranagar",
        pickup_lat: 12.9784,
        pickup_lng: 77.6408,
        drop_address: "Kempegowda International Airport",
        drop_lat: 13.1986,
        drop_lng: 77.7066,
        use_coins: false
      })
    });
    if (res.ok) {
      const ride = await res.json();
      state.activeRide = ride;
      await fetchWallet();
      openRideModal(ride);
    } else {
      const err = await res.json();
      alert(`Booking failed: ${err.detail || "Error"}`);
    }
  } catch (err) {
    alert(`Error booking ride: ${err.message}`);
  }
}

function openRideModal(ride) {
  triggerHaptic(20);
  const body = document.getElementById("rideModalBody");
  body.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <h3 style="font-weight:800; font-size:16px;">Driver En Route (${ride.vehicle_model})</h3>
      <span class="badge badge-available">OTP: ${ride.otp}</span>
    </div>
    <div style="background:var(--bg-light); border-radius:var(--radius-md); padding:12px; margin-bottom:12px;">
      <div style="font-size:14px; font-weight:700;">${ride.driver_name} ★ ${ride.driver_rating}</div>
      <div style="font-size:12px; color:var(--text-muted);">${ride.vehicle_number} • Phone: ${ride.driver_phone}</div>
    </div>
    <div style="display:flex; gap:8px;">
      <button class="btn-primary" style="flex:1; background:var(--danger);" onclick="triggerRideSos('${ride.id}')">🚨 Emergency SOS</button>
      <button class="btn-primary" style="flex:1; background:var(--text-dark);" onclick="alert('Trip tracking link copied to clipboard!')">🔗 Share Trip</button>
    </div>
  `;
  openModal("rideModal");
}

async function triggerRideSos(rideId) {
  triggerHaptic(50);
  const res = await fetch(`${API_BASE}/rides/${rideId}/sos`, { method: "POST" });
  if (res.ok) {
    const data = await res.json();
    alert(`🚨 SOS TRIGGERED! Bengaluru Police (112) and emergency contacts alerted.\nTracking URL: ${data.shareable_live_tracking_url}`);
  }
}

// ==========================================
// 5. REAL-TIME EV CHARGING MODULE
// ==========================================
async function renderEvCharging(container) {
  container.innerHTML = `
    <div style="background: var(--card-light); border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 12px; margin-bottom: 12px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-size: 14px; font-weight: 800;">⚡ Ai1 Real-Time EV Grid (Bengaluru)</span>
        <span class="badge badge-available">WebSocket Live</span>
      </div>
      <div id="map"></div>
      <div style="display: flex; gap: 6px; overflow-x: auto; padding-top: 4px;">
        <button class="add-btn" onclick="filterStations(null)">All Connectors</button>
        <button class="add-btn" onclick="filterStations('CCS2')">CCS2 Fast</button>
        <button class="add-btn" onclick="filterStations('Type 2')">Type 2 AC</button>
        <button class="add-btn" onclick="openRoutePlannerModal()">🗺️ Route Planner</button>
      </div>
    </div>
    <div id="stationsList"></div>
  `;

  setTimeout(initLeafletMap, 100);
}

async function initLeafletMap() {
  const mapElement = document.getElementById("map");
  if (!mapElement) return;

  if (state.mapInstance) {
    state.mapInstance.remove();
  }

  // Optimized for mobile touch without gesture blocking
  state.mapInstance = L.map("map", {
    tap: false,
    zoomControl: true
  }).setView([12.9716, 77.5946], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© OpenStreetMap contributors"
  }).addTo(state.mapInstance);

  await loadEvStations();
}

async function loadEvStations(filterConnector = null) {
  try {
    let url = `${API_BASE}/ev/stations`;
    if (filterConnector) url += `?connector_type=${filterConnector}`;

    const res = await fetch(url);
    const stations = await res.json();
    state.stations = stations;

    stations.forEach(stn => {
      const availCount = stn.connectors.filter(c => c.status === "available").length;
      const markerColor = availCount > 0 ? "#10B981" : "#EF4444";
      
      const marker = L.circleMarker([stn.lat, stn.lng], {
        radius: 11,
        fillColor: markerColor,
        color: "#ffffff",
        weight: 2.5,
        opacity: 1,
        fillOpacity: 0.95
      }).addTo(state.mapInstance);

      marker.bindPopup(`<b>${stn.name}</b><br>${stn.operator_name}<br>Available: ${availCount}/${stn.connectors.length}<br><button onclick="openEvStationSheet('${stn.id}')" style="margin-top:6px; font-size:11px; padding:3px 10px; cursor:pointer; background:#0066FF; color:white; border:none; border-radius:6px;">View Connectors</button>`);
    });

    const listEl = document.getElementById("stationsList");
    if (!listEl) return;

    let html = `<div style="display:flex; flex-direction:column; gap:10px;">`;
    stations.forEach(stn => {
      const availCount = stn.connectors.filter(c => c.status === "available").length;
      html += `
        <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; background:var(--card-light); cursor:pointer;" onclick="openEvStationSheet('${stn.id}')">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div style="font-size:14px; font-weight:800;">${stn.name}</div>
            <span class="badge ${availCount > 0 ? 'badge-available' : 'badge-occupied'}">${availCount} Available</span>
          </div>
          <div style="font-size:11px; color:var(--text-muted); margin: 4px 0;">${stn.address}</div>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:var(--text-muted);">
            <span>Uptime: ${stn.reliability_score}%</span>
            <span>Tariff: ~₹19.5/kWh</span>
          </div>
        </div>
      `;
    });
    html += `</div>`;
    listEl.innerHTML = html;
  } catch (err) {
    console.error("Error loading EV stations:", err);
  }
}

function filterStations(connector) {
  triggerHaptic(15);
  loadEvStations(connector);
}

function openEvStationSheet(stationId) {
  triggerHaptic(20);
  const stn = state.stations.find(s => s.id === stationId);
  if (!stn) return;

  const body = document.getElementById("evStationModalBody");
  let html = `
    <h3 style="font-size:16px; font-weight:800; margin-bottom:4px;">${stn.name}</h3>
    <p style="font-size:12px; color:var(--text-muted); margin-bottom:12px;">${stn.address} • Operated by ${stn.operator_name}</p>
    
    <div style="font-size:13px; font-weight:700; margin-bottom:8px;">Live Connectors (${stn.connectors.length})</div>
    <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
  `;

  stn.connectors.forEach(conn => {
    html += `
      <div style="border:1px solid var(--border-light); border-radius:8px; padding:10px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-weight:700; font-size:13px;">${conn.connector_type} (${conn.power_kw} kW)</div>
          <div style="font-size:11px; color:var(--text-muted);">₹${conn.tariff_per_kwh}/kWh • Heartbeat: ${conn.last_heartbeat}</div>
        </div>
        <div style="display:flex; gap:6px;">
          <button class="add-btn" onclick="reserveConnector('${stn.id}', '${conn.id}')">Hold 15m</button>
          <button class="btn-primary" style="padding:4px 10px; font-size:11px;" onclick="startEvSession('${stn.id}', '${conn.id}')">Start</button>
        </div>
      </div>
    `;
  });

  html += `
    </div>
    <div style="display:flex; gap:8px;">
      <button class="btn-primary" style="flex:1; background:var(--bg-light); color:var(--text-dark); border:1px solid var(--border-light);" onclick="alert('Thank you for reporting! Feedback sent to Ai1 Grid.')">⚠️ Report Issue</button>
      <button class="btn-primary" style="flex:1;" onclick="closeModal('evStationModal')">Done</button>
    </div>
  `;
  body.innerHTML = html;
  openModal("evStationModal");
}

async function reserveConnector(stationId, connectorId) {
  triggerHaptic(25);
  const res = await fetch(`${API_BASE}/ev/reservations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      station_id: stationId,
      connector_id: connectorId,
      hold_minutes: 15
    })
  });
  const data = await res.json();
  if (res.ok) {
    alert(`Connector locked for 15 minutes! Please arrive before expiry.`);
    closeModal("evStationModal");
  } else {
    alert(`Reservation failed: ${data.detail || data.error}`);
  }
}

async function startEvSession(stationId, connectorId) {
  triggerHaptic(30);
  const res = await fetch(`${API_BASE}/ev/sessions/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      station_id: stationId,
      connector_id: connectorId,
      target_soc: 85
    })
  });
  if (res.ok) {
    const data = await res.json();
    state.activeEvSession = data.session;
    closeModal("evStationModal");
    openLiveEvSessionModal();
  } else {
    const err = await res.json();
    alert(`Failed to start: ${err.detail || "Error"}`);
  }
}

function openLiveEvSessionModal() {
  triggerHaptic(20);
  const s = state.activeEvSession;
  const body = document.getElementById("evLiveSessionBody");
  body.innerHTML = `
    <div style="text-align:center; margin-bottom:16px;">
      <span class="badge badge-available" style="font-size:12px; margin-bottom:6px;">LIVE TELEMETRY ACTIVE</span>
      <h3 style="font-weight:800; font-size:18px;">Ai1 SmartGrid Session</h3>
      <p style="font-size:12px; color:var(--text-muted);">${s.station_name} • ${s.connector_type}</p>
    </div>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px;">
      <div style="background:var(--bg-light); padding:12px; border-radius:12px; text-align:center;">
        <div style="font-size:24px; font-weight:800; color:var(--primary);">${s.energy_delivered_kwh} kWh</div>
        <div style="font-size:11px; color:var(--text-muted);">Energy Delivered</div>
      </div>
      <div style="background:var(--bg-light); padding:12px; border-radius:12px; text-align:center;">
        <div style="font-size:24px; font-weight:800; color:var(--success);">${s.soc_current_pct}%</div>
        <div style="font-size:11px; color:var(--text-muted);">State of Charge (SoC)</div>
      </div>
    </div>

    <div class="proposal-box">
      <div class="proposal-item"><span>Current Charging Power</span><span>60.0 kW (DC Fast)</span></div>
      <div class="proposal-item"><span>Running Tariff</span><span>₹${s.total_cost}</span></div>
      <div class="proposal-total"><span>Payment Source</span><span>Ai1 Unified Wallet</span></div>
    </div>

    <button class="btn-primary" style="background:var(--danger);" onclick="stopEvSession('${s.id}')">Stop Charging & Deduct from Wallet</button>
  `;
  openModal("evLiveSessionModal");
}

async function stopEvSession(sessionId) {
  triggerHaptic(30);
  const res = await fetch(`${API_BASE}/ev/sessions/stop`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId })
  });
  if (res.ok) {
    const data = await res.json();
    alert(`Charging complete! ${data.energy_delivered_kwh} kWh delivered. ₹${data.total_cost} deducted from your Ai1 Wallet.`);
    closeModal("evLiveSessionModal");
    await fetchWallet();
    selectModule("ev");
  }
}

function openRoutePlannerModal() {
  triggerHaptic(20);
  alert("Ai1 EV Route Planner\nOrigin: Indiranagar ➔ Destination: Airport (NH 44)\nDistance: 28 km\nRecommended Stop: Ai1 FastGrid Airport Highway (150kW Ultra)");
}

// ==========================================
// 6. HOME SERVICES & MECHANIC
// ==========================================
async function renderHomeServices(container) {
  const res = await fetch(`${API_BASE}/services/items`);
  const items = await res.json();

  let html = `
    <div class="section-header">
      <span class="section-title">Verified Urban Home Services</span>
      <span class="badge badge-available">30-day Warranty</span>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
  `;

  items.forEach(item => {
    html += `
      <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; background:var(--card-light); display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:14px; font-weight:800;">${item.image_url} ${item.title}</div>
          <div style="font-size:11px; color:var(--text-muted);">${item.description}</div>
          <div style="font-size:12px; font-weight:700; color:var(--primary); margin-top:4px;">₹${item.price} • ${item.duration_mins} mins</div>
        </div>
        <button class="btn-primary" style="padding:6px 12px; font-size:12px;" onclick="bookHomeService('${item.id}')">Book Slot</button>
      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
}

async function bookHomeService(serviceId) {
  triggerHaptic(25);
  const res = await fetch(`${API_BASE}/services/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      service_id: serviceId,
      scheduled_date: "Tomorrow",
      time_slot: "10:00 AM - 12:00 PM",
      address: "Indiranagar 100ft Road"
    })
  });
  if (res.ok) {
    const data = await res.json();
    alert(`Service Scheduled!\nProfessional: ${data.pro_name}\nStart OTP: ${data.start_otp}\nScheduled Slot: ${data.scheduled_slot}`);
    await fetchWallet();
  }
}

async function renderMechanic(container) {
  container.innerHTML = `
    <div style="background:linear-gradient(135deg, #EF4444, #B91C1C); color:white; border-radius:var(--radius-md); padding:16px; margin-bottom:14px;">
      <h3 style="font-size:16px; font-weight:800; margin-bottom:4px;">🚨 Breakdown & Roadside Assistance (SOS)</h3>
      <p style="font-size:12px; opacity:0.9; margin-bottom:12px;">Flat tyre, battery jumpstart, towing, or overheated engine anywhere in Bengaluru.</p>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px;">
        <button class="btn-primary" style="background:white; color:var(--danger);" onclick="triggerBreakdownSos('flat_tyre')">Flat Tyre Fix (₹350)</button>
        <button class="btn-primary" style="background:white; color:var(--danger);" onclick="triggerBreakdownSos('battery_dead')">Battery Jumpstart (₹499)</button>
      </div>
    </div>
    
    <div class="section-header">
      <span class="section-title">Doorstep Vehicle Servicing</span>
    </div>
    <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; background:var(--card-light);">
      <div style="font-size:14px; font-weight:800;">Comprehensive Periodic Car Service</div>
      <p style="font-size:11px; color:var(--text-muted); margin-bottom:8px;">Synthetic engine oil, air/oil filter, 40-point diagnostic check, wash.</p>
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:16px; font-weight:800;">₹3,499</span>
        <button class="btn-primary" style="padding:6px 12px; font-size:12px;" onclick="alert('Doorstep technician scheduled for Saturday!')">Book</button>
      </div>
    </div>
  `;
}

async function triggerBreakdownSos(type) {
  triggerHaptic(40);
  const res = await fetch(`${API_BASE}/mechanic/breakdown-sos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      emergency_type: type,
      vehicle_type: "car",
      location_address: "Near Dell Ring Road, Domlur",
      lat: 12.9609,
      lng: 77.6387
    })
  });
  if (res.ok) {
    const job = await res.json();
    alert(`🚨 MECHANIC DISPATCHED!\nTechnician: ${job.technician_name}\nPhone: ${job.technician_phone}\nEstimated Cost: ₹${job.estimated_cost}`);
  }
}

// ==========================================
// 7. TRAVEL & INSURANCE
// ==========================================
async function renderTravel(container) {
  container.innerHTML = `
    <div style="background:var(--card-light); border:1px solid var(--border-light); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
      <h3 style="font-size:15px; font-weight:800; margin-bottom:10px;">Check IRCTC Live Train PNR</h3>
      <div style="display:flex; gap:8px;">
        <input type="text" id="pnrInput" value="8423451290" style="flex:1; padding:8px 12px; border-radius:8px; border:1px solid var(--border-light);" placeholder="10-digit PNR">
        <button class="btn-primary" style="width:auto; padding:8px 14px;" onclick="checkPnr()">Check</button>
      </div>
      <div id="pnrResultArea" style="margin-top:10px;"></div>
    </div>

    <div class="section-header">
      <span class="section-title">Popular Flights from Bengaluru</span>
    </div>
    <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; background:var(--card-light); margin-bottom:8px;">
      <div style="display:flex; justify-content:space-between;">
        <div><b>IndiGo 6E-512</b> (BLR to DEL)</div>
        <div style="font-weight:800;">₹5,499</div>
      </div>
      <div style="font-size:11px; color:var(--text-muted); margin:4px 0;">06:15 AM - 09:05 AM • Non-stop (2h 50m)</div>
      <button class="btn-primary" style="padding:6px; font-size:12px; margin-top:6px;" onclick="bookTripItinerary()">Book Flight + Airport Cab + Travel Insurance (₹6,328)</button>
    </div>
  `;
}

async function checkPnr() {
  triggerHaptic(20);
  const pnr = document.getElementById("pnrInput").value;
  const res = await fetch(`${API_BASE}/travel/trains/pnr?pnr=${pnr}`);
  const data = await res.json();
  const area = document.getElementById("pnrResultArea");
  area.innerHTML = `
    <div class="proposal-box">
      <div style="font-weight:800; font-size:13px;">${data.train_name} (${data.train_number})</div>
      <div style="font-size:11px; color:var(--text-muted); margin-bottom:6px;">${data.from_station} ➔ ${data.to_station}</div>
      <div class="proposal-item"><span>Passenger 1</span><span class="badge badge-available">Coach C4 / Berth 42 (CNF)</span></div>
      <div class="proposal-item"><span>Confirmation Probability</span><span>${data.confirmation_probability}%</span></div>
    </div>
  `;
}

async function bookTripItinerary() {
  triggerHaptic(30);
  const res = await fetch(`${API_BASE}/travel/itinerary/build`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      travel_type: "flight",
      origin: "BLR",
      destination: "DEL",
      date: "Tomorrow",
      add_airport_cab: true,
      add_travel_insurance: true
    })
  });
  if (res.ok) {
    const data = await res.json();
    alert(`Trip Bundle Confirmed!\nBooking ID: ${data.booking_details.booking_id}\nTotal Fare: ₹${data.booking_details.total_fare}\nIncludes Flight + Cab Pickup + Travel Insurance`);
    await fetchWallet();
  }
}

async function renderInsurance(container) {
  const res = await fetch(`${API_BASE}/insurance/quotes`);
  const quotes = await res.json();

  let html = `
    <div class="section-header">
      <span class="section-title">Instant Digital Policy Vault</span>
      <span class="badge badge-available">15-day Free Look</span>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
  `;

  quotes.forEach(q => {
    html += `
      <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; background:var(--card-light);">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:11px; font-weight:800; color:var(--primary);">${q.insurer_name}</span>
          <span style="font-weight:800; font-size:15px;">₹${q.premium_annual}/yr</span>
        </div>
        <div style="font-size:14px; font-weight:800; margin:2px 0;">${q.plan_name}</div>
        <div style="font-size:11px; color:var(--text-muted); margin-bottom:8px;">Cover: ₹${(q.cover_amount/100000).toFixed(1)} Lakhs • Settlement Ratio: ${q.irda_claim_settlement_ratio}%</div>
        <button class="btn-primary" style="padding:6px 12px; font-size:12px;" onclick="buyPolicy('${q.quote_id}', '${q.plan_name}', ${q.premium_annual})">Buy with 1-Click KYC</button>
      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
}

async function buyPolicy(quoteId, planName, premium) {
  triggerHaptic(30);
  const res = await fetch(`${API_BASE}/insurance/buy`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      quote_id: quoteId,
      insured_name: state.user.name,
      insured_pan_or_aadhaar: "ABCDE1234F"
    })
  });
  if (res.ok) {
    const pol = await res.json();
    alert(`Policy Issued Instantly!\nPolicy No: ${pol.policy_number}\nInsurer: ${pol.insurer_name}\nFree-look cancellation allowed until ${pol.free_look_ends}`);
    await fetchWallet();
  } else {
    alert("Insufficient balance in Ai1 Wallet. Please top-up.");
  }
}

// ==========================================
// 8. PAYMENTS & WALLET MODULE
// ==========================================
async function renderWalletModule(container) {
  const txnsRes = await fetch(`${API_BASE}/wallet/transactions`);
  const txns = await txnsRes.json();

  let html = `
    <div style="background:linear-gradient(135deg, #0066FF, #0044B3); color:white; border-radius:var(--radius-md); padding:16px; margin-bottom:14px;">
      <div style="font-size:12px; opacity:0.9;">Ai1 Unified Super Wallet (RBI PPI Compliant)</div>
      <div style="font-size:28px; font-weight:800; margin:4px 0;">₹${Math.round(state.wallet.balance).toLocaleString("en-IN")}</div>
      <div style="font-size:12px;">UPI ID: <b>${state.wallet.upi_vpa}</b> • <b>${state.wallet.ai1_coins}</b> Ai1 Coins 🪙</div>
      <div style="display:flex; gap:8px; margin-top:12px;">
        <button class="btn-primary" style="background:white; color:var(--primary); padding:6px 12px; font-size:12px;" onclick="topUpWallet(1000)">+ Add ₹1,000</button>
        <button class="btn-primary" style="background:rgba(255,255,255,0.2); padding:6px 12px; font-size:12px;" onclick="simulateQrScan()">Scan Bharat QR</button>
      </div>
    </div>

    <div class="section-header">
      <span class="section-title">Recharges & Bill Payments</span>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:16px;">
      <button class="btn-primary" style="background:var(--bg-light); color:var(--text-dark); border:1px solid var(--border-light); font-size:12px;" onclick="payBill('fastag', 'NHAI FASTag', 500)">🚗 FASTag (₹500)</button>
      <button class="btn-primary" style="background:var(--bg-light); color:var(--text-dark); border:1px solid var(--border-light); font-size:12px;" onclick="payBill('electricity', 'BESCOM', 450)">⚡ BESCOM (₹450)</button>
    </div>

    <div class="section-header">
      <span class="section-title">Transaction History Across All Modules</span>
    </div>
    <div style="max-height:220px; overflow-y:auto; -webkit-overflow-scrolling:touch;">
  `;

  if (txns.length === 0) {
    html += `<p style="font-size:12px; color:var(--text-muted);">No transactions yet.</p>`;
  } else {
    txns.forEach(t => {
      html += `
        <div style="border-bottom:1px solid var(--border-light); padding:8px 0; display:flex; justify-content:space-between; align-items:center; font-size:13px;">
          <div>
            <div style="font-weight:700;">${t.description}</div>
            <div style="font-size:11px; color:var(--text-muted);">${t.reference_module.toUpperCase()} • ${t.timestamp.slice(11, 16)}</div>
          </div>
          <div style="font-weight:800; color:${t.type === 'debit' ? 'var(--danger)' : 'var(--success)'};">
            ${t.type === 'debit' ? '-' : '+'}₹${t.amount}
          </div>
        </div>
      `;
    });
  }

  html += `</div>`;
  container.innerHTML = html;
}

async function topUpWallet(amount) {
  triggerHaptic(25);
  const res = await fetch(`${API_BASE}/wallet/top-up`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount: amount, payment_method: "upi" })
  });
  if (res.ok) {
    alert(`₹${amount} added to Ai1 Wallet!`);
    await fetchWallet();
    selectModule("wallet");
  }
}

async function payBill(cat, biller, amount) {
  triggerHaptic(25);
  const res = await fetch(`${API_BASE}/wallet/bill-payment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      category: cat,
      biller_name: biller,
      consumer_number: "KA03MX8899",
      amount: amount
    })
  });
  if (res.ok) {
    alert(`${biller} bill of ₹${amount} paid successfully via BBPS! Cashback coins credited.`);
    await fetchWallet();
    selectModule("wallet");
  }
}

function simulateQrScan() {
  triggerHaptic(30);
  alert("BharatQR Scanned: 'Indiranagar Fresh Mart' (merchant@icici)\nProcessing payment from Ai1 Wallet...");
  payBill("qr_merchant", "Indiranagar Fresh Mart", 120);
}

// ==========================================
// 9. MULTILINGUAL AI ASSISTANT (CORE)
// ==========================================
function openAssistantModal(startVoice = false) {
  triggerHaptic(20);
  openModal("assistantModal");
  if (startVoice) startVoiceInput();
}

async function sendAssistantQuery(queryText) {
  triggerHaptic(20);
  addChatMessage("user", queryText);
  await executeAssistantNlp(queryText);
}

async function submitAssistantChat() {
  const input = document.getElementById("assistantMessageInput");
  const msg = input.value.trim();
  if (!msg) return;
  input.value = "";
  triggerHaptic(15);
  addChatMessage("user", msg);
  await executeAssistantNlp(msg);
}

async function executeAssistantNlp(queryText) {
  try {
    const res = await fetch(`${API_BASE}/assistant/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: queryText,
        language: state.language
      })
    });
    const data = await res.json();
    addChatMessage("assistant", data.reply_text);

    // Speak response if Web Speech synthesis is available
    if ('speechSynthesis' in window) {
      try {
        const utter = new SpeechSynthesisUtterance(data.reply_text.split('\n')[0]);
        window.speechSynthesis.speak(utter);
      } catch (e) {
        // Ignored if user hasn't interacted
      }
    }

    // Render Proposal Card if two-phase commit
    const proposalBox = document.getElementById("proposalContainer");
    if (data.action_proposal) {
      state.currentProposal = data.action_proposal;
      let breakdownHtml = "";
      data.action_proposal.breakdown.forEach(item => {
        breakdownHtml += `<div class="proposal-item"><span>${item.label}</span><span>₹${item.amount}</span></div>`;
      });

      proposalBox.innerHTML = `
        <div class="proposal-box">
          <div style="font-weight:800; font-size:14px; margin-bottom:2px;">${data.action_proposal.title}</div>
          <div style="font-size:11px; color:var(--text-muted); margin-bottom:8px;">${data.action_proposal.description}</div>
          ${breakdownHtml}
          <div class="proposal-total"><span>Total Amount</span><span>₹${data.action_proposal.total_cost}</span></div>
          <button class="btn-primary" style="margin-top:10px;" onclick="confirmAssistantAction()">Confirm & Pay (₹${data.action_proposal.total_cost})</button>
        </div>
      `;
      proposalBox.style.display = "block";
    } else {
      proposalBox.style.display = "none";
    }
  } catch (err) {
    addChatMessage("assistant", `Sorry, I encountered an error: ${err.message}`);
  }
}

async function confirmAssistantAction() {
  triggerHaptic(40);
  if (!state.currentProposal) return;
  try {
    const res = await fetch(`${API_BASE}/assistant/confirm-action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        proposal_payload: state.currentProposal.payload,
        mpin_or_biometric: "1234"
      })
    });
    const data = await res.json();
    if (res.ok) {
      document.getElementById("proposalContainer").style.display = "none";
      addChatMessage("assistant", `✅ ${data.message}`);
      await fetchWallet();
      
      // Update Tray with new status
      document.getElementById("activeTrayTitle").innerText = "Cross-Module Bundle Active";
      document.getElementById("activeTrayDesc").innerText = data.results.map(r => r.status).join(" • ");
      
      alert("Cross-module flow executed atomically! Unified Ai1 Wallet debited.");
    } else {
      alert(`Error: ${data.detail || "Transaction failed"}`);
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
}

function addChatMessage(sender, text) {
  const container = document.getElementById("chatMessages");
  const msgEl = document.createElement("div");
  msgEl.style.padding = "8px 12px";
  msgEl.style.borderRadius = "14px";
  msgEl.style.maxWidth = "82%";
  msgEl.style.fontSize = "13px";

  if (sender === "user") {
    msgEl.style.marginLeft = "auto";
    msgEl.style.background = "var(--primary)";
    msgEl.style.color = "white";
  } else {
    msgEl.style.marginRight = "auto";
    msgEl.style.background = "var(--bg-light)";
    msgEl.style.color = "var(--text-dark)";
    msgEl.style.border = "1px solid var(--border-light)";
  }
  msgEl.innerText = text;
  container.appendChild(msgEl);
  container.scrollTop = container.scrollHeight;
}

// Robust Speech Recognition for Safari on iOS and Chrome on Android
function startVoiceInput() {
  triggerHaptic(20);
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert("Speech recognition is not supported in this browser. Please type your query in the input box.");
    document.getElementById("assistantMessageInput").focus();
    return;
  }

  const mic = document.getElementById("voiceMicBtn");
  const headerMic = document.getElementById("headerMicBtn");

  try {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = state.language === "hi" ? "hi-IN" : state.language === "kn" ? "kn-IN" : state.language === "ta" ? "ta-IN" : state.language === "te" ? "te-IN" : "en-IN";

    if (mic) mic.classList.add("listening");
    if (headerMic) headerMic.classList.add("listening");

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      document.getElementById("assistantMessageInput").value = text;
      if (mic) mic.classList.remove("listening");
      if (headerMic) headerMic.classList.remove("listening");
      submitAssistantChat();
    };

    recognition.onerror = (e) => {
      console.warn("Speech recognition error:", e);
      if (mic) mic.classList.remove("listening");
      if (headerMic) headerMic.classList.remove("listening");
    };

    recognition.onend = () => {
      if (mic) mic.classList.remove("listening");
      if (headerMic) headerMic.classList.remove("listening");
    };

    recognition.start();
  } catch (err) {
    console.error("SpeechRecognition start error:", err);
    if (mic) mic.classList.remove("listening");
    if (headerMic) headerMic.classList.remove("listening");
  }
}

// ==========================================
// 10. PARTNER & ADMIN VIEWS
// ==========================================
async function loadPartnerDashboard(role) {
  triggerHaptic(15);
  const res = await fetch(`${API_BASE}/partner/dashboard?role=${role}`);
  const data = await res.json();
  const content = document.getElementById("partnerDashboardContent");

  content.innerHTML = `
    <div style="background:var(--primary-light); border:1px solid var(--primary); border-radius:var(--radius-md); padding:14px; margin-bottom:14px;">
      <div style="font-size:12px; font-weight:800; color:var(--primary);">${data.role.toUpperCase()}</div>
      <div style="font-size:18px; font-weight:800;">${data.partner_name || data.operator_name}</div>
      <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:13px;">
        <span>Today's Earnings: <b>₹${data.today_earnings || data.revenue_today_inr}</b></span>
        <span>Rating / Uptime: <b>${data.rating || data.uptime_pct}%</b></span>
      </div>
    </div>
    <h3 style="font-size:14px; font-weight:700; margin-bottom:8px;">Live Active Dispatches</h3>
    <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:12px; background:var(--card-light);">
      <p style="font-size:13px; font-weight:700;">Task: ${data.active_tasks ? data.active_tasks[0].status : "All Stations Operational"}</p>
      <button class="btn-primary" style="margin-top:8px; padding:6px 12px; font-size:12px;" onclick="alert('Task Accepted! Live GPS route activated.')">Accept Task</button>
    </div>
  `;
}

async function loadAdminDashboard() {
  triggerHaptic(15);
  const res = await fetch(`${API_BASE}/admin/metrics`);
  const metrics = await res.json();

  const auditRes = await fetch(`${API_BASE}/admin/audit-logs`);
  const logs = await auditRes.json();

  document.getElementById("adminMetricsContent").innerHTML = `
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:14px;">
      <div style="background:var(--bg-light); border:1px solid var(--border-light); border-radius:12px; padding:12px;">
        <div style="font-size:11px; color:var(--text-muted);">Gross Merchandise Value (GMV)</div>
        <div style="font-size:20px; font-weight:800; color:var(--primary);">₹${metrics.gross_merchandise_value_inr.toLocaleString("en-IN")}</div>
      </div>
      <div style="background:var(--bg-light); border:1px solid var(--border-light); border-radius:12px; padding:12px;">
        <div style="font-size:11px; color:var(--text-muted);">Total Active Users</div>
        <div style="font-size:20px; font-weight:800;">${metrics.total_active_users.toLocaleString("en-IN")}</div>
      </div>
    </div>
    <div class="proposal-box">
      <div class="proposal-item"><span>RBI PPI Compliance</span><span style="color:var(--success); font-weight:700;">100% Verified</span></div>
      <div class="proposal-item"><span>IRDAI E-Commerce Compliance</span><span style="color:var(--success); font-weight:700;">15-day Free Look Active</span></div>
      <div class="proposal-item"><span>DPDP Act 2023 Compliance</span><span style="color:var(--success); font-weight:700;">Consent Notices Enforced</span></div>
    </div>
  `;

  let logsHtml = "";
  logs.forEach(l => {
    logsHtml += `
      <div style="border-bottom:1px solid var(--border-light); padding:8px 0; font-size:11px;">
        <div style="font-weight:700;">${l.action} • <span style="color:var(--primary);">${l.module}</span></div>
        <div style="color:var(--text-muted);">${JSON.stringify(l.details)}</div>
      </div>
    `;
  });
  document.getElementById("adminAuditLogs").innerHTML = logsHtml;
}

async function exportMyData() {
  triggerHaptic(20);
  const res = await fetch(`${API_BASE}/admin/users/export-my-data`);
  const data = await res.json();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Ai1_DPDP_Data_Export_${state.user.id}.json`;
  a.click();
}

// ==========================================
// 11. WEBSOCKET VIEWPORT ENGINE
// ==========================================
function setupWebSocketViewport() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/api/v1/ev/ws/viewport`;

  try {
    const ws = new WebSocket(wsUrl);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("[WebSocket Event]", data);
    };
    ws.onopen = () => {
      ws.send(JSON.stringify({ bbox: [12.80, 77.50, 13.30, 77.85] }));
    };
  } catch (err) {
    console.log("WebSocket running in polling fallback mode.");
  }
}

// Proactive suggestions
async function fetchSuggestions() {
  const res = await fetch(`${API_BASE}/assistant/proactive-suggestions`);
  const list = await res.json();
  const el = document.getElementById("suggestionsList");
  if (!el) return;

  let html = `<div style="display:flex; flex-direction:column; gap:8px;">`;
  list.forEach(s => {
    html += `
      <div style="border:1px solid var(--border-light); border-radius:var(--radius-md); padding:10px; background:var(--card-light); display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:13px; font-weight:800;">${s.title} <span class="badge" style="background:#EBF3FF; color:#0066FF;">${s.accent_badge}</span></div>
          <div style="font-size:11px; color:var(--text-muted);">${s.subtitle}</div>
        </div>
        <button class="add-btn" onclick="selectModule('${s.action_route}')">${s.action_text}</button>
      </div>
    `;
  });
  html += `</div>`;
  el.innerHTML = html;
}

// Modal Helpers
function openModal(modalId) {
  triggerHaptic(15);
  const m = document.getElementById(modalId);
  if (m) m.classList.add("open");
}

function closeModal(modalId) {
  triggerHaptic(10);
  const m = document.getElementById(modalId);
  if (m) m.classList.remove("open");
}

function closeSheetOnClickOutside(e, modalId) {
  if (e.target.id === modalId) {
    closeModal(modalId);
  }
}

function handleSearchKey(e) {
  if (e.key === "Enter") {
    const q = e.target.value.trim();
    if (!q) return;
    openAssistantModal(false);
    sendAssistantQuery(q);
  }
}

function showPincodeModal() {
  triggerHaptic(15);
  const newPin = prompt("Enter delivery pincode (e.g. 560038 Indiranagar, 560034 Koramangala, 560102 HSR Layout):", "560038");
  if (newPin) {
    document.getElementById("currentLocationText").innerText = `Bengaluru (${newPin})`;
    selectModule("qc");
  }
}

function openWalletModal() {
  selectModule("wallet");
}

function openActiveOrderDetails() {
  triggerHaptic(20);
  if (state.activeEvSession && state.activeEvSession.status === "charging") {
    openLiveEvSessionModal();
  } else if (state.activeRide) {
    openRideModal(state.activeRide);
  } else {
    selectModule("qc");
  }
}
