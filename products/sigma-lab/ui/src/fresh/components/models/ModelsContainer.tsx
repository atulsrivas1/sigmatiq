import React from 'react'
import { FreshModel, FreshModelCard } from './ModelCard'

export const FreshModelsContainer: React.FC<{ view: 'card'|'row'; models: FreshModel[] }>= ({ view, models }) => {
  return (
    <div id="cardsContainer" className={`cards-container ${view}-view`}>
      {models.map(m => (
        <FreshModelCard key={m.id} model={m} view={view} />
      ))}
    </div>
  )
}

