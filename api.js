/**
 * API Helper - Backend'ga so'rov yuborish
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';

// Order yaratish
export const createOrder = async (orderData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderData)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Buyurtma yuborilishida xato:', error);
    throw error;
  }
};

// Mahsulotlarni olish
export const getProducts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/products`);
    
    if (!response.ok) {
      throw new Error('Mahsulotlarni yuklab olishda xato');
    }

    return await response.json();
  } catch (error) {
    console.error('Mahsulotlar yuklanishida xato:', error);
    throw error;
  }
};

// Kategoriyalarni olish
export const getCategories = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/categories`);
    
    if (!response.ok) {
      throw new Error('Kategoriyalarni yuklab olishda xato');
    }

    return await response.json();
  } catch (error) {
    console.error('Kategoriyalar yuklanishida xato:', error);
    throw error;
  }
};

// Foydalanuvchining oldingi buyurtmalarini olish
export const getUserOrders = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}/orders`);
    
    if (!response.ok) {
      throw new Error('Buyurtmalarni yuklab olishda xato');
    }

    return await response.json();
  } catch (error) {
    console.error('Buyurtmalar yuklanishida xato:', error);
    throw error;
  }
};

// Mahsulot qidirish
export const searchProducts = async (query) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/products/search?q=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      throw new Error('Qidirishda xato');
    }

    return await response.json();
  } catch (error) {
    console.error('Qidirish xatosi:', error);
    throw error;
  }
};

// To'lov ma'lumotlarini yuborish
export const processPayment = async (paymentData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/payments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(paymentData)
    });

    if (!response.ok) {
      throw new Error('To\'lovni qayta ishlashda xato');
    }

    return await response.json();
  } catch (error) {
    console.error('To\'lov xatosi:', error);
    throw error;
  }
};

// Foydalanuvchi profilini yangilash
export const updateUserProfile = async (userId, profileData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/users/${userId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(profileData)
    });

    if (!response.ok) {
      throw new Error('Profilni yangilashda xato');
    }

    return await response.json();
  } catch (error) {
    console.error('Profil yangilash xatosi:', error);
    throw error;
  }
};

// Error handling wrapper
export const apiCall = async (endpoint, options = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'API xatosi yuz berdi');
    }

    return await response.json();
  } catch (error) {
    console.error('API xatosi:', error);
    throw error;
  }
};

export default {
  createOrder,
  getProducts,
  getCategories,
  getUserOrders,
  searchProducts,
  processPayment,
  updateUserProfile,
  apiCall
};
