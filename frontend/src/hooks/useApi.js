// src/hooks/useApi.js
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';

export function useApi() {
  const { getAccessTokenSilently } = useAuth0();

  const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL,
  });

  api.interceptors.request.use(async (config) => {
    const token = await getAccessTokenSilently();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  return api;
}