"use strict";

import {
  addFavorite,
  addHistoryEntry,
  clearHistory,
  entryKey,
  removeFavorite,
  selectFamily,
  setFamilies,
  setUnits,
  state,
} from "./state.js";
import { convert, fetchFamilies, fetchUnits } from "./api.js";
import {
  enableCopyButtons,
  fillForm,
  populateFamilySelect,
  renderPresets,
  setStatus,
  updateHistoryUI,
} from "./ui.js";

const form = document.querySelector("#convert-form");
const valueInput = document.querySelector("#from-value");
const fromInput = document.querySelector("#from-unit");
const toInput = document.querySelector("#to-unit");
const familySelect = document.querySelector("#family-select");
const presetList = document.querySelector("#preset-list");
const resultDisplay = document.querySelector("#result-display");
const status = document.querySelector("#status");
const copyButtons = document.querySelector(".copy-buttons");
const historyList = document.querySelector("#history-list");
const favoritesList = document.querySelector("#favorites-list");
const historyTemplate = document.querySelector("#history-item-template");
const favoritesTemplate = document.querySelector("#favorite-item-template");
const clearHistoryButton = document.querySelector("#clear-history");
const swapButton = document.querySelector("#swap-button");

async function initialise() {
  try {
    const response = await fetchFamilies();
    setFamilies(response.families || []);
    populateFamilySelect(familySelect, state.families);
  } catch (error) {
    setStatus(status, error.message || "Unable to load families", true);
  }
}

familySelect.addEventListener("change", async (event) => {
  const family = event.target.value;
  selectFamily(family);
  renderPresets(presetList, family, applyPreset);
  if (!family) {
    return;
  }
  try {
    const response = await fetchUnits(family);
    setUnits(family, response.units || []);
  } catch (error) {
    setStatus(status, error.message || "Unable to load units", true);
  }
});

function applyPreset(preset) {
  fromInput.value = preset.from;
  toInput.value = preset.to;
  form.mode.value = preset.mode || "absolute";
  valueInput.focus();
}

function buildRequestBody() {
  const sigFigs = form.sig_figs.value ? Number(form.sig_figs.value) : undefined;
  const decimals = form.decimals.value ? Number(form.decimals.value) : undefined;
  return {
    value: valueInput.value,
    from: fromInput.value,
    to: toInput.value,
    mode: form.mode.value,
    notation: form.notation.value,
    sig_figs: sigFigs,
    decimals,
  };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  status.textContent = "Converting...";
  const body = buildRequestBody();
  try {
    const response = await convert(body);
    status.textContent = "";
    resultDisplay.textContent = response.text;
    const entry = {
      key: entryKey(body),
      text: `${body.value} ${body.from} → ${response.text}`,
      value: body.value,
      from: body.from,
      to: body.to,
      mode: body.mode,
      resultText: response.text,
      resultValue: response.result,
    };
    addHistoryEntry(entry);
    updateHistoryUI(historyList, historyTemplate, favoritesList, favoritesTemplate, handleHistoryAction);
    enableCopyButtons(copyButtons, (type) => handleCopy(type, entry));
  } catch (error) {
    setStatus(status, error.message || "Conversion failed", true);
    resultDisplay.textContent = "";
  }
});

function handleCopy(type, entry) {
  let textToCopy = "";
  if (type === "value") {
    textToCopy = String(entry.resultValue);
  } else if (type === "full") {
    textToCopy = entry.resultText;
  } else if (type === "latex") {
    textToCopy = `${entry.resultValue}\\,${entry.to}`;
  }
  if (!textToCopy) return;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(textToCopy).catch(() => {
      fallbackCopy(textToCopy);
    });
  } else {
    fallbackCopy(textToCopy);
  }
}

function fallbackCopy(text) {
  const temp = document.createElement("textarea");
  temp.value = text;
  temp.setAttribute("readonly", "");
  temp.style.position = "absolute";
  temp.style.left = "-9999px";
  document.body.appendChild(temp);
  temp.select();
  document.execCommand("copy");
  document.body.removeChild(temp);
}

function handleHistoryAction(action, entry) {
  if (action === "replay") {
    fillForm(form, entry);
    resultDisplay.textContent = entry.resultText;
  } else if (action === "favorite") {
    addFavorite(entry);
  } else if (action === "remove") {
    removeFavorite(entry.key);
  } else if (action === "copy") {
    handleCopy("full", entry);
  }
  updateHistoryUI(historyList, historyTemplate, favoritesList, favoritesTemplate, handleHistoryAction);
}

clearHistoryButton.addEventListener("click", () => {
  clearHistory();
  updateHistoryUI(historyList, historyTemplate, favoritesList, favoritesTemplate, handleHistoryAction);
});

swapButton.addEventListener("click", () => {
  const from = fromInput.value;
  fromInput.value = toInput.value;
  toInput.value = from;
});

initialise();
updateHistoryUI(historyList, historyTemplate, favoritesList, favoritesTemplate, handleHistoryAction);
valueInput.focus();
