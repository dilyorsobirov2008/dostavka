import '../styles/Category.css';

export default function Category({ selectedCategory, onSelectCategory }) {
  const categories = [
    { id: 'mevalar', label: '🍎 Mevalar', icon: '🍎' },
    { id: 'sutMahsulotlari', label: '🥛 Sut mahsulotlari', icon: '🥛' },
    { id: 'gosht', label: '🍗 Go\'sht', icon: '🍗' },
    { id: 'ichimliklar', label: '🥤 Ichimliklar', icon: '🥤' }
  ];

  return (
    <div className="category-container">
      <div className="category-list">
        {categories.map(cat => (
          <button
            key={cat.id}
            className={`category-btn ${selectedCategory === cat.id ? 'active' : ''}`}
            onClick={() => onSelectCategory(cat.id)}
          >
            <span className="category-icon">{cat.icon}</span>
            <span className="category-label">{cat.label}</span>
          </button>
        ))}
      </div>
      
      <div className="search-bar">
        <input
          type="text"
          placeholder="🔍 Mahsulotni qidirish..."
          className="search-input"
        />
      </div>
    </div>
  );
}
