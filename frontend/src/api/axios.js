// src/api/axios.js
import axios from 'axios';
import { getAccessTokenSilently } from '@auth0/auth0-react';

export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

api.interceptors.request.use(
  async (config) => {
    try {
      const token = await getAccessTokenSilently();
      config.headers.Authorization = `Bearer ${token}`;
    } catch (e) {
      console.warn('No se pudo obtener el token', e);
    }
    return config;
  },
  (error) => Promise.reject(error)
);