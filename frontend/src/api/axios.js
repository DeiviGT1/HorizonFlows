// src/api/axios.js
import axios from "axios";

// Si no está definida, usamos localhost:8000
const baseURL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});