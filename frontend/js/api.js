const API = {
  base: () => window.HR_API_BASE,

  async get(endpoint) {
    const res = await fetch(`${this.base()}${endpoint}`);
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  },

  async post(endpoint, data) {
    const res = await fetch(`${this.base()}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
  },

  async upload(file) {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(`${this.base()}/upload`, { method: 'POST', body: form });
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
    return res.json();
  },

  downloadUrl(format) {
    return `${this.base()}/download-report?format=${format}`;
  },
};

window.API = API;
