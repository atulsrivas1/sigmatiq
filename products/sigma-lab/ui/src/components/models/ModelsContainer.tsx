import React from 'react'
import { ModelCard, type ModelCardModel } from './ModelCard'

export const ModelsContainer: React.FC<{ view: 'card'|'row'; models: ModelCardModel[] }>= ({ view, models }) => {
  return (
    <div id="cardsContainer" className={`cards-container ${view}-view`}>
      {models.map(m => (
        <ModelCard key={m.id} model={m} view={view} />
      ))}
    </div>
  )
}

