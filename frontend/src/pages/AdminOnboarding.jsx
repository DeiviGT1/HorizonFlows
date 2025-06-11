// frontend/src/pages/AdminOnboarding.jsx
import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useApi } from "../hooks/useApi";

export default function AdminOnboarding() {
  const api = useApi();
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");

  const createCompanyMutation = useMutation({
    mutationFn: (newCompany) => api.post("/onboarding/register", newCompany),
    onSuccess: (data) => {
      alert(`¡Empresa "${data.data.name}" creada con éxito!`);
      setName("");
      setSlug("");
    },
    onError: (error) => {
      const errorMsg = error.response?.data?.detail || "Ocurrió un error desconocido.";
      alert(`Error al crear la empresa: ${errorMsg}`);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !slug) {
      alert("Por favor, completa ambos campos.");
      return;
    }
    createCompanyMutation.mutate({ name, slug });
  };

  const handleNameChange = (e) => {
    const value = e.target.value;
    setName(value);
    // Sugerencia de slug automática
    const suggestedSlug = value
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
    setSlug(suggestedSlug);
  };

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[600px] w-full">
        <div className="p-4">
          <p className="text-white text-[32px] font-bold">Admin: Crear Nueva Empresa</p>
          <p className="text-[#8dabce] text-sm mt-2">
            Esta sección es para crear un nuevo tenant en el sistema, incluyendo su base de datos dedicada.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-4 flex flex-col gap-4">
          <div>
            <label htmlFor="companyName" className="block text-white mb-2">Nombre de la Empresa</label>
            <input
              id="companyName"
              type="text"
              value={name}
              onChange={handleNameChange}
              className="w-full p-2 rounded bg-[#172536] text-white border border-[#2e4a6b] focus:outline-none focus:ring-2 focus:ring-accent"
              placeholder="Ej: SOS Llaves"
            />
          </div>
          <div>
            <label htmlFor="companySlug" className="block text-white mb-2">Slug (para subdominio)</label>
            <input
              id="companySlug"
              type="text"
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              className="w-full p-2 rounded bg-[#172536] text-white border border-[#2e4a6b] focus:outline-none focus:ring-2 focus:ring-accent"
              placeholder="Ej: sosllaves"
            />
             <p className="text-[#8dabce] text-xs mt-1">
              Solo letras minúsculas, números y guiones. Será usado como `slug.dominio.com`.
            </p>
          </div>
          <button
            type="submit"
            disabled={createCompanyMutation.isPending}
            className="mt-4 h-10 px-6 bg-accent text-white font-bold rounded hover:bg-opacity-80 disabled:bg-muted disabled:cursor-not-allowed"
          >
            {createCompanyMutation.isPending ? "Creando..." : "Crear Empresa y Base de Datos"}
          </button>
        </form>
      </div>
    </div>
  );
}