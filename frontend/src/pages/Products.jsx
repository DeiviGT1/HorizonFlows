// src/pages/Products.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";
import TableBase from "../components/TableBase";

export default function Products() {
  const qc = useQueryClient();

  // 1️⃣ Traer lista de productos
  const { data, isLoading, error } = useQuery({ // Un solo objeto como argumento
    queryKey: ["products"],
    queryFn: async () => {
      const res = await api.get("/products/");
      return res.data;
    }
    // Aquí puedes añadir otras opciones de query si las necesitas
  });

  // 2️⃣ Mutación: eliminar
  const deleteMutation = useMutation({ // Un solo objeto como argumento
    mutationFn: async (id) => { // La función ahora es una propiedad 'mutationFn'
      await api.delete(`/products/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["products"]), // Las opciones van en el mismo objeto
    // Aquí puedes añadir otras opciones de mutación si las necesitas
  });

  // 3️⃣ Mutación: crear producto demo
  const createMutation = useMutation({ // Un solo objeto como argumento
    mutationFn: async () => { // La función ahora es una propiedad 'mutationFn'
      await api.post("/products/", {
        company_id: 1,
        sku: "PRD-001",
        name: "Servicio Demo",
        type: "service",
        unit_price: 100.0,
        tax_rate: 0.07,
      });
    },
    onSuccess: () => qc.invalidateQueries(["products"]), // Las opciones van en el mismo objeto
    // Aquí puedes añadir otras opciones de mutación si las necesitas
  });

  if (isLoading) return <p>Cargando productos…</p>;
  if (error) return <p>Error al cargar productos.</p>;

  const columns = [
    { key: "id", header: "ID" },
    { key: "company_id", header: "Empresa ID" },
    { key: "sku", header: "SKU" },
    { key: "name", header: "Nombre" },
    { key: "type", header: "Tipo" },
    { key: "unit_price", header: "Precio Unitario" },
    { key: "tax_rate", header: "Impuesto" },
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
        <h1 className="text-2xl font-semibold">Productos</h1>
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

