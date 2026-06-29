const CHART_COLORS = ['#D4AF37', '#4F4F4F', '#B8962E', '#6B6B6B', '#E8D5A3', '#3D3D3D', '#F5E6A3', '#8B7355'];
const CHART_DEFAULTS = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { font: { family: 'Inter', size: 12 }, padding: 16 } },
  },
};

const ChartHelpers = {
  _isDark: false,

  updateTheme(isDark) {
    this._isDark = isDark;
    Chart.defaults.color = isDark ? '#A0A0A0' : '#6B6B6B';
    Chart.defaults.borderColor = isDark ? '#404040' : '#E0E0E0';
  },

  destroyChart(id) {
    const existing = Chart.getChart(id);
    if (existing) existing.destroy();
  },

  doughnut(canvasId, labels, data, options = {}) {
    this.destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{ data, backgroundColor: CHART_COLORS.slice(0, labels.length), borderWidth: 2, borderColor: '#fff' }],
      },
      options: { ...CHART_DEFAULTS, cutout: '65%', ...options },
    });
  },

  bar(canvasId, labels, datasets, options = {}) {
    this.destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets },
      options: {
        ...CHART_DEFAULTS,
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.05)' } },
          x: { grid: { display: false } },
        },
        ...options,
      },
    });
  },

  horizontalBar(canvasId, labels, data, options = {}) {
    this.destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ data, backgroundColor: CHART_COLORS[0], borderRadius: 8 }],
      },
      options: {
        ...CHART_DEFAULTS,
        indexAxis: 'y',
        scales: { x: { beginAtZero: true }, y: { grid: { display: false } } },
        ...options,
      },
    });
  },

  line(canvasId, labels, datasets, options = {}) {
    this.destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
      type: 'line',
      data: { labels, datasets },
      options: {
        ...CHART_DEFAULTS,
        scales: { y: { beginAtZero: true } },
        elements: { line: { tension: 0.4 } },
        ...options,
      },
    });
  },

  pie(canvasId, labels, data) {
    this.destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
      type: 'pie',
      data: {
        labels,
        datasets: [{ data, backgroundColor: CHART_COLORS.slice(0, labels.length) }],
      },
      options: CHART_DEFAULTS,
    });
  },

  gauge(canvasId, value, max = 100) {
    this.destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    const color = value < 35 ? '#22C55E' : value < 65 ? '#EAB308' : '#EF4444';
    return new Chart(ctx, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [value, max - value],
          backgroundColor: [color, '#E0E0E0'],
          borderWidth: 0,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        circumference: 180,
        rotation: -90,
        cutout: '75%',
        plugins: { legend: { display: false }, tooltip: { enabled: false } },
      },
    });
  },

  groupedBar(canvasId, labels, datasets) {
    return this.bar(canvasId, labels, datasets.map((d, i) => ({
      label: d.label,
      data: d.data,
      backgroundColor: CHART_COLORS[i],
      borderRadius: 6,
    })));
  },
};

window.ChartHelpers = ChartHelpers;
