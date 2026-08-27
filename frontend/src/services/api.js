/**
 * API service – the only module that talks to FastAPI.
 *
 * React → api.js → FastAPI → Service → Repository → CognoDB
 *
 * Never import neo4j or CognoDB anything here.
 */

const BASE = '/api';

async function request(path) {
  const res = await fetch(`${BASE}${path}`);
  const data = await res.json();

  if (!res.ok) {
    const error = new Error(data.error || `Request failed: ${res.status}`);
    error.status = res.status;
    throw error;
  }

  return data;
}

// --- Skills ---

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
