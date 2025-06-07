// src/components/AuthGuard.jsx
import { useAuth0 } from "@auth0/auth0-react";

export default function AuthGuard({ children }) {
  const { isLoading } = useAuth0();
  if (isLoading) return null; // o spinner pantalla completa
  return children;
}