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
import TestPage from "./pages/TestPage";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <h1>Hola Mundo0</h1>
      <BrowserRouter>
      <h1>Hola Mundo1</h1>
        <AuthGuard>
          <h1>Hola Mundo2</h1>
          {/* 👇 WRAP your components */}
          <CompanyProvider> 
            <Header />
            <h1>Hola Mundo3</h1>
            <Routes>
              <h1>Hola Mundo4</h1>
              <Route path="/" element={<TestPage />} /> 
              <Route path="/dashboard" element={<Dashboard />} />
              <h1>Hola Mundo5</h1>
              {/* Note: The '/companies' route seems for admin purposes. 
                  It should fetch from the master DB, not the tenant DB. */}
              <Route path="/customers" element={<Customers />} />
              <Route path="/products" element={<Products />} />
              <Route path="/invoices" element={<Invoices />} />
              <Route path="/admin/onboarding" element={<AdminRoute element={<AdminOnboarding />} />}/>
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </CompanyProvider>
        </AuthGuard>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;