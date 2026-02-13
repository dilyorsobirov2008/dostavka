/**
 * Storage Helper - LocalStorage va Cache bilan ishlash
 */

const STORAGE_PREFIX = 'supermarket_';

// Savatcha ma'lumotlarini saqlash
export const saveCart = (cartItems) => {
  try {
    localStorage.setItem(`${STORAGE_PREFIX}cart`, JSON.stringify(cartItems));
    return true;
  } catch (error) {
    console.error('Savatcha saqlashda xato:', error);
    return false;
  }
};

// Savatcha ma'lumotlarini olish
export const getCart = () => {
  try {
    const cart = localStorage.getItem(`${STORAGE_PREFIX}cart`);
    return cart ? JSON.parse(cart) : [];
  } catch (error) {
    console.error('Savatcha olinishida xato:', error);
    return [];
  }
};

// Savatcha tozalash
export const clearCart = () => {
  try {
    localStorage.removeItem(`${STORAGE_PREFIX}cart`);
    return true;
  } catch (error) {
    console.error('Savatcha tozalashda xato:', error);
    return false;
  }
};

// Foydalanuvchi ma'lumotlarini saqlash
export const saveUserData = (userData) => {
  try {
    localStorage.setItem(`${STORAGE_PREFIX}user`, JSON.stringify(userData));
    return true;
  } catch (error) {
    console.error('Foydalanuvchi ma\'lumotlarini saqlashda xato:', error);
    return false;
  }
};

// Foydalanuvchi ma'lumotlarini olish
export const getUserData = () => {
  try {
    const user = localStorage.getItem(`${STORAGE_PREFIX}user`);
    return user ? JSON.parse(user) : null;
  } catch (error) {
    console.error('Foydalanuvchi ma\'lumotlarini olinishida xato:', error);
    return null;
  }
};

// Foydalanuvchi ma'lumotlarini o'chirish
export const clearUserData = () => {
  try {
    localStorage.removeItem(`${STORAGE_PREFIX}user`);
    return true;
  } catch (error) {
    console.error('Foydalanuvchi ma\'lumotlarini o\'chirishda xato:', error);
    return false;
  }
};

// Sevimli mahsulotlarni saqlash
export const saveFavorites = (favorites) => {
  try {
    localStorage.setItem(`${STORAGE_PREFIX}favorites`, JSON.stringify(favorites));
    return true;
  } catch (error) {
    console.error('Sevimli mahsulotlarni saqlashda xato:', error);
    return false;
  }
};

// Sevimli mahsulotlarni olish
export const getFavorites = () => {
  try {
    const favorites = localStorage.getItem(`${STORAGE_PREFIX}favorites`);
    return favorites ? JSON.parse(favorites) : [];
  } catch (error) {
    console.error('Sevimli mahsulotlarni olinishida xato:', error);
    return [];
  }
};

// Sevimli mahsulotlarni o'chirish
export const clearFavorites = () => {
  try {
    localStorage.removeItem(`${STORAGE_PREFIX}favorites`);
    return true;
  } catch (error) {
    console.error('Sevimli mahsulotlarni o\'chirishda xato:', error);
    return false;
  }
};

// Mahsulotni sevimliga qo'shish/o'chirish
export const toggleFavorite = (productId) => {
  const favorites = getFavorites();
  const index = favorites.indexOf(productId);
  
  if (index > -1) {
    favorites.splice(index, 1);
  } else {
    favorites.push(productId);
  }
  
  saveFavorites(favorites);
  return !favorites.includes(productId);
};

// Sevimli bo'lgan-yo bo'lmagani tekshirish
export const isFavorite = (productId) => {
  const favorites = getFavorites();
  return favorites.includes(productId);
};

// Ilova sozlamalarini saqlash
export const saveSettings = (settings) => {
  try {
    localStorage.setItem(`${STORAGE_PREFIX}settings`, JSON.stringify(settings));
    return true;
  } catch (error) {
    console.error('Sozlamalarni saqlashda xato:', error);
    return false;
  }
};

// Ilova sozlamalarini olish
export const getSettings = () => {
  try {
    const settings = localStorage.getItem(`${STORAGE_PREFIX}settings`);
    return settings ? JSON.parse(settings) : {
      darkMode: false,
      notifications: true,
      language: 'uz'
    };
  } catch (error) {
    console.error('Sozlamalarni olinishida xato:', error);
    return {};
  }
};

// SessionStorage uchun
export const setSession = (key, value) => {
  try {
    sessionStorage.setItem(`${STORAGE_PREFIX}${key}`, JSON.stringify(value));
    return true;
  } catch (error) {
    console.error('Session saqlashda xato:', error);
    return false;
  }
};

export const getSession = (key) => {
  try {
    const value = sessionStorage.getItem(`${STORAGE_PREFIX}${key}`);
    return value ? JSON.parse(value) : null;
  } catch (error) {
    console.error('Session olinishida xato:', error);
    return null;
  }
};

export const clearSession = (key) => {
  try {
    sessionStorage.removeItem(`${STORAGE_PREFIX}${key}`);
    return true;
  } catch (error) {
    console.error('Session o\'chirishda xato:', error);
    return false;
  }
};

// Barcha ma'lumotlarni o'chirish
export const clearAllStorage = () => {
  try {
    const keys = Object.keys(localStorage);
    keys.forEach(key => {
      if (key.startsWith(STORAGE_PREFIX)) {
        localStorage.removeItem(key);
      }
    });
    return true;
  } catch (error) {
    console.error('Saqlanganni o\'chirishda xato:', error);
    return false;
  }
};

export default {
  saveCart,
  getCart,
  clearCart,
  saveUserData,
  getUserData,
  clearUserData,
  saveFavorites,
  getFavorites,
  clearFavorites,
  toggleFavorite,
  isFavorite,
  saveSettings,
  getSettings,
  setSession,
  getSession,
  clearSession,
  clearAllStorage
};
