// src/pages/Stock.jsx
import React from "react";
import { useApi } from '../hooks/useApi';

export default function Stock() {
  const api = useApi();
  
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Inventario</h1>
      <p>En construcción…</p>
    </div>
  );
}