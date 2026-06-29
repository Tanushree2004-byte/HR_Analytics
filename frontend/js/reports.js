function downloadReport(format) {
  window.open(API.downloadUrl(format), '_blank');
  App.showToast(`${format.toUpperCase()} report download started`, 'success');
}

async function uploadDataset(e) {
  const file = e.target.files[0];
  if (!file) return;
  App.showLoading();
  try {
    await API.upload(file);
    App.showToast('Dataset uploaded and pipeline re-run successfully', 'success');
  } catch (err) {
    App.showToast('Upload failed: ' + err.message, 'error');
  } finally {
    App.hideLoading();
    e.target.value = '';
  }
}

async function retrainModel() {
  App.showLoading();
  try {
    const result = await API.post('/retrain', {});
    App.showToast(`Model retrained: ${result.metrics?.best_model || 'Success'}`, 'success');
    loadMetrics();
  } catch (err) {
    App.showToast('Retraining failed', 'error');
  } finally {
    App.hideLoading();
  }
}

async function loadMetrics() {
  const container = document.getElementById('modelMetrics');
  if (!container) return;
  try {
    const data = await API.get('/model-metrics');
    if (!data.models) return;

    container.innerHTML = `
      <p style="margin-bottom:16px"><strong>Best Model:</strong> ${data.best_model} (ROC-AUC: ${data.best_roc_auc})</p>
      <div class="table-wrapper">
        <table>
          <thead><tr><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>ROC-AUC</th></tr></thead>
          <tbody>${data.models.map(m => `
            <tr>
              <td>${m.model}</td>
              <td>${(m.accuracy * 100).toFixed(1)}%</td>
              <td>${(m.precision * 100).toFixed(1)}%</td>
              <td>${(m.recall * 100).toFixed(1)}%</td>
              <td>${(m.f1_score * 100).toFixed(1)}%</td>
              <td>${(m.roc_auc * 100).toFixed(1)}%</td>
            </tr>
          `).join('')}</tbody>
        </table>
      </div>
    `;
  } catch { container.innerHTML = '<p>Metrics unavailable</p>'; }
}

document.addEventListener('DOMContentLoaded', () => {
  App.initApp('Reports', 'Generate and export analytics reports');
  loadMetrics();
  document.getElementById('uploadInput')?.addEventListener('change', uploadDataset);
  document.getElementById('retrainBtn')?.addEventListener('click', retrainModel);
});

window.downloadReport = downloadReport;
