async function initAnalytics() {
  App.showLoading();
  try {
    const [dash, insights] = await Promise.all([API.get('/dashboard'), API.get('/insights')]);
    renderAnalyticsCharts(dash.charts);
    renderAllInsights(insights.insights || []);
    renderModelComparison();
  } catch (err) {
    App.showToast('Failed to load analytics', 'error');
  } finally {
    App.hideLoading();
  }
}

function renderAnalyticsCharts(charts) {
  if (!charts) return;
  ChartHelpers.doughnut('aGender', Object.keys(charts.gender || {}), Object.values(charts.gender || {}));
  ChartHelpers.bar('aDept', Object.keys(charts.department || {}), [{
    label: 'Employees', data: Object.values(charts.department || {}), backgroundColor: '#D4AF37', borderRadius: 8,
  }]);
  ChartHelpers.groupedBar('aDeptAttr', Object.keys(charts.departmentAttrition || {}), [
    { label: 'Attrition %', data: Object.values(charts.departmentAttrition || {}) },
  ]);
  ChartHelpers.bar('aDistance', Object.keys(charts.distanceFromHome || {}), [{
    label: 'Count', data: Object.values(charts.distanceFromHome || {}), backgroundColor: '#4F4F4F', borderRadius: 8,
  }]);
  ChartHelpers.pie('aMarital', Object.keys(charts.maritalStatus || {}), Object.values(charts.maritalStatus || {}));
  ChartHelpers.groupedBar('aEduAttr', Object.keys(charts.educationAttrition || {}), [
    { label: 'Attrition %', data: Object.values(charts.educationAttrition || {}) },
  ]);
}

function renderAllInsights(insights) {
  const panel = document.getElementById('allInsights');
  if (!panel) return;
  panel.innerHTML = insights.map(i => `
    <div class="insight-item">
      <h4>${i.title}</h4>
      <p>${i.insight}</p>
    </div>
  `).join('');
}

async function renderModelComparison() {
  const container = document.getElementById('modelComparison');
  if (!container) return;
  try {
    const data = await API.get('/model-metrics');
    container.innerHTML = data.models?.map(m => `
      <div class="metric-box">
        <div class="value">${(m.roc_auc * 100).toFixed(1)}%</div>
        <div class="label">${m.model} AUC</div>
      </div>
    `).join('') || '';
  } catch { /* ignore */ }
}

async function initDepartments() {
  App.showLoading();
  try {
    const data = await API.get('/departments');
    const grid = document.getElementById('deptGrid');
    if (grid) {
      grid.innerHTML = data.departments.map(d => `
        <div class="kpi-card">
          <div class="kpi-header"><span class="kpi-label">${d.name}</span><div class="kpi-icon">🏢</div></div>
          <div class="kpi-value" style="font-size:24px">${d.count}</div>
          <div class="kpi-change">Attrition: ${d.attritionRate}% | Avg Salary: ${App.formatCurrency(d.avgSalary)} | Avg Age: ${d.avgAge}</div>
        </div>
      `).join('');
    }
    const charts = (await API.get('/dashboard')).charts;
    ChartHelpers.groupedBar('deptAttrChart', Object.keys(charts.departmentAttrition || {}), [
      { label: 'Attrition %', data: Object.values(charts.departmentAttrition || {}) },
    ]);
  } catch (err) {
    App.showToast('Failed to load departments', 'error');
  } finally {
    App.hideLoading();
  }
}

async function initJobs() {
  App.showLoading();
  try {
    const data = await API.get('/jobs');
    const grid = document.getElementById('jobsGrid');
    if (grid) {
      grid.innerHTML = data.jobs.map(j => `
        <div class="kpi-card">
          <div class="kpi-header"><span class="kpi-label">${j.name}</span><div class="kpi-icon">💼</div></div>
          <div class="kpi-value" style="font-size:24px">${j.count}</div>
          <div class="kpi-change">Attrition: ${j.attritionRate}% | Avg Salary: ${App.formatCurrency(j.avgSalary)}</div>
        </div>
      `).join('');
    }
    const charts = (await API.get('/dashboard')).charts;
    ChartHelpers.horizontalBar('jobsChart', Object.keys(charts.jobRole || {}), Object.values(charts.jobRole || {}));
    ChartHelpers.groupedBar('jobsAttrChart', Object.keys(charts.jobRoleAttrition || {}).slice(0, 10), [
      { label: 'Attrition %', data: Object.values(charts.jobRoleAttrition || {}).slice(0, 10) },
    ]);
  } catch (err) {
    App.showToast('Failed to load jobs', 'error');
  } finally {
    App.hideLoading();
  }
}

window.initAnalytics = initAnalytics;
window.initDepartments = initDepartments;
window.initJobs = initJobs;
