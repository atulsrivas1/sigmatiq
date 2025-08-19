// This page is deprecated - Build/Train/Backtest is now part of the Composer workflow
export function render() {
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <div class="page-redirect">
      <h2>Redirecting to Models...</h2>
      <p>Build, Train, and Backtest are now part of the Composer workflow within each model.</p>
      <p>Please select a model first, then access these features through the Composer.</p>
    </div>
  `;
  
  // Redirect to models page after a short delay
  setTimeout(() => {
    window.location.hash = '#/models';
  }, 2000);
  
  return wrap;
}