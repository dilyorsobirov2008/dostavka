import { useState } from 'react'
import { createOrder } from '../utils/api'

const tg = window.Telegram?.WebApp

const CartModal = ({ cart, onClose, onUpdateQuantity, total, onClearCart }) => {
  const [isCheckout, setIsCheckout] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: ''
  })
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const formatPrice = (price) => {
    return new Intl.NumberFormat('uz-UZ').format(price)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.name || !formData.phone || !formData.address) {
      tg?.showAlert('Iltimos, barcha maydonlarni to\'ldiring')
      return
    }

    try {
      setLoading(true)
      tg?.HapticFeedback?.notificationOccurred('success')

      await createOrder({
        items: cart,
        customer: formData,
        total: total
      })

      setSuccess(true)
      
      setTimeout(() => {
        onClearCart()
        onClose()
        setSuccess(false)
        setIsCheckout(false)
      }, 2000)

    } catch (error) {
      console.error('Buyurtma yuborishda xatolik:', error)
      tg?.showAlert('Buyurtma yuborishda xatolik yuz berdi')
      tg?.HapticFeedback?.notificationOccurred('error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            {isCheckout ? '📝 Buyurtma berish' : '🛒 Savat'}
          </h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="modal-content">
          {success && (
            <div className="success-message">
              ✅ Buyurtma muvaffaqiyatli qabul qilindi!
            </div>
          )}

          {!isCheckout ? (
            <>
              {cart.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">🛒</div>
                  <div className="empty-text">Savat bo'sh</div>
                </div>
              ) : (
                <>
                  {cart.map(item => (
                    <div key={item.id} className="cart-item">
                      <div className="cart-item-image">{item.image}</div>
                      <div className="cart-item-info">
                        <div className="cart-item-name">{item.name}</div>
                        <div className="cart-item-price">
                          {formatPrice(item.price)} so'm / {item.unit}
                        </div>
                        <div className="cart-item-controls">
                          <button
                            className="quantity-button"
                            onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                          >
                            −
                          </button>
                          <span className="quantity-display">{item.quantity}</span>
                          <button
                            className="quantity-button"
                            onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                          >
                            +
                          </button>
                        </div>
                      </div>
                      <div style={{ fontWeight: 'bold', fontSize: '16px' }}>
                        {formatPrice(item.price * item.quantity)} so'm
                      </div>
                    </div>
                  ))}
                </>
              )}
            </>
          ) : (
            <form className="order-form" onSubmit={handleSubmit}>
              <div className="form-group">
                <label className="form-label">👤 Ismingiz</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="Ismingizni kiriting"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">📱 Telefon raqam</label>
                <input
                  type="tel"
                  className="form-input"
                  placeholder="+998 90 123 45 67"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">📍 Manzil</label>
                <textarea
                  className="form-input form-textarea"
                  placeholder="Yetkazib berish manzilini kiriting"
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  required
                />
              </div>
            </form>
          )}
        </div>

        {cart.length > 0 && (
          <div className="cart-total">
            <div className="total-row">
              <span className="total-label">Jami summa:</span>
              <span className="total-amount">{formatPrice(total)} so'm</span>
            </div>
            {!isCheckout ? (
              <button
                className="checkout-button"
                onClick={() => {
                  tg?.HapticFeedback?.impactOccurred('medium')
                  setIsCheckout(true)
                }}
              >
                📝 Buyurtma berish
              </button>
            ) : (
              <button
                className="checkout-button"
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? '⏳ Yuklanmoqda...' : '✅ Tasdiqlash'}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default CartModal
