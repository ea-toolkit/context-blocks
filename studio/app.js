/* Context Blocks Studio — thin client over the Studio API.
 * Served by the API at /ui (same origin) → root-relative fetches. Override the
 * base for standalone use via window.CB_API_BASE. */

const API = (window.CB_API_BASE || "").replace(/\/$/, "");

const els = {};
let currentBlock = null;

// ── HTTP ──────────────────────────────────────────────────────────────────

async function api(path, options) {
  const res = await fetch(`${API}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  let body = null;
  try {
    body = await res.json();
  } catch (_) {
    /* no JSON body */
  }
  return { ok: res.ok, status: res.status, body };
}

// ── UI helpers ──────────────────────────────────────────────────────────────

function show(view) {
  ["empty-view", "create-view", "block-view"].forEach((id) => {
    els[id].hidden = id !== view;
  });
}

let toastTimer = null;
function toast(message, kind = "ok") {
  const t = els["toast"];
  t.textContent = message;
  t.className = `toast ${kind}`;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.hidden = true), 4000);
}

function detailMessage(body) {
  const d = body && body.detail;
  if (!d) return "Request failed";
  if (typeof d === "string") return d;
  if (d.errors) return d.errors.join("; ");
  return JSON.stringify(d);
}

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "text") node.textContent = v;
    else node.setAttribute(k, v);
  }
  children.forEach((c) => node.append(c));
  return node;
}

// ── Blocks list ──────────────────────────────────────────────────────────────

async function loadBlocks() {
  const { ok, body } = await api("/blocks");
  if (!ok) return toast("Could not load blocks", "err");
  renderBlocks(body);
}

function renderBlocks(blocks) {
  const list = els["blocks-list"];
  list.replaceChildren();
  if (blocks.length === 0) {
    list.append(el("li", { class: "muted", text: "No blocks yet." }));
    return;
  }
  for (const b of blocks) {
    const item = el(
      "li",
      { class: "block-item" + (b.name === currentBlock ? " active" : ""), role: "button", tabindex: "0" },
      el("div", { class: "bi-label", text: b.label || b.name }),
      el("div", { class: "bi-count", text: `${b.name} · ${b.entity_count} entities` })
    );
    const open = () => openBlock(b.name);
    item.addEventListener("click", open);
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        open();
      }
    });
    list.append(item);
  }
}

// ── Block detail ─────────────────────────────────────────────────────────────

async function openBlock(name) {
  currentBlock = name;
  const detail = await api(`/blocks/${encodeURIComponent(name)}`);
  if (!detail.ok) return toast(detailMessage(detail.body), "err");
  const entities = await api(`/blocks/${encodeURIComponent(name)}/entities`);
  renderDetail(detail.body, entities.ok ? entities.body : []);
  await loadBlocks(); // refresh active highlight + counts
  show("block-view");
}

function renderDetail(block, entities) {
  els["bv-title"].textContent = block.label || block.name;
  els["bv-outputdir"].textContent = block.output_dir;
  els["bv-description"].textContent = block.description || "";
  els["bv-ontology"].textContent = block.ontology;

  const types = els["bv-types"];
  types.replaceChildren();
  (block.ontology_detail.types || []).forEach((t) => types.append(el("span", { class: "chip", text: t })));

  const layers = els["bv-layers"];
  layers.replaceChildren();
  (block.ontology_detail.layers || []).forEach((l) => layers.append(el("span", { class: "chip layer", text: l })));

  els["bv-count"].textContent = String(entities.length);
  const tbody = els["bv-entities"];
  tbody.replaceChildren();
  for (const e of entities) {
    tbody.append(
      el(
        "tr",
        {},
        el("td", { text: e.id }),
        el("td", { text: e.type }),
        el("td", { text: e.name }),
        el("td", { class: "path", text: e.path })
      )
    );
  }

  // Reset the add-entity form each time a block opens.
  els["add-entity-form"].hidden = true;
  els["ae-content"].value = "";
  els["ae-errors"].hidden = true;
}

// ── Create block ─────────────────────────────────────────────────────────────

function showCreate() {
  els["create-view"].reset();
  els["cb-ontology"].hidden = true;
  show("create-view");
  els["cb-name"].focus();
}

async function submitCreate(event) {
  event.preventDefault();
  const name = els["cb-name"].value.trim();
  if (!name) return toast("Name is required", "err");

  const payload = {
    name,
    label: els["cb-label"].value.trim(),
    description: els["cb-description"].value.trim(),
  };
  const useCustom = document.querySelector('input[name="onto"]:checked').value === "custom";
  if (useCustom) {
    const yaml = els["cb-ontology"].value.trim();
    if (yaml) payload.ontology_yaml = yaml;
  }
  const seed = els["cb-seed"].value.trim();
  if (seed) payload.seed_context = seed;

  const { ok, body } = await api("/blocks", { method: "POST", body: JSON.stringify(payload) });
  if (!ok) return toast(detailMessage(body), "err");
  toast(`Block '${body.name}' created`, "ok");
  await loadBlocks();
  await openBlock(body.name);
}

// ── Add entity ───────────────────────────────────────────────────────────────

async function submitAddEntity(event) {
  event.preventDefault();
  const content = els["ae-content"].value;
  if (!content.trim()) return toast("Paste entity markdown first", "err");

  const { ok, status, body } = await api(`/blocks/${encodeURIComponent(currentBlock)}/entities`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });

  const errBox = els["ae-errors"];
  if (ok) {
    errBox.hidden = true;
    toast(`Added '${body.id}' → ${body.path}`, "ok");
    await openBlock(currentBlock);
    return;
  }
  if (status === 422 && body && body.detail && body.detail.errors) {
    errBox.replaceChildren(...body.detail.errors.map((m) => el("li", { text: m })));
    errBox.hidden = false;
  } else {
    toast(detailMessage(body), "err");
  }
}

// ── Theme ────────────────────────────────────────────────────────────────────

function toggleTheme() {
  const root = document.documentElement;
  const next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
  root.setAttribute("data-theme", next);
}

// ── Wire up ──────────────────────────────────────────────────────────────────

function init() {
  const ids = [
    "blocks-list", "empty-view", "create-view", "block-view", "toast",
    "cb-name", "cb-label", "cb-description", "cb-ontology", "cb-seed",
    "bv-title", "bv-outputdir", "bv-description", "bv-ontology", "bv-types",
    "bv-layers", "bv-count", "bv-entities", "add-entity-form", "ae-content", "ae-errors",
  ];
  ids.forEach((id) => (els[id] = document.getElementById(id)));

  document.getElementById("new-block-btn").addEventListener("click", showCreate);
  document.getElementById("empty-create").addEventListener("click", showCreate);
  document.getElementById("cb-cancel").addEventListener("click", () => show("empty-view"));
  els["create-view"].addEventListener("submit", submitCreate);

  document.querySelectorAll('input[name="onto"]').forEach((radio) =>
    radio.addEventListener("change", () => {
      els["cb-ontology"].hidden = document.querySelector('input[name="onto"]:checked').value !== "custom";
    })
  );

  document.getElementById("add-entity-btn").addEventListener("click", () => {
    els["add-entity-form"].hidden = false;
    els["ae-content"].focus();
  });
  document.getElementById("ae-cancel").addEventListener("click", () => (els["add-entity-form"].hidden = true));
  els["add-entity-form"].addEventListener("submit", submitAddEntity);

  document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

  loadBlocks();
}

document.addEventListener("DOMContentLoaded", init);
