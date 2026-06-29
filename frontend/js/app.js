const NAV_ITEMS = [
  { href: 'index.html', icon: '⊞', label: 'Dashboard', page: 'dashboard' },
  { href: 'employees.html', icon: '👥', label: 'Employees', page: 'employees' },
  { href: 'departments.html', icon: '🏢', label: 'Departments', page: 'departments' },
  { href: 'jobs.html', icon: '💼', label: 'Jobs', page: 'jobs' },
  { href: 'analytics.html', icon: '📊', label: 'Analytics', page: 'analytics' },
  { href: 'prediction.html', icon: '🎯', label: 'Prediction', page: 'prediction' },
  { href: 'reports.html', icon: '📄', label: 'Reports', page: 'reports' },
];

const BOTTOM_NAV = [
  { href: 'settings.html', icon: '⚙', label: 'Settings', page: 'settings' },
  { href: 'support.html', icon: '💬', label: 'Support', page: 'support' },
];

function getCurrentPage() {
  const path = window.location.pathname.split('/').pop() || 'index.html';
  return path.replace('.html', '') === 'index' ? 'dashboard' : path.replace('.html', '');
}

function renderSidebar() {
  const current = getCurrentPage();
  const sidebar = document.getElementById('sidebar');
  if (!sidebar) return;

  const navHtml = NAV_ITEMS.map(item => `
    <a href="${item.href}" class="nav-item ${current === item.page ? 'active' : ''}" data-page="${item.page}">
      <span class="nav-icon">${item.icon}</span>
      <span>${item.label}</span>
    </a>
  `).join('');

  const bottomHtml = BOTTOM_NAV.map(item => `
    <a href="${item.href}" class="nav-item ${current === item.page ? 'active' : ''}">
      <span class="nav-icon">${item.icon}</span>
      <span>${item.label}</span>
    </a>
  `).join('');

  sidebar.innerHTML = `
    <button class="sidebar-toggle" id="sidebarToggle" aria-label="Toggle sidebar">‹</button>
    <div class="sidebar-logo">
      <div class="logo-icon">HR</div>
      <span class="logo-text">HR Intelligence</span>
    </div>
    <nav class="sidebar-nav">${navHtml}</nav>
    <div class="sidebar-bottom">${bottomHtml}</div>
  `;

  document.getElementById('sidebarToggle')?.addEventListener('click', toggleSidebar);
}

function renderTopbar(title, subtitle) {
  const topbar = document.getElementById('topbar');
  if (!topbar) return;

  const now = new Date();
  const dateStr = now.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

  topbar.innerHTML = `
    <div class="topbar-left">
      <h1>${title}</h1>
      <p>${subtitle || ''}</p>
    </div>
    <div class="topbar-right">
      <div class="search-box">
        <span>🔍</span>
        <input type="text" id="globalSearch" placeholder="Search employees, departments...">
      </div>
      <span class="date-display">${dateStr}</span>
      <div class="topbar-icon" id="notifBtn" title="Notifications">
        🔔<span class="notification-dot"></span>
      </div>
      <div class="topbar-icon" id="themeToggle" title="Toggle theme">🌙</div>
      <div class="profile-chip">
        <div class="profile-avatar">T</div>
        <span class="profile-name">Tanushree</span>
      </div>
    </div>
  `;

  document.getElementById('themeToggle')?.addEventListener('click', toggleTheme);
  document.getElementById('globalSearch')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.value.trim()) {
      window.location.href = `employees.html?search=${encodeURIComponent(e.target.value.trim())}`;
    }
  });
}

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const main = document.querySelector('.main-content');
  sidebar?.classList.toggle('collapsed');
  main?.classList.toggle('expanded');
  const btn = document.getElementById('sidebarToggle');
  if (btn) btn.textContent = sidebar?.classList.contains('collapsed') ? '›' : '‹';
}

function toggleTheme() {
  document.body.classList.toggle('dark-mode');
  const isDark = document.body.classList.contains('dark-mode');
  localStorage.setItem('hr-theme', isDark ? 'dark' : 'light');
  const btn = document.getElementById('themeToggle');
  if (btn) btn.textContent = isDark ? '☀️' : '🌙';
  ChartHelpers?.updateTheme(isDark);
}

function initTheme() {
  if (localStorage.getItem('hr-theme') === 'dark') {
    document.body.classList.add('dark-mode');
  }
}

function showLoading() {
  let overlay = document.getElementById('loadingOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
  }
  overlay.classList.remove('hidden');
}

function hideLoading() {
  document.getElementById('loadingOverlay')?.classList.add('hidden');
}

function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

function animateCounter(el, target, duration = 1200, suffix = '') {
  const start = 0;
  const startTime = performance.now();
  const isFloat = String(target).includes('.');

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = start + (target - start) * eased;
    el.textContent = isFloat ? current.toFixed(1) + suffix : Math.round(current).toLocaleString() + suffix;
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

function formatCurrency(val) {
  return '$' + Number(val).toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

function initApp(title, subtitle) {
  initTheme();
  renderSidebar();
  renderTopbar(title, subtitle);
}

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(hideLoading, 600);
});

window.App = { initApp, showLoading, hideLoading, showToast, animateCounter, formatCurrency, toggleSidebar };
