const API_URL = import.meta.env.VITE_API_URL;

console.log("VITE_API_URL =", import.meta.env.VITE_API_URL);

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) throw new Error(`GET ${path} -> ${res.status}`);
  return res.json();
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const text = await res.text();
  let data: any = null;
  try { data = text ? JSON.parse(text) : null; } catch { /* ignore */ }

  if (!res.ok) {
    const detail = data?.detail ? JSON.stringify(data.detail) : text;
    throw new Error(`POST ${path} -> ${res.status} | ${detail}`);
  }
  return data as T;
}