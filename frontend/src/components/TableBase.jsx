// src/components/TableBase.jsx
import React from "react";

export default function TableBase({ data, columns }) {
  return (
    <table className="min-w-full bg-white border border-gray-200">
      <thead className="bg-secondary text-white">
        <tr>
          {columns.map((col) => (
            <th key={col.key} className="p-2 border-b">
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} className="hover:bg-gray-100">
            {columns.map((col) => (
              <td key={col.key} className="p-2 border-b">
                {col.render ? col.render(row) : row[col.key]}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}