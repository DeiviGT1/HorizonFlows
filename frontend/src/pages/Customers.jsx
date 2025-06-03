// src/pages/Customers.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";
import TableBase from "../components/TableBase";

export default function Customers() {
  const qc = useQueryClient();

  // 1️⃣ Traer lista de clientes
  const { data, isLoading, error } = useQuery({
    queryKey: ["customers"],
    queryFn: async () => {
      const res = await api.get("/customers/");
      return res.data;
    }});

  // 2️⃣ Mutación: eliminar
  const deleteMutation = useMutation({
    mutationFn: async (id) => { // La función ahora es una propiedad 'mutationFn'
      await api.delete(`/customers/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["customers"]), // Las opciones van en el mismo objeto
  });

  // 3️⃣ Mutación: crear cliente demo
  const createMutation = useMutation({
    mutationFn: async () => { // La función ahora es una propiedad 'mutationFn'
      await api.post("/customers/", {
        company_id: 1,
        name: "Juan Pérez",
        email: "juan@example.com",
        phone: "555-0000",
      });
    },
    onSuccess: () => qc.invalidateQueries(["customers"]), // Las opciones van en el mismo objeto
  });

  if (isLoading) return <p>Cargando clientes…</p>;
  if (error) return <p>Error al cargar clientes.</p>;

  const columns = [
    { key: "id", header: "ID" },
    { key: "company_id", header: "Empresa ID" },
    { key: "name", header: "Nombre" },
    { key: "email", header: "Email" },
    { key: "phone", header: "Teléfono" },
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
        <h1 className="text-2xl font-semibold">Clientes</h1>
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