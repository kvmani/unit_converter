"use strict";

const API_PREFIX = "/api/v1/units";

async function request(path, options = {}) {
  const response = await fetch(`${API_PREFIX}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "same-origin",
    ...options,
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ message: response.statusText }));
    const error = new Error(payload.message || "Request failed");
    error.code = payload.error_code || "REQUEST_FAILED";
    throw error;
  }
  return response.json();
}

export async function fetchFamilies() {
  return request("/families");
}

export async function fetchUnits(family) {
  const url = new URL(`${API_PREFIX}/units`, window.location.origin);
  url.searchParams.set("family", family);
  const response = await fetch(url.toString(), { credentials: "same-origin" });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    const error = new Error(payload.message || response.statusText);
    error.code = payload.error_code || "REQUEST_FAILED";
    throw error;
  }
  return response.json();
}

export async function convert(body) {
  return request("/convert", { method: "POST", body: JSON.stringify(body) });
}

export async function convertExpression(body) {
  return request("/convert/expression", { method: "POST", body: JSON.stringify(body) });
}
