const ProductCard = ({ product, onAddToCart }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('uz-UZ').format(price)
  }

  return (
    <div className="product-card">
      <div className="product-image">{product.image}</div>
      <div className="product-info">
        <div className="product-name">{product.name}</div>
        <div className="product-unit">1 {product.unit}</div>
        <div className="product-footer">
          <div className="product-price">{formatPrice(product.price)} so'm</div>
          <button
            className="add-button"
            onClick={() => onAddToCart(product)}
          >
            +
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProductCard
