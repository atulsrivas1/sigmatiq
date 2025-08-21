import React from 'react'
import { Link } from 'react-router-dom'

export const ModelIdLink: React.FC<{ id: string }>= ({ id }) => (
  <Link to={`/models/${id}/designer`} className="model-id-link">{id}</Link>
)

