// src/App.js
import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import PrivateRoute from "./components/PrivateRoute";
import Dashboard  from "./pages/Dashboard";
import Companies  from "./pages/Companies";
import Customers  from "./pages/Customers";
import Products   from "./pages/Products";
import Invoices   from "./pages/Invoices";
import AuthGuard  from "./components/AuthGuard";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthGuard>
        <Header />
        <Routes>
          {/* Redirect root → dashboard */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* All these routes now live “behind” PrivateRoute */}
          <Route path="/dashboard" element={<Dashboard />} />

            <Route path="/companies" element={<Companies />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/products"  element={<Products />} />
            <Route path="/invoices"  element={<Invoices />} />  


          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        </AuthGuard>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;