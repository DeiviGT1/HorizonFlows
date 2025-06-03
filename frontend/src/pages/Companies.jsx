// src/pages/Companies.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";
import TableBase from "../components/TableBase";

export default function Companies() {
  const qc = useQueryClient();

  // 1️⃣ Traer lista de compañías
  const { data, isLoading, error } = useQuery({ // Un solo objeto como argumento
    queryKey: ["companies"],
    queryFn: async () => {
      const res = await api.get("/companies/");
      return res.data;
    }
    // Aquí puedes añadir otras opciones de query si las necesitas
  });

  // 2️⃣ Mutación: eliminar
  const deleteMutation = useMutation({ // Un solo objeto como argumento
    mutationFn: async (id) => {
      await api.delete(`/companies/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["companies"]),
    // Aquí puedes añadir otras opciones de mutación si las necesitas
  });

  // 3️⃣ Mutación: crear compañía demo
  const createMutation = useMutation({ // Un solo objeto como argumento
    mutationFn: async () => {
      await api.post("/companies/", {
        name: "Demo Corp",
        industry: "Technology",
      });
    },
    onSuccess: () => qc.invalidateQueries(["companies"]),
    // Aquí puedes añadir otras opciones de mutación si las necesitas
  });

  if (isLoading) return <p>Cargando compañías…</p>;
  if (error) return <p>Error al cargar compañías.</p>;

  const columns = [
    { key: "id", header: "ID" },
    { key: "name", header: "Nombre" },
    { key: "industry", header: "Industria" },
    {
      key: "id",
      header: "Acciones",
      render: (row) => (
        <button
          onClick={() => deleteMutation.mutate(row.id)}
          className="text-red-600 hover:underline"
        >
          Borrar
        </button>
      ),
    },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Compañías</h1>
        <button
          onClick={() => createMutation.mutate()}
          className="bg-primary text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          + Nuevo
        </button>
      </div>

      <TableBase data={data || []} columns={columns} />
    </div>
  );
}