import React from 'react'

export const JobsTable: React.FC<{ headers: string[]; children: React.ReactNode }>= ({ headers, children }) => {
  return (
    <table className="table jobs-table">
      <thead>
        <tr>
          {headers.map((h, i) => (
            <th key={i}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>{children}</tbody>
    </table>
  )
}

