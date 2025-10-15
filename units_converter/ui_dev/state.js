"use strict";

export const state = {
  families: [],
  units: new Map(),
  selectedFamily: null,
  history: [],
  favorites: [],
};

const MAX_HISTORY = 25;

export const PRESETS = {
  pressure: [
    { label: "MPa → ksi", from: "MPa", to: "ksi" },
    { label: "MPa → N/mm^2", from: "MPa", to: "N/mm^2" },
  ],
  length: [
    { label: "Å → nm", from: "Å", to: "nm" },
    { label: "micron → mm", from: "micron", to: "mm" },
  ],
  energy: [
    { label: "kJ/mol → eV", from: "kJ/mol", to: "eV" },
  ],
  temperature: [
    { label: "°C → K", from: "degC", to: "K" },
    { label: "Δ°C → K", from: "degC", to: "K", mode: "interval" },
  ],
};

export function setFamilies(families) {
  state.families = Array.isArray(families) ? families.slice().sort() : [];
}

export function setUnits(family, units) {
  if (!family) return;
  state.units.set(family, Array.isArray(units) ? units.slice() : []);
}

export function getUnits(family) {
  return state.units.get(family) || [];
}

export function selectFamily(family) {
  state.selectedFamily = family;
}

export function addHistoryEntry(entry) {
  state.history.unshift(entry);
  if (state.history.length > MAX_HISTORY) {
    state.history.length = MAX_HISTORY;
  }
}

export function clearHistory() {
  state.history = [];
}

export function addFavorite(entry) {
  if (!state.favorites.find((item) => item.key === entry.key)) {
    state.favorites.push(entry);
  }
}

export function removeFavorite(key) {
  state.favorites = state.favorites.filter((entry) => entry.key !== key);
}

export function getHistory() {
  return state.history.slice();
}

export function getFavorites() {
  return state.favorites.slice();
}

export function entryKey(data) {
  return [data.value, data.from, data.to, data.mode].join("::");
}
