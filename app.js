// ==================== CONFIG ====================
const API_URL = 'http://localhost:8000'; // Change to production URL
const DELIVERY_FEE = 25000;

// ==================== GLOBAL STATE ====================
let state = {
    cart: [],
    products: {},
    currentCategory: 'mevalar',
    searchQuery: '',
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 App initializing...');
    
    // Load products
    await loadProducts();
    
    // Setup event listeners
    setupEventListeners();
    
    // Render initial content
    renderCategories();
    renderProducts();
    
    // Load cart from storage
    loadCartFromStorage();
    updateCartDisplay();
    
    console.log('✅ App initialized');
});

// ==================== PRODUCT LOADING ====================
async function loadProducts() {
    try {
        const response = await fetch(`${API_URL}/api/products`);
        const data = await response.json();
        state.products = data.products;
        console.log('✅ Products loaded:', state.products);
    } catch (error) {
        console.error('❌ Error loading products:', error);
        state.products = getDefaultProducts();
    }
}

function getDefaultProducts() {
    return {
        mevalar: [
            { id: 1, name: 'Olma', price: 5000, image: 'https://via.placeholder.com/150?text=Olma', description: 'Qizil, sog\'lom olma' },
            { id: 2, name: 'Apelsin', price: 6000, image: 'https://via.placeholder.com/150?text=Apelsin', description: 'Shirin apelsin' },
            { id: 3, name: 'Banan', price: 4500, image: 'https://via.placeholder.com/150?text=Banan', description: 'Ranga oqargan banan' },
            { id: 4, name: 'Angur', price: 8000, image: 'https://via.placeholder.com/150?text=Angur', description: 'Siyoh, shirin angur' }
        ],
        sutMahsulotlari: [
            { id: 5, name: 'Sut (1L)', price: 12000, image: 'https://via.placeholder.com/150?text=Sut', description: '100% natural sut' },
            { id: 6, name: 'Yogurt', price: 8000, image: 'https://via.placeholder.com/150?text=Yogurt', description: 'Sog\'lom yogurt' },
            { id: 7, name: 'Pishloq', price: 25000, image: 'https://via.placeholder.com/150?text=Pishloq', description: 'Eski pishloq' }
        ],
        gosht: [
            { id: 9, name: 'Go\'sht (1kg)', price: 45000, image: 'https://via.placeholder.com/150?text=Gosht', description: 'Yangi mobilli et' },
            { id: 10, name: 'Tovuq (1kg)', price: 35000, image: 'https://via.placeholder.com/150?text=Tovuq', description: 'Toza tovuq go\'sti' }
        ],
        ichimliklar: [
            { id: 12, name: 'Suv (1.5L)', price: 3000, image: 'https://via.placeholder.com/150?text=Suv', description: 'Toza ichimlik suvi' },
            { id: 13, name: 'Choy', price: 5000, image: 'https://via.placeholder.com/150?text=Choy', description: 'Qora choy' },
            { id: 14, name: 'Cola (2L)', price: 12000, image: 'https://via.placeholder.com/150?text=Cola', description: 'Sovun cola' }
        ]
    };
}

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Cart icon click
    const cartIcon = document.getElementById('cartIcon');
    if (cartIcon) {
        cartIcon.addEventListener('click', openCheckout);
    }

    // Search input
    document.getElementById('searchInput').addEventListener('input', (e) => {
        state.searchQuery = e.target.value.toLowerCase();
        renderProducts();
    });

    // Checkout button
    document.getElementById('checkoutBtn').addEventListener('click', openCheckout);

    // Close modal
    document.getElementById('closeModal').addEventListener('click', closeCheckout);
    document.getElementById('checkoutModal').addEventListener('click', (e) => {
        if (e.target.id === 'checkoutModal') closeCheckout();
    });

    // Form submission
    document.getElementById('checkoutForm').addEventListener('submit', submitOrder);

    // Clear cart button
    const clearBtn = document.getElementById('clearCartBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearCart);
    }
}

