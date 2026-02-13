import { useState } from 'react';
import '../styles/Checkout.css';

export default function Checkout({ cart, totalPrice, user, apiUrl, onSuccess, onBack }) {
  const [formData, setFormData] = useState({
    name: user?.first_name || '',
    phone: user?.username || '',
    address: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name || !formData.phone || !formData.address) {
      setError('❌ Iltimos, barcha maydonlarni to\'ldiring');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess(false);

    try {
      const orderData = {
        userId: user?.id,
        userName: formData.name,
        phone: formData.phone,
        address: formData.address,
        notes: formData.notes,
        items: cart,
        totalPrice: totalPrice + 25000,
        timestamp: new Date().toISOString()
      };

      console.log('📤 Sending order to:', apiUrl);
      console.log('📦 Order data:', orderData);

      // Backend'ga so'rov yuborish
      const response = await fetch(`${apiUrl}/api/orders`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setSuccess(true);
        setError('');
        setTimeout(() => {
          onSuccess();
        }, 2000);
      } else {
        setError('❌ ' + (data.error || 'Buyurtma yuborilishida xato yuz berdi'));
      }
    } catch (err) {
      console.error('Error:', err);
      setError('❌ Xato: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="checkout-container">
      <div className="checkout-header">
        <button className="back-btn" onClick={onBack}>← Ortga</button>
        <h2>Buyurtmani rasmiylashtirish</h2>
      </div>

      {success ? (
        <div className="success-message">
          <div className="success-icon">✅</div>
          <h3>Buyurtmangiz qabul qilindi!</h3>
          <p>Siz bilan tez orada bog'lanib, dostavka vaqtini keltiramiz.</p>
          <p className="thanks">Rahmat! 🙏</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="checkout-form">
          <div className="form-section">
            <h3>👤 Shaxsiy ma'lumotlar</h3>
            <input
              type="text"
              name="name"
              placeholder="Ismingiz"
              value={formData.name}
              onChange={handleChange}
              className="form-input"
              required
            />
            <input
              type="tel"
              name="phone"
              placeholder="+998 (__) ___-__-__"
              value={formData.phone}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-section">
            <h3>📍 Dostavka manzili</h3>
            <textarea
              name="address"
              placeholder="To'liq manzilni kiriting (xonadon, blok, ko'cha va h.k.)"
              value={formData.address}
              onChange={handleChange}
              className="form-input textarea"
              rows="3"
              required
            ></textarea>
          </div>

          <div className="form-section">
            <h3>📝 Qo'shimcha izoh (ixtiyoriy)</h3>
            <textarea
              name="notes"
              placeholder="Masalan: pintig'iga qo'ng'iroq qiling, eshik oldiga qo'ying"
              value={formData.notes}
              onChange={handleChange}
              className="form-input textarea"
              rows="2"
            ></textarea>
          </div>

          <div className="order-summary">
            <h3>📦 Buyurtma tafsilotlari</h3>
            {cart.map(item => (
              <div key={item.id} className="summary-item">
                <span>{item.name} × {item.quantity}</span>
                <span>{(item.price * item.quantity).toLocaleString()} so'm</span>
              </div>
            ))}
            <div className="summary-divider"></div>
            <div className="summary-item">
              <span>Oraliq narx:</span>
              <span>{totalPrice.toLocaleString()} so'm</span>
            </div>
            <div className="summary-item">
              <span>Dostavka:</span>
              <span>25,000 so'm</span>
            </div>
            <div className="summary-item total">
              <span>Jami:</span>
              <span>{(totalPrice + 25000).toLocaleString()} so'm</span>
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="submit-btn"
          >
            {loading ? '⏳ Yuborilmoqda...' : '✅ Buyurtmani tasdiqlash'}
          </button>
        </form>
      )}
    </div>
  );
}
