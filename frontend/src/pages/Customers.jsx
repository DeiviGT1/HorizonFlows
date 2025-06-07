// src/pages/Customers.jsx
import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useApi } from "../hooks/useApi";
import { useSortableData } from "../hooks/useSortableData";

export default function Customers() {
  const qc = useQueryClient();
  const api = useApi();

  // 📦 datos crudos
  const { data: customers = [], isLoading } = useQuery({
    queryKey: ["customers"],
    queryFn: async () => (await api.get("/customers/")).data,
  });

  // 🛠 hook de orden
  const { items: sortedCustomers, requestSort, sortConfig } =
    useSortableData(customers);

  const getClassNamesFor = (name) =>
    sortConfig?.key === name ? (sortConfig.direction === "ascending" ? "▲" : "▼") : "";

  // operaciones mutación...
  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/customers/${id}`),
    onSuccess: () => qc.invalidateQueries(["customers"]),
  });
  const createMutation = useMutation({
    mutationFn: () =>
      api.post("/customers/", {
        company_id: 1,
        name: "Cliente Demo",
        email: "demo@example.com",
        phone: "555-1234",
      }),
    onSuccess: () => qc.invalidateQueries(["customers"]),
  });

  return (
    <div className="px-40 flex flex-1 justify-center py-5 bg-[#0f1524] min-h-screen">
      <div className="layout-content-container flex flex-col max-w-[960px] w-full">
        {/* Header */}
        <div className="flex flex-wrap justify-between items-center gap-3 p-4">
          <p className="text-white tracking-light text-[32px] font-bold leading-tight min-w-72">
            Clientes
          </p>
          <button
            onClick={() => createMutation.mutate()}
            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center rounded h-8 px-4 bg-[#20344b] text-white text-sm font-medium leading-normal hover:bg-[#2a4262]"
          >
            + Nuevo
          </button>
        </div>

        {/* Tabla */}
        <div className="px-4 py-3" style={{ containerType: "inline-size" }}>
          <div className="flex overflow-x-auto rounded border border-[#2e4a6b] bg-[#0f1924]">
            <table className="flex-1 border-collapse min-w-full">
              <thead>
                <tr className="bg-[#172536]">
                  {/** Cada th dispara requestSort y muestra flecha */}
                  <th
                    onClick={() => requestSort("name")}
                    className="column-240 px-4 py-3 text-left text-white w-[250px] text-sm font-medium leading-normal cursor-pointer"
                  >
                    Nombre {getClassNamesFor("name")}
                  </th>
                  <th
                    onClick={() => requestSort("email")}
                    className="column-480 px-4 py-3 text-left text-white w-[300px] text-sm font-medium leading-normal cursor-pointer"
                  >
                    Email {getClassNamesFor("email")}
                  </th>
                  <th
                    onClick={() => requestSort("phone")}
                    className="column-720 px-4 py-3 text-left text-white w-[200px] text-sm font-medium leading-normal cursor-pointer"
                  >
                    Teléfono {getClassNamesFor("phone")}
                  </th>
                  <th
                    onClick={() => requestSort("company_id")}
                    className="column-960 px-4 py-3 text-left text-white w-[160px] text-sm font-medium leading-normal cursor-pointer"
                  >
                    Empresa ID {getClassNamesFor("company_id")}
                  </th>
                  <th className="column-1200 px-4 py-3 text-left text-[#8dabce] w-60 text-sm font-medium leading-normal">
                    Acción
                  </th>
                  <th
                    onClick={() => requestSort("id")}
                    className="column-120 px-4 py-3 text-left text-white w-16 text-sm font-medium leading-normal cursor-pointer"
                  >
                    ID {getClassNamesFor("id")}
                  </th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-6 text-center text-white">
                      Cargando…
                    </td>
                  </tr>
                ) : sortedCustomers.length > 0 ? (
                  sortedCustomers.map((row) => (
                    <tr key={row.id} className="border-t border-t-[#2e4a6b]">
                      <td className="column-240 h-[60px] px-4 py-2 text-white text-sm truncate">
                        {row.name}
                      </td>
                      <td className="column-480 h-[60px] px-4 py-2 text-[#8dabce] text-sm truncate">
                        {row.email}
                      </td>
                      <td className="column-720 h-[60px] px-4 py-2 text-[#8dabce] text-sm">
                        {row.phone}
                      </td>
                      <td className="column-960 h-[60px] px-4 py-2 text-[#8dabce] text-sm">
                        {row.company_id}
                      </td>
                      <td className="column-1200 h-[60px] px-4 py-2 text-sm">
                        <button
                          onClick={() => deleteMutation.mutate(row.id)}
                          className="w-full h-8 flex items-center justify-center rounded bg-[#20344b] text-white text-sm hover:bg-[#2a4262]"
                        >
                          Borrar
                        </button>
                      </td>
                      <td className="column-120 h-[60px] px-4 py-2 text-[#8dabce] text-sm">
                        {row.id}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td
                      colSpan={6}
                      className="px-4 py-6 text-center text-[#8dabce]"
                    >
                      No se encontraron clientes
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          {/* container-queries igual que antes */}
          <style>{`
            @container (max-width: 120px) { .column-120 { display: none; } }
            @container (max-width: 480px) { .column-960 { display: none; } }
            @container (max-width: 720px) { .column-720 { display: none; } }
            @container (max-width: 960px) { .column-480 { display: none; } }
            @container (max-width: 1200px) { .column-240 { display: none; } }
          `}</style>
        </div>
      </div>
    </div>
  );
}