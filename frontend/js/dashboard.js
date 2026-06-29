async function initDashboard() {
  App.showLoading();
  try {
    const data = await API.get('/dashboard');
    renderKPIs(data.kpis);
    renderCharts(data.charts, data.featureImportance);
    renderInsights();
    renderEmployeePreview();
  } catch (err) {
    App.showToast('Failed to load dashboard data. Is the backend running?', 'error');
    console.error(err);
  } finally {
    App.hideLoading();
  }
}

function renderKPIs(kpis) {
  const grid = document.getElementById('kpiGrid');
  if (!grid || !kpis) return;

  const cards = [
    { label: 'Total Employees', value: kpis.totalEmployees, icon: '👥', cls: '' },
    { label: 'Active Employees', value: kpis.activeEmployees, icon: '✅', cls: 'gold' },
    { label: 'Employees Left', value: kpis.employeesLeft, icon: '🚪', cls: 'dark' },
    { label: 'Attrition Rate', value: kpis.attritionRate, icon: '📉', cls: '', suffix: '%' },
    { label: 'Average Salary', value: kpis.averageSalary, icon: '💰', cls: '', currency: true },
    { label: 'Average Experience', value: kpis.averageExperience, icon: '📅', cls: '', suffix: ' yrs' },
    { label: 'Average Age', value: kpis.averageAge, icon: '🎂', cls: '' },
    { label: 'Avg Satisfaction', value: kpis.averageSatisfaction, icon: '😊', cls: 'gold', suffix: '/4' },
  ];

  grid.innerHTML = cards.map((c, i) => `
    <div class="kpi-card ${c.cls}" style="animation-delay:${i * 0.08}s">
      <div class="kpi-header">
        <span class="kpi-label">${c.label}</span>
        <div class="kpi-icon">${c.icon}</div>
      </div>
      <div class="kpi-value" id="kpi-${i}">0</div>
    </div>
  `).join('');

  cards.forEach((c, i) => {
    const el = document.getElementById(`kpi-${i}`);
    const val = c.currency ? kpis.averageSalary : c.value;
    if (c.currency) {
      el.textContent = App.formatCurrency(val);
    } else {
      App.animateCounter(el, val, 1200, c.suffix || '');
    }
  });
}

function renderCharts(charts, featureImportance) {
  if (!charts) return;

  ChartHelpers.doughnut('chartGender', Object.keys(charts.gender || {}), Object.values(charts.gender || {}));
  ChartHelpers.bar('chartAge', Object.keys(charts.ageGroups || {}), [{
    label: 'Employees', data: Object.values(charts.ageGroups || {}), backgroundColor: '#D4AF37', borderRadius: 8,
  }]);
  ChartHelpers.bar('chartEducation', Object.keys(charts.education || {}), [{
    label: 'Count', data: Object.values(charts.education || {}), backgroundColor: '#4F4F4F', borderRadius: 8,
  }]);
  ChartHelpers.groupedBar('chartDeptAttrition', Object.keys(charts.departmentAttrition || {}), [
    { label: 'Attrition %', data: Object.values(charts.departmentAttrition || {}) },
  ]);
  ChartHelpers.horizontalBar('chartJobRole', Object.keys(charts.jobRole || {}), Object.values(charts.jobRole || {}));
  ChartHelpers.groupedBar('chartJobRoleAttrition', Object.keys(charts.jobRoleAttrition || {}).slice(0, 8), [
    { label: 'Attrition %', data: Object.values(charts.jobRoleAttrition || {}).slice(0, 8) },
  ]);
  ChartHelpers.bar('chartIncome', Object.keys(charts.salaryBins || {}), [{
    label: 'Employees', data: Object.values(charts.salaryBins || {}), backgroundColor: '#B8962E', borderRadius: 8,
  }]);
  ChartHelpers.bar('chartJobSat', Object.keys(charts.jobSatisfaction || {}), [{
    label: 'Count', data: Object.values(charts.jobSatisfaction || {}), backgroundColor: '#D4AF37', borderRadius: 8,
  }]);
  ChartHelpers.bar('chartEnvSat', Object.keys(charts.environmentSatisfaction || {}), [{
    label: 'Count', data: Object.values(charts.environmentSatisfaction || {}), backgroundColor: '#4F4F4F', borderRadius: 8,
  }]);
  ChartHelpers.bar('chartRelSat', Object.keys(charts.relationshipSatisfaction || {}), [{
    label: 'Count', data: Object.values(charts.relationshipSatisfaction || {}), backgroundColor: '#B8962E', borderRadius: 8,
  }]);
  ChartHelpers.pie('chartOverTime', Object.keys(charts.overTime || {}), Object.values(charts.overTime || {}));
  ChartHelpers.bar('chartTravel', Object.keys(charts.businessTravel || {}), [{
    label: 'Count', data: Object.values(charts.businessTravel || {}), backgroundColor: '#D4AF37', borderRadius: 8,
  }]);
  ChartHelpers.bar('chartPerformance', Object.keys(charts.performanceRating || {}), [{
    label: 'Count', data: Object.values(charts.performanceRating || {}), backgroundColor: '#4F4F4F', borderRadius: 8,
  }]);
  ChartHelpers.bar('chartWLB', Object.keys(charts.workLifeBalance || {}), [{
    label: 'Count', data: Object.values(charts.workLifeBalance || {}), backgroundColor: '#E8D5A3', borderRadius: 8,
  }]);
  ChartHelpers.groupedBar('chartAgeAttrition', Object.keys(charts.ageGroupAttrition || {}), [
    { label: 'Attrition %', data: Object.values(charts.ageGroupAttrition || {}) },
  ]);

  if (featureImportance) {
    const entries = Object.entries(featureImportance).slice(0, 10);
    ChartHelpers.horizontalBar('chartFeatureImp', entries.map(e => e[0]), entries.map(e => e[1]));
  }
}

async function renderInsights() {
  const panel = document.getElementById('insightsPanel');
  if (!panel) return;
  try {
    const data = await API.get('/insights');
    const insights = (data.insights || []).slice(0, 6);
    panel.innerHTML = insights.map(i => `
      <div class="insight-item">
        <h4>${i.title}</h4>
        <p>${i.insight}</p>
      </div>
    `).join('');
  } catch { panel.innerHTML = '<p>Insights loading...</p>'; }
}

async function renderEmployeePreview() {
  const tbody = document.getElementById('employeePreviewBody');
  if (!tbody) return;
  try {
    const data = await API.get('/employees?per_page=8');
    tbody.innerHTML = data.employees.map(e => `
      <tr>
        <td>${e.EmployeeNumber}</td>
        <td>${e.Department}</td>
        <td>${e.JobRole}</td>
        <td>${e.Age}</td>
        <td>${App.formatCurrency(e.MonthlyIncome)}</td>
        <td><span class="badge badge-${e.Attrition === 'Yes' ? 'yes' : 'no'}">${e.Attrition}</span></td>
      </tr>
    `).join('');
  } catch { tbody.innerHTML = '<tr><td colspan="6">Unable to load employees</td></tr>'; }
}

document.addEventListener('DOMContentLoaded', () => {
  App.initApp('Dashboard', 'Workforce analytics overview');
  initDashboard();
});
