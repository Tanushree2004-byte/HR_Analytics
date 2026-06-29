let currentPage = 1;
let sortBy = 'EmployeeNumber';
let sortDir = 'asc';

async function loadEmployees(page = 1) {
  currentPage = page;
  const search = document.getElementById('empSearch')?.value || new URLSearchParams(window.location.search).get('search') || '';
  const department = document.getElementById('deptFilter')?.value || '';

  if (search && document.getElementById('empSearch')) {
    document.getElementById('empSearch').value = search;
  }

  App.showLoading();
  try {
    const data = await API.get(`/employees?page=${page}&per_page=15&search=${encodeURIComponent(search)}&department=${encodeURIComponent(department)}&sort_by=${sortBy}&sort_dir=${sortDir}`);
    renderTable(data);
    renderPagination(data);
  } catch (err) {
    App.showToast('Failed to load employees', 'error');
  } finally {
    App.hideLoading();
  }
}

function renderTable(data) {
  const tbody = document.getElementById('employeeTableBody');
  if (!tbody) return;

  tbody.innerHTML = data.employees.map(e => `
    <tr>
      <td>${e.EmployeeNumber}</td>
      <td>${e.Age}</td>
      <td>${e.Gender}</td>
      <td>${e.Department}</td>
      <td>${e.JobRole}</td>
      <td>${App.formatCurrency(e.MonthlyIncome)}</td>
      <td>${e.YearsAtCompany}</td>
      <td>${e.OverTime}</td>
      <td>${e.AvgSatisfaction?.toFixed(1) || '—'}</td>
      <td><span class="badge badge-${e.Attrition === 'Yes' ? 'yes' : 'no'}">${e.Attrition}</span></td>
    </tr>
  `).join('') || '<tr><td colspan="10">No employees found</td></tr>';

  document.getElementById('totalCount').textContent = `${data.total} employees`;
}

function renderPagination(data) {
  const pag = document.getElementById('pagination');
  if (!pag) return;
  let html = `<button ${data.page <= 1 ? 'disabled' : ''} onclick="loadEmployees(${data.page - 1})">← Prev</button>`;
  for (let i = 1; i <= Math.min(data.totalPages, 7); i++) {
    html += `<button class="${i === data.page ? 'active' : ''}" onclick="loadEmployees(${i})">${i}</button>`;
  }
  html += `<button ${data.page >= data.totalPages ? 'disabled' : ''} onclick="loadEmployees(${data.page + 1})">Next →</button>`;
  pag.innerHTML = html;
}

function exportCSV() {
  window.open(API.downloadUrl('csv'), '_blank');
  App.showToast('CSV export started', 'success');
}

function setupSort() {
  document.querySelectorAll('thead th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.dataset.sort;
      if (sortBy === col) sortDir = sortDir === 'asc' ? 'desc' : 'asc';
      else { sortBy = col; sortDir = 'asc'; }
      loadEmployees(currentPage);
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  App.initApp('Employees', 'Workforce directory and management');
  setupSort();
  loadEmployees();

  document.getElementById('empSearch')?.addEventListener('input', debounce(() => loadEmployees(1), 400));
  document.getElementById('deptFilter')?.addEventListener('change', () => loadEmployees(1));
  document.getElementById('exportBtn')?.addEventListener('click', exportCSV);
});

function debounce(fn, ms) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

window.loadEmployees = loadEmployees;
