const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export function listStartups(params = {}) {
  const qs = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== '') qs.set(k, v);
  }
  const suffix = qs.toString() ? `?${qs}` : '';
  return request(`/startups${suffix}`);
}

export function getStartup(id) {
  return request(`/startups/${id}`);
}

export function createStartup(payload) {
  return request('/startups', { method: 'POST', body: JSON.stringify(payload) });
}

export function updateStartup(id, payload) {
  return request(`/startups/${id}`, { method: 'PUT', body: JSON.stringify(payload) });
}

export function deleteStartup(id) {
  return request(`/startups/${id}`, { method: 'DELETE' });
}

export function getFacets() {
  return request('/facets');
}
