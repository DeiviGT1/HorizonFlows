// src/pages/Companies.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/axios";

export default function Companies() {
  const qc = useQueryClient();

  // 1️⃣ Traer lista de compañías
  const { data: companies, isLoading, error } = useQuery({
    queryKey: ["companies"],
    queryFn: async () => {
      const res = await api.get("/companies/");
      return res.data;
    },
  });

  // 2️⃣ Mutación: eliminar compañía
  const deleteMutation = useMutation({
    mutationFn: async (id) => {
      await api.delete(`/companies/${id}`);
    },
    onSuccess: () => qc.invalidateQueries(["companies"]),
  });

  // 3️⃣ Mutación: crear compañía demo
  const createMutation = useMutation({
    mutationFn: async () => {
      await api.post("/companies/", {
        name: "Demo Corp",
        industry: "Technology",
      });
    },
    onSuccess: () => qc.invalidateQueries(["companies"]),
  });

  if (isLoading)
    return (
      <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
        <p className="text-white">Cargando compañías…</p>
      </div>
    );
  if (error)
    return (
      <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
        <p className="text-red-500">Error al cargar compañías.</p>
      </div>
    );

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* ───────── Header (Título + Botón) ───────── */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Compañías
          </p>
          <button
            onClick={() => createMutation.mutate()}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            <span className="truncate">+ Nuevo</span>
          </button>
        </div>

        {/* ───────── Tabla de Compañías ───────── */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-hidden rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse">
              {/* ─── Head ─── */}
              <thead>
                <tr className="bg-[#172536]">
                  <th className="column-240 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Nombre
                  </th>
                  <th className="column-480 px-4 py-3 text-left text-white w-[400px] text-sm font-medium leading-normal">
                    Industria
                  </th>
                  <th className="column-720 px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Acción
                  </th>
                  {/* La columna “ID” se pone última en el JSX para que al reducir pantallas 
                      primero “ID” se oculte (por container query), pero aparezca al ampliar. */}
                  <th className="column-120 px-4 py-3 text-left text-white w-24 text-sm font-medium leading-normal">
                    ID
                  </th>
                </tr>
              </thead>

              {/* ─── Body ─── */}
              <tbody>
                {companies.map((row) => (
                  <tr key={row.id} className="border-t border-t-[#2e4a6b]">
                    {/* Nombre */}
                    <td className="column-240 h-[72px] px-4 py-2 w-[400px] text-white text-sm font-normal leading-normal">
                      {row.name}
                    </td>

                    {/* Industria */}
                    <td className="column-480 h-[72px] px-4 py-2 w-[400px] text-[#8dabce] text-sm font-normal leading-normal">
                      {row.industry}
                    </td>

                    {/* Acción: botón “Borrar” */}
                    <td className="column-720 h-[72px] px-4 py-2 w-60 text-sm font-normal leading-normal">
                      <button
                        onClick={() => deleteMutation.mutate(row.id)}
                        className="flex w-full h-8 items-center justify-center rounded px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
                      >
                        <span className="truncate">Borrar</span>
                      </button>
                    </td>

                    {/* ID */}
                    <td className="column-120 h-[72px] px-4 py-2 w-24 text-[#8dabce] text-sm font-normal leading-normal">
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
              @container (max-width: 240px) {
                .column-240 { display: none; }   /* Oculta “Nombre” en contenedores muy estrechos */
              }
              @container (max-width: 480px) {
                .column-480 { display: none; }   /* Oculta “Industria” en anchos intermedios */
              }
              @container (max-width: 720px) {
                .column-720 { display: none; }   /* Oculta “Acción” si el contenedor está por debajo de 720px */
              }
              @container (max-width: 960px) {
                .column-120 { display: none; }   /* Oculta “ID” en contenedor < 960px */
              }
            `}
          </style>
        </div>
      </div>
    </div>
  );
}