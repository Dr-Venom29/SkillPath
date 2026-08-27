/**
 * API service – the only module that talks to FastAPI.
 *
 * React → api.js → FastAPI → Service → Repository → CognoDB
 *
 * Never import neo4j or CognoDB anything here.
 */

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '');

async function request(path) {
  try {
    const res = await fetch(`${API_BASE_URL}${path}`);
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      const isServerError = res.status >= 500;
      const cleanMessage = isServerError
        ? "We couldn't reach the learning graph. Please try again."
        : data.error || `Request failed (${res.status})`;

      const error = new Error(cleanMessage);
      error.status = res.status;
      throw error;
    }

    return data;
  } catch (err) {
    if (err.status && err.status < 500) {
      throw err;
    }
    const error = new Error("We couldn't reach the learning graph. Please try again.");
    error.status = err.status || 500;
    throw error;
  }
}

// --- Skills ---

export function listSkills() {
  return request('/skills');
}

export function searchSkills(query, limit = 25) {
  return request(`/skills/search?q=${encodeURIComponent(query)}&limit=${limit}`);
}

export function getSkillDetails(skillId) {
  return request(`/skills/${encodeURIComponent(skillId)}`);
}

export function getPrerequisites(skillId) {
  return request(`/skills/${encodeURIComponent(skillId)}/prerequisites`);
}

export function getRelatedSkills(skillId) {
  return request(`/skills/${encodeURIComponent(skillId)}/related`);
}

export function getPrerequisiteChain(skillId) {
  return request(`/skills/${encodeURIComponent(skillId)}/chain`);
}

export function getNextSkills(skillId) {
  return request(`/skills/${encodeURIComponent(skillId)}/next`);
}

// --- Roles ---

export function listRoles() {
  return request('/roles');
}

export function getRoleDetails(roleId) {
  return request(`/roles/${encodeURIComponent(roleId)}`);
}

export function getRoleGraph(roleId) {
  return request(`/roles/${encodeURIComponent(roleId)}/graph`);
}

// --- Paths ---

export function findLearningPath(fromId, toId) {
  return request(`/paths?from=${encodeURIComponent(fromId)}&to=${encodeURIComponent(toId)}`);
}

// --- Health ---

export function checkHealth() {
  return request('/health');
}
