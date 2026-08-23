const byId = (id) => document.getElementById(id);

async function jsonRequest(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.message || payload.error || "The conversion could not be completed.");
  }
  return payload;
}

async function loadUnits() {
  const family = byId("family").value;
  const payload = await jsonRequest(`/api/units/${encodeURIComponent(family)}`);
  for (const id of ["from", "to"]) {
    const select = byId(id);
    select.replaceChildren(...payload.units.map((unit) => {
      const option = document.createElement("option");
      option.value = unit;
      option.textContent = unit;
      return option;
    }));
  }
  if (payload.units.length > 1) byId("to").selectedIndex = 1;
}

byId("family").addEventListener("change", () => loadUnits().catch(showError));
byId("convert").addEventListener("click", async () => {
  try {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    const payload = await jsonRequest("/api/v1/units/convert", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({value: Number(byId("value").value), from: byId("from").value, to: byId("to").value, mode}),
    });
    byId("convert-result").textContent = payload.text;
  } catch (error) {
    byId("convert-result").textContent = error.message;
  }
});
byId("evaluate").addEventListener("click", async () => {
  try {
    const payload = await jsonRequest("/api/expressions", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({expression: byId("expression").value}),
    });
    byId("expression-result").textContent = payload.formatted;
  } catch (error) {
    byId("expression-result").textContent = error.message;
  }
});
function showError(error) { byId("convert-result").textContent = error.message; }
loadUnits().catch(showError);

