import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getProducts = async (category = null, search = null) => {
  try {
    const params = {}
    if (category) params.category = category
    if (search) params.search = search
    
    const response = await api.get('/products', { params })
    return response.data
  } catch (error) {
    console.error('Mahsulotlarni yuklashda xatolik:', error)
    throw error
  }
}

export const getCategories = async () => {
  try {
    const response = await api.get('/categories')
    return response.data
  } catch (error) {
    console.error('Kategoriyalarni yuklashda xatolik:', error)
    throw error
  }
}

export const createOrder = async (orderData) => {
  try {
    const response = await api.post('/order', orderData)
    return response.data
  } catch (error) {
    console.error('Buyurtma yuborishda xatolik:', error)
    throw error
  }
}

export default api
