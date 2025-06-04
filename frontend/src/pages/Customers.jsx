// src/pages/Customers.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";

export default function Customers() {
  const qc = useQueryClient();

  // 1️⃣ Traer lista de clientes
  const { data: customers, isLoading, error } = useQuery({
    queryKey: ["customers"],
    queryFn: async () => {
      const res = await api.get("/customers/");
      return res.data;
    },
  });

  // 2️⃣ Mutación: eliminar cliente
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      await api.delete(`/customers/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["customers"]),
  });

  // 3️⃣ Mutación: crear cliente demo
  const createMutation = useMutation({
    mutationFn: async () => {
      await api.post("/customers/", {
        company_id: 1,
        name: "Cliente Demo",
        email: "demo@example.com",
        phone: "555-1234",
      });
    },
    onSuccess: () => qc.invalidateQueries(["customers"]),
  });

  if (isLoading)
    return (
      <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
        <p className="text-white">Cargando clientes…</p>
      </div>
    );
  if (error)
    return (
      <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
        <p className="text-red-500">Error al cargar clientes.</p>
      </div>
    );

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* ───────── Header (Título + Botón) ───────── */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Clientes
          </p>
          <button
            onClick={() => createMutation.mutate()}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            <span className="truncate">+ Nuevo</span>
          </button>
        </div>

        {/* ───────── Tabla de Clientes ───────── */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-x-auto rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse min-w-full">
              {/* ─── Head ─── */}
              <thead>
                <tr className="bg-[#172536]">
                  <th className="column-240 px-4 py-3 text-left text-white w-[250px] text-sm font-medium leading-normal">
                    Nombre
                  </th>
                  <th className="column-480 px-4 py-3 text-left text-white w-[300px] text-sm font-medium leading-normal">
                    Email
                  </th>
                  <th className="column-720 px-4 py-3 text-left text-white w-[200px] text-sm font-medium leading-normal">
                    Teléfono
                  </th>
                  <th className="column-960 px-4 py-3 text-left text-white w-[160px] text-sm font-medium leading-normal">
                    Empresa ID
                  </th>
                  <th className="column-1200 px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Acciones
                  </th>
                  {/* La columna “ID” se deja al final para que se oculte primero via container query */}
                  <th className="column-120 px-4 py-3 text-left text-white w-16 text-sm font-medium leading-normal">
                    ID
                  </th>
                </tr>
              </thead>

              {/* ─── Body ─── */}
              <tbody>
                {customers.map((row) => (
                  <tr key={row.id} className="border-t border-t-[#2e4a6b]">
                    {/* Nombre */}
                    <td className="column-240 h-[60px] px-4 py-2 w-[250px] text-white text-sm font-normal leading-normal truncate">
                      {row.name}
                    </td>

                    {/* Email */}
                    <td className="column-480 h-[60px] px-4 py-2 w-[300px] text-[#8dabce] text-sm font-normal leading-normal truncate">
                      {row.email}
                    </td>

                    {/* Teléfono */}
                    <td className="column-720 h-[60px] px-4 py-2 w-[200px] text-[#8dabce] text-sm font-normal leading-normal">
                      {row.phone}
                    </td>

                    {/* Empresa ID */}
                    <td className="column-960 h-[60px] px-4 py-2 w-[160px] text-[#8dabce] text-sm font-normal leading-normal">
                      {row.company_id}
                    </td>

                    {/* Acciones: botón “Borrar” */}
                    <td className="column-1200 h-[60px] px-4 py-2 w-60 text-sm font-normal leading-normal">
                      <button
                        onClick={() => deleteMutation.mutate(row.id)}
                        className="flex w-full h-8 items-center justify-center rounded px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
                      >
                        <span className="truncate">Borrar</span>
                      </button>
                    </td>

                    {/* ID */}
                    <td className="column-120 h-[60px] px-4 py-2 w-16 text-[#8dabce] text-sm font-normal leading-normal">
                      {row.id}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* ───────── Container Queries ───────── */}
          <style>
            {`
              /* Cuando el contenedor mide menos de 120px, ocultar columna ID */
              @container (max-width: 120px) {
                .column-120 { display: none; }
              }
              /* Cuando el contenedor mide menos de 480px, ocultar “Empresa ID” */
              @container (max-width: 480px) {
                .column-960 { display: none; }
              }
              /* Cuando el contenedor mide menos de 720px, ocultar “Teléfono” */
              @container (max-width: 720px) {
                .column-720 { display: none; }
              }
              /* Cuando el contenedor mide menos de 960px, ocultar “Email” */
              @container (max-width: 960px) {
                .column-480 { display: none; }
              }
              /* Cuando el contenedor mide menos de 1200px, ocultar “Nombre” */
              @container (max-width: 1200px) {
                .column-240 { display: none; }
              }
            `}
          </style>
        </div>
      </div>
    </div>
  );
}