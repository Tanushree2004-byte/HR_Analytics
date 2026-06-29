async function predictAttrition(e) {
  e.preventDefault();
  const form = document.getElementById('predictionForm');
  const formData = new FormData(form);
  const data = {};
  formData.forEach((val, key) => {
    data[key] = isNaN(val) || val === '' ? val : Number(val);
  });

  App.showLoading();
  try {
    const result = await API.post('/predict', data);
    renderResult(result);
    App.showToast('Prediction complete', 'success');
  } catch (err) {
    App.showToast('Prediction failed. Ensure backend is running.', 'error');
  } finally {
    App.hideLoading();
  }
}

function renderResult(result) {
  const panel = document.getElementById('resultPanel');
  if (!panel) return;

  panel.style.display = 'block';
  panel.innerHTML = `
    <div class="risk-meter">
      <h3>Attrition Prediction Result</h3>
      <div class="gauge-container"><canvas id="gaugeChart"></canvas></div>
      <div class="risk-label ${result.risk_color}">${result.risk_level} Risk</div>
      <p style="margin-top:8px;color:var(--text-muted)">
        Prediction: <strong>${result.prediction}</strong> |
        Leave Probability: <strong>${result.probability}%</strong> |
        Confidence: <strong>${result.confidence}%</strong>
      </p>
    </div>
    <div class="recommendations">
      <h4 style="margin-bottom:12px">HR Recommendations</h4>
      <ul>${result.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>
    </div>
  `;

  setTimeout(() => ChartHelpers.gauge('gaugeChart', result.probability), 100);
}

document.addEventListener('DOMContentLoaded', () => {
  App.initApp('Attrition Prediction', 'Predict employee retention risk with ML');
  document.getElementById('predictionForm')?.addEventListener('submit', predictAttrition);
});