// ==================== CATEGORY RENDERING ====================
function renderCategories() {
    const categories = [
        { id: 'mevalar', name: '🍎 Mevalar' },
        { id: 'sutMahsulotlari', name: '🥛 Sut mahsulotlari' },
        { id: 'gosht', name: '🍗 Go\'sht' },
        { id: 'ichimliklar', name: '🥤 Ichimliklar' }
    ];

    const categoryList = document.getElementById('categoryList');
    categoryList.innerHTML = categories.map(cat => `
        <button class="category-btn ${cat.id === state.currentCategory ? 'active' : ''}" 
                onclick="selectCategory('${cat.id}')">
            ${cat.name}
        </button>
    `).join('');
}

function selectCategory(categoryId) {
    state.currentCategory = categoryId;
    state.searchQuery = '';
    document.getElementById('searchInput').value = '';
    renderCategories();
    renderProducts();
}

// ==================== PRODUCT RENDERING ====================
function renderProducts() {
    const categoryProducts = state.products[state.currentCategory] || [];
    
    // Filter by search
    const filtered = state.searchQuery 
        ? categoryProducts.filter(p => p.name.toLowerCase().includes(state.searchQuery))
        : categoryProducts;

    const productsGrid = document.getElementById('productsGrid');

    if (filtered.length === 0) {
        productsGrid.innerHTML = '<div class="empty-cart-message" style="grid-column: 1/-1;">Mahsulot topilmadi</div>';
        return;
    }

    productsGrid.innerHTML = filtered.map(product => `
        <div class="product-card">
            <img src="${product.image}" alt="${product.name}" class="product-image">
            <h3 class="product-name">${product.name}</h3>
            ${product.description ? `<p class="product-description">${product.description}</p>` : ''}
            <p class="product-price">${product.price.toLocaleString()} so'm</p>
            <button class="add-to-cart-btn" onclick="addToCart(${product.id}, '${product.name}', ${product.price}, '${product.image}')">
                🛒 Qo'shish
            </button>
        </div>
    `).join('');
}

// ==================== CART MANAGEMENT ====================
function addToCart(id, name, price, image) {
    const existingItem = state.cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity++;
    } else {
        state.cart.push({ id, name, price, image, quantity: 1 });
    }
    
    saveCartToStorage();
    updateCartDisplay();
    
    // Show feedback
    showNotification(`✅ ${name} savatchaga qo'shildi!`);
}

function removeFromCart(id) {
    state.cart = state.cart.filter(item => item.id !== id);
    saveCartToStorage();
    updateCartDisplay();
}

function updateQuantity(id, quantity) {
    if (quantity <= 0) {
        removeFromCart(id);
    } else {
        const item = state.cart.find(item => item.id === id);
        if (item) item.quantity = quantity;
        saveCartToStorage();
        updateCartDisplay();
    }
}

function clearCart() {
    if (confirm('Savatcha tozalashga ishonchingiz komilmi?')) {
        state.cart = [];
        saveCartToStorage();
        updateCartDisplay();
        closeCheckout();
    }
}

