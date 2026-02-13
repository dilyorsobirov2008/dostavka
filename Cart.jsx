import '../styles/Cart.css';

export default function Cart({ items, totalPrice, onUpdateQuantity, onRemove, onCheckout }) {
  return (
    <div className="cart-section">
      <div className="cart-header">
        <h2>🛒 Savatcha ({items.length} dona)</h2>
      </div>

      <div className="cart-items">
        {items.map(item => (
          <div key={item.id} className="cart-item">
            <img src={item.image} alt={item.name} className="cart-item-image" />
            
            <div className="cart-item-details">
              <h4>{item.name}</h4>
              <p className="item-price">{item.price.toLocaleString()} so'm</p>
            </div>

            <div className="quantity-control">
              <button 
                className="qty-btn"
                onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
              >
                −
              </button>
              <span className="qty-value">{item.quantity}</span>
              <button 
                className="qty-btn"
                onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
              >
                +
              </button>
            </div>

            <div className="item-total">
              {(item.price * item.quantity).toLocaleString()} so'm
            </div>

            <button 
              className="remove-btn"
              onClick={() => onRemove(item.id)}
              title="O'chirish"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <div className="summary-row">
          <span>Oraliq narx:</span>
          <span>{totalPrice.toLocaleString()} so'm</span>
        </div>
        <div className="summary-row delivery">
          <span>Dostavka:</span>
          <span>25,000 so'm</span>
        </div>
        <div className="summary-row total">
          <span>Jami:</span>
          <span>{(totalPrice + 25000).toLocaleString()} so'm</span>
        </div>
      </div>

      <button className="checkout-btn" onClick={onCheckout}>
        Buyurtma berish →
      </button>
    </div>
  );
}
