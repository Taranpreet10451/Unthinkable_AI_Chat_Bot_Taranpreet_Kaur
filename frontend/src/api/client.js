const BASE_URL = 'https://unthinkable-solutions-ai-chatbot.onrender.com';

async function httpJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  const isJson = (response.headers.get('content-type') || '').includes('application/json');
  const data = isJson ? await response.json() : await response.text();
  if (!response.ok) {
    const message = typeof data === 'string' ? data : (data && data.error) || 'Request failed';
    throw new Error(message);
  }
  return data;
}

export async function getHealth() {
  return await httpJson(`${BASE_URL}/health`, { method: 'GET' });
}

export async function postChat({ sessionId, message }) {
  return await httpJson(`${BASE_URL}/chat`, {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId, message }),
  });
}

export async function postReset({ sessionId }) {
  return await httpJson(`${BASE_URL}/reset`, {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId }),
  });
}


