import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth APIs
export const authAPI = {
  signup: (email: string, password: string) =>
    api.post('/auth/signup', { email, password }),
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
}

// Asset APIs
export const assetAPI = {
  search: (query: string) =>
    api.get(`/assets/search?q=${encodeURIComponent(query)}`),
  create: (asset: any) =>
    api.post('/assets', asset),
  getPrice: (assetId: number) =>
    api.get(`/assets/${assetId}/price`),
}

// Portfolio APIs
export const portfolioAPI = {
  list: () =>
    api.get('/portfolios'),
  create: (portfolio: any) =>
    api.post('/portfolios', portfolio),
  get: (id: number) =>
    api.get(`/portfolios/${id}`),
  analyze: (id: number) =>
    api.get(`/portfolios/${id}/analysis`),
  updateItemQuantity: (portfolioId: number, itemId: number, quantity: number) =>
    api.patch(`/portfolios/${portfolioId}/items/${itemId}`, { current_quantity: quantity }),
  delete: (id: number) =>
    api.delete(`/portfolios/${id}`),
}

export default api

