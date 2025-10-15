"use strict";

import { PRESETS, entryKey, getFavorites, getHistory } from "./state.js";

export function populateFamilySelect(selectEl, families) {
  selectEl.innerHTML = "";
  const defaultOption = document.createElement("option");
  defaultOption.value = "";
  defaultOption.textContent = "Choose family";
  selectEl.appendChild(defaultOption);
  families.forEach((family) => {
    const option = document.createElement("option");
    option.value = family;
    option.textContent = family;
    selectEl.appendChild(option);
  });
}

export function renderPresets(listEl, family, onPresetClick) {
  listEl.innerHTML = "";
  const presets = PRESETS[family] || [];
  if (presets.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "No presets available";
    listEl.appendChild(empty);
    return;
  }
  presets.forEach((preset) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = preset.label;
    button.addEventListener("click", () => onPresetClick(preset));
    item.appendChild(button);
    listEl.appendChild(item);
  });
}

export function renderHistory(listEl, template, entries, onAction) {
  listEl.innerHTML = "";
  entries.forEach((entry) => {
    const clone = template.content.firstElementChild.cloneNode(true);
    const actionButtons = clone.querySelectorAll("[data-action]");
    const button = clone.querySelector(".history-entry");
    button.textContent = entry.text;
    button.addEventListener("click", () => onAction("replay", entry));
    actionButtons.forEach((action) => {
      action.addEventListener("click", (event) => {
        event.stopPropagation();
        onAction(action.getAttribute("data-action"), entry);
      });
    });
    listEl.appendChild(clone);
  });
}

export function renderFavorites(listEl, template, entries, onAction) {
  listEl.innerHTML = "";
  entries.forEach((entry) => {
    const clone = template.content.firstElementChild.cloneNode(true);
    const button = clone.querySelector(".history-entry");
    button.textContent = entry.text;
    button.addEventListener("click", () => onAction("replay", entry));
    const removeButton = clone.querySelector("[data-action='remove']");
    removeButton.addEventListener("click", (event) => {
      event.stopPropagation();
      onAction("remove", entry);
    });
    listEl.appendChild(clone);
  });
}

export function updateHistoryUI(historyList, historyTemplate, favoritesList, favoritesTemplate, handler) {
  renderHistory(historyList, historyTemplate, getHistory(), handler);
  renderFavorites(favoritesList, favoritesTemplate, getFavorites(), handler);
}

export function enableCopyButtons(container, handler) {
  container.hidden = false;
  if (container.dataset.bound === "true") {
    return;
  }
  container.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => handler(button.dataset.copy));
  });
  container.dataset.bound = "true";
}

export function setStatus(element, text, isError = false) {
  element.textContent = text;
  element.classList.toggle("error", isError);
}

export function fillForm(form, data) {
  form.value.value = data.value;
  form.from.value = data.from;
  form.to.value = data.to;
  if (data.mode) {
    form.mode.value = data.mode;
  }
}
