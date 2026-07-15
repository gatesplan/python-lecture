const BASE = '/api';

async function request(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (res.status === 204) return null;
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json();
}

// Problems
export const getProblems = (tags) => {
  const q = tags ? `?tags=${encodeURIComponent(tags)}` : '';
  return request(`/problems${q}`);
};
export const getProblem = (id) => request(`/problems/${id}`);
export const createProblem = (data) => request('/problems', { method: 'POST', body: JSON.stringify(data) });
export const updateProblem = (id, data) => request(`/problems/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteProblem = (id) => request(`/problems/${id}`, { method: 'DELETE' });

// Tags
export const getTags = () => request('/tags');

// Exams
export const getExams = () => request('/exams');
export const getExam = (id) => request(`/exams/${id}`);
export const createExam = (data) => request('/exams', { method: 'POST', body: JSON.stringify(data) });
export const updateExam = (id, data) => request(`/exams/${id}`, { method: 'PUT', body: JSON.stringify(data) });
export const deleteExam = (id) => request(`/exams/${id}`, { method: 'DELETE' });
export const renderExam = (id) => request(`/exams/${id}/render`);
