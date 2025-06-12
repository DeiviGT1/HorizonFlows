// src/App.js 
import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Dashboard from "./pages/Dashboard";
import Customers from "./pages/Customers";
import Products from "./pages/Products";
import Invoices from "./pages/Invoices";
import AuthGuard from "./components/AuthGuard";
import AdminOnboarding from "./pages/AdminOnboarding";
import AdminRoute from "./components/AdminRoute";
import { CompanyProvider } from "./context/CompanyContext";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthGuard>
          {/* 👇 WRAP your components */}
          <CompanyProvider> 
            <Header />
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              {/* Note: The '/companies' route seems for admin purposes. 
                  It should fetch from the master DB, not the tenant DB. */}
              <Route path="/customers" element={<Customers />} />
              <Route path="/products" element={<Products />} />
              <Route path="/invoices" element={<Invoices />} />
              <Route
                path="/admin/onboarding"
                element={<AdminRoute element={<AdminOnboarding />} />}
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </CompanyProvider>
        </AuthGuard>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;