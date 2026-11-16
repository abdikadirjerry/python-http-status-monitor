async function fetchDashboard() {
  const res = await fetch("/api/services");
  const data = await res.json();
  renderKPIs(data.metrics);
  renderTable(data.services);
}

function renderKPIs(m) {
  const grid = document.getElementById("kpi-grid");
  const cards = [
    {
      label: "System Availability",
      value: `${m.uptime_pct}%`,
      accent: "text-emerald-600",
    },
    {
      label: "Healthy Endpoints",
      value: `${m.up} / ${m.total}`,
      accent: "text-zinc-900",
    },
    {
      label: "Degraded / Down",
      value: `${m.degraded} / ${m.down}`,
      accent: "text-rose-600",
    },
    {
      label: "Avg Response Time",
      value: `${m.avg_latency} ms`,
      accent: "text-indigo-600",
    },
  ];
  grid.innerHTML = cards
    .map(
      (c) => `
    <div class="bg-white border border-zinc-200 rounded-xl p-4">
      <span class="text-[11px] font-mono uppercase text-zinc-500 block">${c.label}</span>
      <span class="text-2xl font-bold ${c.accent} mt-1 block">${c.value}</span>
    </div>
  `,
    )
    .join("");
}

function renderTable(services) {
  const tbody = document.getElementById("services-body");
  const badges = {
    UP: "bg-emerald-100 text-emerald-800 border-emerald-200",
    DEGRADED: "bg-amber-100 text-amber-800 border-amber-200",
    DOWN: "bg-rose-100 text-rose-800 border-rose-200",
  };
  tbody.innerHTML = services
    .map(
      (s) => `
    <tr class="hover:bg-zinc-50">
      <td class="py-3 px-4">
        <span class="px-2 py-0.5 rounded border text-[10px] font-bold font-mono ${badges[s.status]}">${s.status}</span>
      </td>
      <td class="py-3 px-4 font-semibold">${s.name} <span class="text-[10px] text-zinc-400 ml-1">(${s.category})</span></td>
      <td class="py-3 px-4 font-mono text-zinc-500">${s.url}</td>
      <td class="py-3 px-4 font-mono">${s.latency_ms} ms</td>
      <td class="py-3 px-4 text-zinc-500 font-mono text-[11px]">${s.last_checked}</td>
      <td class="py-3 px-4 text-right">
        <button onclick="removeService('${s.id}')" class="text-rose-600 hover:underline font-semibold">Delete</button>
      </td>
    </tr>
  `,
    )
    .join("");
}

async function handleAdd(e) {
  e.preventDefault();
  const payload = {
    name: document.getElementById("srv-name").value,
    url: document.getElementById("srv-url").value,
    category: document.getElementById("srv-cat").value,
  };
  await fetch("/api/services", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  e.target.reset();
  fetchDashboard();
}

async function removeService(id) {
  await fetch(`/api/services?id=${id}`, { method: "DELETE" });
  fetchDashboard();
}

async function refreshChecks() {
  const btn = document.getElementById("refresh-btn");
  btn.textContent = "Probing Targets...";
  btn.disabled = true;
  await fetch("/api/refresh", { method: "POST" });
  await fetchDashboard();
  btn.textContent = "Run Live Probes";
  btn.disabled = false;
}

fetchDashboard();
