// Minimal Assistant client stub to integrate inline hooks with the drawer.
export async function queryAssistant(contextPacket) {
  const res = await fetch('/assistant/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(contextPacket)
  });
  if (!res.ok) throw new Error('Assistant query failed');
  return await res.json();
}

export function buildContextFromDOM({ view, modelId, packId, riskProfile, extra = {} }) {
  return {
    route: location.hash || '#/',
    model_id: modelId || (window.currentModelId || null),
    pack_id: packId || (document.documentElement.getAttribute('data-edge') || 'zerosigma'),
    risk_profile: riskProfile || (window.currentRiskProfile || 'balanced'),
    view,
    form_values: extra.formValues || {},
    selection: extra.selection || [],
    recent_api: extra.recentApi || {},
    user_prompt: extra.userPrompt || null,
  };
}