// ==================== CART DISPLAY ====================
function updateCartDisplay() {
    const cartSection = document.getElementById('cartSection');
    const cartIcon = document.getElementById('cartIcon');
    const cartCount = document.getElementById('cartCount');
    const cartItemCount = document.getElementById('cartItemCount');
    const cartItems = document.getElementById('cartItems');
    const subtotal = document.getElementById('subtotal');
    const cartTotal = document.getElementById('cartTotal');
    const totalPrice = document.getElementById('totalPrice');
    const clearBtn = document.getElementById('clearCartBtn');

    if (state.cart.length === 0) {
        cartSection.style.display = 'none';
        cartIcon.style.display = 'none';
        totalPrice.textContent = '0 so\'m';
        return;
    }

    // Show cart
    cartSection.style.display = 'block';
    cartIcon.style.display = 'block';
    if (clearBtn) clearBtn.style.display = 'block';

    // Update counts
    cartCount.textContent = state.cart.length;
    cartItemCount.textContent = state.cart.length;

    // Calculate totals
    const subtotalAmount = state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const totalAmount = subtotalAmount + DELIVERY_FEE;

    subtotal.textContent = subtotalAmount.toLocaleString() + ' so\'m';
    cartTotal.textContent = totalAmount.toLocaleString() + ' so\'m';
    totalPrice.textContent = totalAmount.toLocaleString() + ' so\'m';

    // Render cart items
    cartItems.innerHTML = state.cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}" class="cart-item-image">
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${item.price.toLocaleString()} so'm</div>
                <div class="quantity-control">
                    <button class="qty-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">−</button>
                    <span class="qty-value">${item.quantity}</span>
                    <button class="qty-btn" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                </div>
            </div>
            <div class="cart-item-total">${(item.price * item.quantity).toLocaleString()} so'm</div>
            <button class="remove-item-btn" onclick="removeFromCart(${item.id})" title="O'chirish">✕</button>
        </div>
    `).join('');
}

// ==================== CHECKOUT ====================
function openCheckout() {
    if (state.cart.length === 0) {
        showNotification('❌ Savatcha bo\'sh!');
        return;
    }

    // Build order summary
    const subtotal = state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const total = subtotal + DELIVERY_FEE;

    let summary = '';
    state.cart.forEach(item => {
        summary += `
            <div class="summary-item">
                <span class="summary-item-name">${item.name} × ${item.quantity}</span>
                <span class="summary-item-price">${(item.price * item.quantity).toLocaleString()} so'm</span>
            </div>
        `;
    });
    summary += `
        <div class="summary-item">
            <span class="summary-item-name">Dostavka:</span>
            <span class="summary-item-price">25,000 so'm</span>
        </div>
        <div class="summary-item summary-total">
            <span>Jami:</span>
            <span>${total.toLocaleString()} so'm</span>
        </div>
    `;

    document.getElementById('orderSummary').innerHTML = summary;
    
    // Reset form
    document.getElementById('checkoutForm').reset();
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('checkoutForm').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';

    // Show modal
    document.getElementById('checkoutModal').classList.add('active');
}

function closeCheckout() {
    document.getElementById('checkoutModal').classList.remove('active');
}

async function submitOrder(e) {
    e.preventDefault();

    const userName = document.getElementById('userName').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const address = document.getElementById('address').value.trim();
    const notes = document.getElementById('notes').value.trim();
    const errorDiv = document.getElementById('errorMessage');

    // Validation
    if (!userName || !phone || !address) {
        errorDiv.textContent = '❌ Iltimos, barcha majburiy maydonlarni to\'ldiring';
        errorDiv.style.display = 'block';
        return;
    }

    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Yuborilmoqda...';

    try {
        const subtotal = state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
        const orderData = {
            userName,
            phone,
            address,
            notes,
            items: state.cart,
            totalPrice: subtotal,
            timestamp: new Date().toISOString()
        };

        console.log('📤 Sending order:', orderData);

        const response = await fetch(`${API_URL}/api/orders`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });

        const data = await response.json();

        if (data.success) {
            // Show success message
            document.getElementById('checkoutForm').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';

            // Clear cart
            setTimeout(() => {
                state.cart = [];
                saveCartToStorage();
                updateCartDisplay();
                closeCheckout();
                
                // Reset form display
                document.getElementById('checkoutForm').style.display = 'block';
                document.getElementById('successMessage').style.display = 'none';
            }, 3000);
        } else {
            errorDiv.textContent = `❌ ${data.error || 'Buyurtma yuborilishida xato yuz berdi'}`;
            errorDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('❌ Order error:', error);
        errorDiv.textContent = `❌ Xato: ${error.message}`;
        errorDiv.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '✅ Buyurtmani tasdiqlash';
    }
}

// ==================== STORAGE ====================
function saveCartToStorage() {
    localStorage.setItem('supermarket_cart', JSON.stringify(state.cart));
}

function loadCartFromStorage() {
    const saved = localStorage.getItem('supermarket_cart');
    if (saved) {
        try {
            state.cart = JSON.parse(saved);
        } catch (error) {
            console.error('Error loading cart from storage:', error);
            state.cart = [];
        }
    }
}

// ==================== UTILITIES ====================
function showNotification(message) {
    // Simple notification
    console.log('📢', message);
    
    // Could add toast notification here
    // For now, just log to console
}

console.log('✅ app.js loaded and ready!');
