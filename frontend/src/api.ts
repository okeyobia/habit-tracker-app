import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
});

// Auth
export const register = (data: { email: string; password: string }) =>
  api.post('/auth/register', data);
export const login = (data: { username: string; password: string }) =>
  api.post('/auth/login', data);
export const getMe = (token: string) =>
  api.get('/users/me', { headers: { Authorization: `Bearer ${token}` } });

// Habits
export const getHabits = (token: string) =>
  api.get('/habits/', { headers: { Authorization: `Bearer ${token}` } });
export const createHabit = (token: string, data: { name: string; description?: string }) =>
  api.post('/habits/', data, { headers: { Authorization: `Bearer ${token}` } });
export const updateHabit = (token: string, habitId: number, data: { name: string; description?: string }) =>
  api.put(`/habits/${habitId}`, data, { headers: { Authorization: `Bearer ${token}` } });
export const deleteHabit = (token: string, habitId: number) =>
  api.delete(`/habits/${habitId}`, { headers: { Authorization: `Bearer ${token}` } });
export const trackHabit = (token: string, habitId: number, data: { date: string }) =>
  api.post(`/habits/${habitId}/track`, data, { headers: { Authorization: `Bearer ${token}` } });
