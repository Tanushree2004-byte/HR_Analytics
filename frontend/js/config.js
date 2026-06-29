(function () {
  const stored = localStorage.getItem('hr-api-url');
  if (stored) {
    window.HR_API_BASE = stored;
    return;
  }
  const host = window.location.hostname;
  const port = window.location.port;
  if (host === 'localhost' || host === '127.0.0.1') {
    window.HR_API_BASE = port === '5000'
      ? `${window.location.origin}/api`
      : `http://${host}:5000/api`;
  } else {
    window.HR_API_BASE = window.__RENDER_API_URL__ || `${window.location.origin}/api`;
  }
})();
