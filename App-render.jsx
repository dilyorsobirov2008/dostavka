import { useEffect, useState } from 'react';
import { initializeApp } from '@telegram-apps/sdk';
import Header from './components/Header';
import Category from './components/Category';
import Cart from './components/Cart';
import Checkout from './components/Checkout';
import './App.css';

// Render.com API URL
const API_URL = import.meta.env.VITE_API_URL || 'https://your-supermarket-bot.onrender.com';

export default function App() {
  const [cart, setCart] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('mevalar');
  const [showCheckout, setShowCheckout] = useState(false);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);

  // Telegram SDK Initialization
  useEffect(() => {
    try {
      const tmaSDK = initializeApp();
      setUser(tmaSDK.initDataUnsafe?.user || null);
      console.log('✅ TMA SDK initialized');
    } catch (error) {
      console.log('ℹ️ TMA SDK not available:', error.message);
    }
  }, []);

  // Mahsulotlarni yuklash
  useEffect(() => {
    const mockProducts = {
      mevalar: [
        { id: 1, name: 'Olma', price: 5000, image: 'https://via.placeholder.com/200?text=Olma', category: 'mevalar' },
        { id: 2, name: 'Apelsin', price: 6000, image: 'https://via.placeholder.com/200?text=Apelsin', category: 'mevalar' },
        { id: 3, name: 'Banan', price: 4500, image: 'https://via.placeholder.com/200?text=Banan', category: 'mevalar' },
        { id: 4, name: 'Angur', price: 8000, image: 'https://via.placeholder.com/200?text=Angur', category: 'mevalar' },
      ],
      sutMahsulotlari: [
        { id: 5, name: 'Sut (1L)', price: 12000, image: 'https://via.placeholder.com/200?text=Sut', category: 'sutMahsulotlari' },
        { id: 6, name: 'Yogurt', price: 8000, image: 'https://via.placeholder.com/200?text=Yogurt', category: 'sutMahsulotlari' },
        { id: 7, name: 'Pishloq', price: 25000, image: 'https://via.placeholder.com/200?text=Pishloq', category: 'sutMahsulotlari' },
        { id: 8, name: 'Qaymoq', price: 15000, image: 'https://via.placeholder.com/200?text=Qaymoq', category: 'sutMahsulotlari' },
      ],
      gosht: [
        { id: 9, name: 'Mobilli go\'sht (1kg)', price: 45000, image: 'https://via.placeholder.com/200?text=Gosht', category: 'gosht' },
        { id: 10, name: 'Tovuq (1kg)', price: 35000, image: 'https://via.placeholder.com/200?text=Tovuq', category: 'gosht' },
        { id: 11, name: 'Baliq (1kg)', price: 40000, image: 'https://via.placeholder.com/200?text=Baliq', category: 'gosht' },
      ],
      ichimliklar: [
        { id: 12, name: 'Suv (1.5L)', price: 3000, image: 'https://via.placeholder.com/200?text=Suv', category: 'ichimliklar' },
        { id: 13, name: 'Choy', price: 5000, image: 'https://via.placeholder.com/200?text=Choy', category: 'ichimliklar' },
        { id: 14, name: 'Kompot', price: 8000, image: 'https://via.placeholder.com/200?text=Kompot', category: 'ichimliklar' },
        { id: 15, name: 'Cola (2L)', price: 12000, image: 'https://via.placeholder.com/200?text=Cola', category: 'ichimliklar' },
      ]
    };
    setProducts(mockProducts);
    setLoading(false);
  }, []);

  // Mahsulotni savatchaga qo'shish
  const addToCart = (product) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === product.id);
      if (existingItem) {
        return prevCart.map(item =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prevCart, { ...product, quantity: 1 }];
    });
  };

  // Savatchadan o'chirish
  const removeFromCart = (productId) => {
    setCart(prevCart => prevCart.filter(item => item.id !== productId));
  };

  // Miqdorni o'zgartirish
  const updateQuantity = (productId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(productId);
    } else {
      setCart(prevCart =>
        prevCart.map(item =>
          item.id === productId ? { ...item, quantity } : item
        )
      );
    }
  };

  // Umumiy narx hisoblash
  const totalPrice = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="app">
      {showCheckout ? (
        <Checkout
          cart={cart}
          totalPrice={totalPrice}
          user={user}
          apiUrl={API_URL}
          onSuccess={() => {
            setCart([]);
            setShowCheckout(false);
          }}
          onBack={() => setShowCheckout(false)}
        />
      ) : (
        <>
          <Header cartCount={cart.length} totalPrice={totalPrice} />
          
          <div className="main-container">
            <div className="products-section">
              <Category
                selectedCategory={selectedCategory}
                onSelectCategory={setSelectedCategory}
              />
              
              <div className="products-grid">
                {loading ? (
                  <p className="loading">Mahsulotlar yuklanmoqda...</p>
                ) : (
                  products[selectedCategory]?.map(product => (
                    <ProductCard
                      key={product.id}
                      product={product}
                      onAddToCart={addToCart}
                    />
                  ))
                )}
              </div>
            </div>

            {cart.length > 0 && (
              <Cart
                items={cart}
                totalPrice={totalPrice}
                onUpdateQuantity={updateQuantity}
                onRemove={removeFromCart}
                onCheckout={() => setShowCheckout(true)}
              />
            )}
          </div>
        </>
      )}
    </div>
  );
}

// ProductCard Komponenta
function ProductCard({ product, onAddToCart }) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} className="product-image" />
      <h3 className="product-name">{product.name}</h3>
      <p className="product-price">{product.price.toLocaleString()} so'm</p>
      <button 
        className="add-btn"
        onClick={() => onAddToCart(product)}
      >
        Savatchaga qo'shish
      </button>
    </div>
  );
}
