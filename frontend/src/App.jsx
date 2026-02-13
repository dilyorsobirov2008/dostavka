import { useState, useEffect } from 'react'
import './App.css'
import ProductCard from './components/ProductCard'
import CartModal from './components/CartModal'
import { getProducts, getCategories } from './utils/api'

const tg = window.Telegram?.WebApp

function App() {
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [cart, setCart] = useState([])
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Telegram WebApp ni sozlash
    if (tg) {
      tg.ready()
      tg.expand()
      tg.enableClosingConfirmation()
      
      // Telegram ranglarini sozlash
      const themeParams = tg.themeParams
      if (themeParams) {
        Object.entries(themeParams).forEach(([key, value]) => {
          document.documentElement.style.setProperty(`--tg-theme-${key.replace(/_/g, '-')}`, value)
        })
      }
    }

    // Ma'lumotlarni yuklash
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [productsData, categoriesData] = await Promise.all([
        getProducts(),
        getCategories()
      ])
      setProducts(productsData)
      setCategories(categoriesData)
    } catch (error) {
      console.error('Ma\'lumotlarni yuklashda xatolik:', error)
      tg?.showAlert('Ma\'lumotlarni yuklashda xatolik yuz berdi')
    } finally {
      setLoading(false)
    }
  }

  const filteredProducts = products.filter(product => {
    const matchesCategory = !selectedCategory || product.category === selectedCategory
    const matchesSearch = !searchQuery || product.name.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const addToCart = (product) => {
    tg?.HapticFeedback?.impactOccurred('medium')
    
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === product.id)
      
      if (existingItem) {
        return prevCart.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      }
      
      return [...prevCart, { ...product, quantity: 1 }]
    })
  }

  const updateQuantity = (productId, newQuantity) => {
    tg?.HapticFeedback?.impactOccurred('light')
    
    if (newQuantity === 0) {
      setCart(prevCart => prevCart.filter(item => item.id !== productId))
    } else {
      setCart(prevCart =>
        prevCart.map(item =>
          item.id === productId
            ? { ...item, quantity: newQuantity }
            : item
        )
      )
    }
  }

  const cartTotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0)

  return (
    <div className="app">
      {/* Header */}
      <div className="header">
        <div className="header-content">
          <div className="header-title">
            <span>🛒</span>
            <span>Supermarket</span>
          </div>
          <button 
            className="cart-button"
            onClick={() => {
              tg?.HapticFeedback?.impactOccurred('light')
              setIsCartOpen(true)
            }}
          >
            <span>Savat</span>
            {cartCount > 0 && (
              <span className="cart-badge">{cartCount}</span>
            )}
          </button>
        </div>
      </div>

      {/* Search */}
      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="🔍 Mahsulot qidirish..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Categories */}
      <div className="categories">
        <div className="categories-list">
          <div
            className={`category-card ${!selectedCategory ? 'active' : ''}`}
            onClick={() => {
              tg?.HapticFeedback?.impactOccurred('light')
              setSelectedCategory(null)
            }}
          >
            <span className="category-icon">🏪</span>
            <span>Barchasi</span>
          </div>
          {categories.map(category => (
            <div
              key={category.id}
              className={`category-card ${selectedCategory === category.id ? 'active' : ''}`}
              onClick={() => {
                tg?.HapticFeedback?.impactOccurred('light')
                setSelectedCategory(category.id)
              }}
            >
              <span className="category-icon">{category.icon}</span>
              <span>{category.name}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Products */}
      <div className="products-container">
        {loading ? (
          <div className="loading">Yuklanmoqda...</div>
        ) : filteredProducts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📦</div>
            <div className="empty-text">Mahsulotlar topilmadi</div>
          </div>
        ) : (
          <div className="products-grid">
            {filteredProducts.map(product => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={addToCart}
              />
            ))}
          </div>
        )}
      </div>

      {/* Cart Modal */}
      {isCartOpen && (
        <CartModal
          cart={cart}
          onClose={() => setIsCartOpen(false)}
          onUpdateQuantity={updateQuantity}
          total={cartTotal}
          onClearCart={() => setCart([])}
        />
      )}
    </div>
  )
}

export default App
