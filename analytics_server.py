from __future__ import annotations

import json
import mimetypes
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


import os
import base64

ROOT = Path(__file__).resolve().parent
EVENTS_PATH = ROOT / "dados" / "analytics-events.txt"
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8788))


class AnalyticsHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        return

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self.path = "/index.html"
            return super().do_GET()

        # Protecao por senha no Dashboard e nos Eventos JSON
        if path in ("/dashboard", "/events"):
            auth = self.headers.get("Authorization")
            # Esperamos que o login seja admin:32731138
            expected = "Basic " + base64.b64encode(b"admin:32731138").decode("ascii")
            if auth != expected:
                self.send_response(401)
                self.send_header("WWW-Authenticate", 'Basic realm="Acesso Restrito ao Analytics"')
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Acesso negado. Insira as credenciais de acesso.")
                return

        if path == "/dashboard":
            return self._send_html(dashboard_html())
        if path == "/events":
            return self._send_json(read_events())
        return super().do_GET()

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/track":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length") or "0")
        raw = self.rfile.read(min(length, 256_000))
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self.send_error(400, "Invalid JSON")
            return

        event = {
            "received_at": datetime.now(timezone.utc).isoformat(),
            "ip": self.client_address[0],
            "user_agent": self.headers.get("User-Agent", ""),
            **payload,
        }
        EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with EVENTS_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
        self._send_json({"ok": True})

    def _send_json(self, payload) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def guess_type(self, path: str) -> str:
        guessed = mimetypes.guess_type(path)[0]
        return guessed or super().guess_type(path)


def read_events() -> list[dict]:
    if not EVENTS_PATH.exists():
        return []
    events: list[dict] = []
    for line in EVENTS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events[-2000:]


def dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Berry Up - Analytics Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root { 
      --bg: #f8fafc; --surface: #ffffff; --text: #0f172a; --text-muted: #64748b; 
      --primary: #f97316; --primary-hover: #ea580c; --border: #e2e8f0;
      --success: #10b981; --warning: #f59e0b; --info: #3b82f6;
    }
    * { box-sizing: border-box; }
    body { margin: 0; font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); }
    header { background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; position: sticky; top: 0; z-index: 10; box-shadow: 0 1px 2px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
    header h1 { margin: 0; font-size: 20px; color: var(--primary); display: flex; align-items: center; gap: 8px; }
    .status { display: flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 500; color: var(--success); background: #dcfce7; padding: 4px 10px; border-radius: 12px; }
    .status-dot { width: 8px; height: 8px; background: var(--success); border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
    
    main { padding: 24px; max-width: 1400px; margin: 0 auto; }

    /* Nav Tabs / Filters */
    .filter-nav { display: flex; gap: 12px; margin-bottom: 24px; overflow-x: auto; padding-bottom: 8px; }
    .filter-btn { background: var(--surface); border: 1px solid var(--border); color: var(--text-muted); font-size: 14px; font-weight: 600; padding: 10px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
    .filter-btn:hover { border-color: var(--primary); color: var(--primary); }
    .filter-btn.active { background: var(--primary); color: white; border-color: var(--primary); box-shadow: 0 4px 12px rgba(249, 115, 22, 0.2); }

    /* Focus View Layout (shown when a specific metric is selected) */
    .focus-view { display: none; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 32px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); text-align: center; }
    .focus-view.active { display: block; }
    .focus-big-number { font-size: 64px; font-weight: 800; color: var(--primary); line-height: 1; margin-bottom: 12px; }
    .focus-title { font-size: 20px; font-weight: 600; color: var(--text); margin-bottom: 8px; }
    .focus-desc { font-size: 15px; color: var(--text-muted); max-width: 600px; margin: 0 auto 24px auto; }
    .focus-chart { height: 300px; max-width: 800px; margin: 0 auto; }

    /* Default Grid (shown when "Geral" is active) */
    .general-view { display: block; }
    .general-view.hidden { display: none; }
    
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 24px; }
    .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .kpi-title { font-size: 13px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
    .kpi-value { font-size: 32px; font-weight: 700; color: var(--text); }
    .kpi-trend { font-size: 13px; font-weight: 500; margin-top: 8px; color: var(--text-muted); }
    
    .charts-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 24px; }
    .chart-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; flex-direction: column; }
    .chart-title { font-size: 16px; font-weight: 600; margin: 0 0 16px 0; color: var(--text); }
    .chart-container { position: relative; flex: 1; min-height: 250px; }
    
    /* Session Explorer */
    .explorer { display: grid; grid-template-columns: 350px 1fr; gap: 0; background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; height: 600px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .session-list { border-right: 1px solid var(--border); overflow-y: auto; background: #fdfdfd; }
    .session-list-header { padding: 16px; border-bottom: 1px solid var(--border); background: var(--surface); position: sticky; top: 0; font-weight: 600; z-index: 2; display: flex; justify-content: space-between; align-items: center; }
    .session-item { padding: 16px; border-bottom: 1px solid var(--border); cursor: pointer; transition: background 0.2s; }
    .session-item:hover { background: #f1f5f9; }
    .session-item.active { background: #fff7ed; border-left: 4px solid var(--primary); padding-left: 12px; }
    .session-id { font-weight: 600; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; color: var(--text); font-size: 14px; }
    .session-meta { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-muted); margin-top: 4px; margin-bottom: 8px; }
    .tags { display: flex; gap: 6px; flex-wrap: wrap; }
    .tag { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 12px; display: inline-flex; align-items: center; gap: 4px; }
    .tag.checkout { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .tag.cta { background: #fef9c3; color: #854d0e; border: 1px solid #fef08a; }
    .tag.scroll { background: #e0f2fe; color: #075985; border: 1px solid #bae6fd; }
    
    .timeline-container { padding: 0; overflow-y: auto; background: var(--surface); position: relative; }
    .timeline-header { padding: 16px 24px; border-bottom: 1px solid var(--border); background: rgba(255,255,255,0.9); backdrop-filter: blur(4px); position: sticky; top: 0; z-index: 2; display: flex; justify-content: space-between; align-items: center; }
    .timeline-title { font-weight: 600; font-size: 16px; }
    .timeline-content { padding: 24px; }
    .event-node { display: flex; gap: 16px; margin-bottom: 24px; position: relative; }
    .event-icon { width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2; font-size: 14px; background: #f1f5f9; border: 2px solid #fff; box-shadow: 0 0 0 1px var(--border); flex-shrink: 0; }
    .event-node:not(:last-child) .event-line { position: absolute; left: 15px; top: 32px; bottom: -24px; width: 2px; background: var(--border); z-index: 1; }
    .event-card { flex: 1; background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 12px 16px; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
    .event-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; }
    .event-type { font-weight: 600; font-size: 14px; color: var(--text); display: flex; align-items: center; gap: 6px; }
    .event-time { font-size: 12px; color: var(--text-muted); font-variant-numeric: tabular-nums; }
    .event-details { font-size: 13px; color: var(--text-muted); }
    .event-details strong { color: var(--text); font-weight: 500; }
    
    .icon-page_view { background: #e0f2fe; color: #0284c7; }
    .icon-section_view { background: #f3e8ff; color: #7e22ce; }
    .icon-cta_click { background: #fef9c3; color: #ca8a04; }
    .icon-checkout_click { background: #dcfce7; color: #15803d; }
    .icon-scroll_percent { background: #f1f5f9; color: #475569; }

    .empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-muted); padding: 40px; text-align: center; }
    .empty-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.5; }
  </style>
</head>
<body>
  <header>
    <h1>📈 Berry Up Analytics</h1>
    <div class="status"><div class="status-dot"></div> Capturando eventos ao vivo</div>
  </header>
  
  <main>
    <div class="filter-nav">
      <button class="filter-btn active" onclick="setFilter('all')">Visão Geral</button>
      <button class="filter-btn" onclick="setFilter('checkout')">Funil de Checkout</button>
      <button class="filter-btn" onclick="setFilter('time')">Tempo Médio na Página</button>
      <button class="filter-btn" onclick="setFilter('scroll')">Engajamento (Scroll)</button>
      <button class="filter-btn" onclick="setFilter('cta')">Cliques em CTA</button>
    </div>

    <!-- DYNAMIC FOCUS VIEW -->
    <div id="focus-view" class="focus-view">
      <div class="focus-title" id="focus-title">Métrica</div>
      <div class="focus-big-number" id="focus-big-number">0%</div>
      <div class="focus-desc" id="focus-desc">Descrição da métrica.</div>
      <div class="focus-chart"><canvas id="focusChart"></canvas></div>
    </div>

    <!-- GENERAL OVERVIEW -->
    <div id="general-view" class="general-view">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-title">👥 Total de Sessões</div>
          <div class="kpi-value" id="kpi-sessions">-</div>
          <div class="kpi-trend">Visitantes únicos rastreados</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">🛒 Conversões (Checkout)</div>
          <div class="kpi-value" id="kpi-checkouts">-</div>
          <div class="kpi-trend" id="kpi-conv-rate">Taxa de conversão: -%</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">🖱️ Cliques em CTA</div>
          <div class="kpi-value" id="kpi-ctas">-</div>
          <div class="kpi-trend">Botões de ação clicados</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-title">📜 Engajamento (Scroll)</div>
          <div class="kpi-value" id="kpi-scroll">-</div>
          <div class="kpi-trend">Média de rolagem máxima</div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card">
          <h2 class="chart-title">Distribuição de Eventos</h2>
          <div class="chart-container"><canvas id="eventsChart"></canvas></div>
        </div>
        <div class="chart-card">
          <h2 class="chart-title">Seções Mais Visualizadas</h2>
          <div class="chart-container"><canvas id="sectionsChart"></canvas></div>
        </div>
      </div>
    </div>

    <!-- SESSION EXPLORER -->
    <h3 style="margin-top:32px; color:var(--text); font-size:18px;">Explorador de Jornadas</h3>
    <div class="explorer">
      <div class="session-list">
        <div class="session-list-header">
          <span id="session-list-title">Todas as Sessões</span>
          <span id="session-count" style="font-size: 12px; font-weight: normal; color: var(--text-muted);">-</span>
        </div>
        <div id="sessions-container"></div>
      </div>
      <div class="timeline-container">
        <div class="timeline-header">
          <span class="timeline-title">Jornada do Usuário</span>
          <span id="current-session-id" style="font-family: monospace; font-size: 13px; color: var(--text-muted);"></span>
        </div>
        <div class="timeline-content" id="timeline-container">
          <div class="empty-state">
            <div class="empty-icon">🖱️</div>
            <h3>Selecione uma sessão</h3>
            <p>Clique em uma sessão na lista ao lado para ver a jornada completa do usuário.</p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    let eventsChartInstance = null;
    let sectionsChartInstance = null;
    let focusChartInstance = null;
    let globalSessions = [];
    let currentFilter = 'all';
    let appStats = {};

    async function loadData() {
      try {
        const events = await fetch('/events').then(r => r.json());
        processAndRender(events);
      } catch (e) {
        console.error("Erro ao carregar dados", e);
      }
    }

    function processAndRender(events) {
      if (!events || !events.length) return;

      const sessionsMap = new Map();
      events.forEach(ev => {
        const id = ev.session_id || 'unknown';
        if (!sessionsMap.has(id)) sessionsMap.set(id, []);
        sessionsMap.get(id).push(ev);
      });

      const sessions = Array.from(sessionsMap.entries()).map(([id, evts]) => {
        evts.sort((a,b) => new Date(a.received_at) - new Date(b.received_at));
        const maxScroll = Math.max(0, ...evts.map(e => Number(e.scroll_percent || 0)));
        const duration = Math.max(0, ...evts.map(e => Number(e.active_seconds || 0)));
        const hasCheckout = evts.some(e => e.type === 'checkout_click');
        const hasCta = evts.some(e => e.type === 'cta_click');
        return {
          id, events: evts, firstEventAt: evts[0].received_at, lastEventAt: evts[evts.length - 1].received_at,
          maxScroll, duration, hasCheckout, hasCta
        };
      }).sort((a, b) => new Date(b.lastEventAt) - new Date(a.lastEventAt));

      globalSessions = sessions;

      const checkoutsCount = events.filter(e => e.type === 'checkout_click').length;
      const ctasCount = events.filter(e => e.type === 'cta_click').length;
      const avgScroll = sessions.length ? Math.round(sessions.reduce((acc, s) => acc + s.maxScroll, 0) / sessions.length) : 0;
      const convRate = sessions.length ? ((sessions.filter(s => s.hasCheckout).length / sessions.length) * 100).toFixed(1) : 0;
      const avgTime = sessions.length ? Math.round(sessions.reduce((acc, s) => acc + s.duration, 0) / sessions.length) : 0;

      appStats = {
        totalSessions: sessions.length,
        checkouts: checkoutsCount,
        convRate,
        ctas: ctasCount,
        avgScroll,
        avgTime,
        events
      };

      document.getElementById('kpi-sessions').textContent = sessions.length;
      document.getElementById('kpi-checkouts').textContent = checkoutsCount;
      document.getElementById('kpi-conv-rate').textContent = `Taxa de conversão: ${convRate}%`;
      document.getElementById('kpi-ctas').textContent = ctasCount;
      document.getElementById('kpi-scroll').textContent = `${avgScroll}%`;

      const typeCounts = {};
      const sectionCounts = {};
      events.forEach(e => {
        typeCounts[e.type] = (typeCounts[e.type] || 0) + 1;
        if (e.type === 'section_view' && e.section) {
          sectionCounts[e.section] = (sectionCounts[e.section] || 0) + 1;
        }
      });

      renderGeneralCharts(typeCounts, sectionCounts);
      applyFilter(currentFilter);
    }

    function renderGeneralCharts(typeCounts, sectionCounts) {
      const typeLabels = { 'page_view': 'Page Views', 'section_view': 'Section Views', 'scroll_percent': 'Scrolls', 'cta_click': 'CTA Clicks', 'checkout_click': 'Checkouts' };
      const typeColors = { 'page_view': '#3b82f6', 'section_view': '#8b5cf6', 'scroll_percent': '#94a3b8', 'cta_click': '#eab308', 'checkout_click': '#10b981' };
      
      const labels = Object.keys(typeCounts).map(k => typeLabels[k] || k);
      const data = Object.values(typeCounts);
      const bgColors = Object.keys(typeCounts).map(k => typeColors[k] || '#ccc');

      if (eventsChartInstance) eventsChartInstance.destroy();
      const ctxEvents = document.getElementById('eventsChart').getContext('2d');
      eventsChartInstance = new Chart(ctxEvents, {
        type: 'doughnut',
        data: { labels, datasets: [{ data, backgroundColor: bgColors, borderWidth: 0 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } }, cutout: '70%' }
      });

      const sortedSections = Object.entries(sectionCounts).sort((a,b) => b[1] - a[1]).slice(0, 10);
      if (sectionsChartInstance) sectionsChartInstance.destroy();
      const ctxSections = document.getElementById('sectionsChart').getContext('2d');
      sectionsChartInstance = new Chart(ctxSections, {
        type: 'bar',
        data: { labels: sortedSections.map(s => s[0]), datasets: [{ label: 'Visualizações', data: sortedSections.map(s => s[1]), backgroundColor: '#f97316', borderRadius: 4 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { beginAtZero: true, grid: { display: false } }, y: { grid: { display: false } } } }
      });
    }

    window.setFilter = function(filter) {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      currentFilter = filter;
      applyFilter(filter);
    };

    function applyFilter(filter) {
      const general = document.getElementById('general-view');
      const focus = document.getElementById('focus-view');
      let filteredSessions = [];
      let listTitle = "";

      if (filter === 'all') {
        general.classList.remove('hidden');
        focus.classList.remove('active');
        filteredSessions = globalSessions;
        listTitle = "Todas as Sessões";
      } else {
        general.classList.add('hidden');
        focus.classList.add('active');

        const titleEl = document.getElementById('focus-title');
        const numberEl = document.getElementById('focus-big-number');
        const descEl = document.getElementById('focus-desc');
        const ctx = document.getElementById('focusChart').getContext('2d');
        if(focusChartInstance) focusChartInstance.destroy();

        if (filter === 'checkout') {
          titleEl.textContent = "Porcentagem que Chega no Checkout";
          numberEl.textContent = `${appStats.convRate}%`;
          descEl.textContent = `De ${appStats.totalSessions} sessões totais, ${globalSessions.filter(s=>s.hasCheckout).length} chegaram até o botão de compra.`;
          filteredSessions = globalSessions.filter(s => s.hasCheckout);
          listTitle = "Sessões que fizeram Checkout";
          
          focusChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: ['Visitantes Totais', 'Clicaram em CTA', 'Chegaram no Checkout'],
              datasets: [{ data: [appStats.totalSessions, globalSessions.filter(s=>s.hasCta).length, globalSessions.filter(s=>s.hasCheckout).length], backgroundColor: ['#3b82f6', '#f59e0b', '#10b981'], borderRadius: 6 }]
            },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true } } }
          });
        } 
        else if (filter === 'time') {
          titleEl.textContent = "Tempo Médio na Página";
          numberEl.textContent = `${appStats.avgTime} seg`;
          descEl.textContent = "Tempo médio que os usuários passam explorando a landing page.";
          filteredSessions = globalSessions.sort((a,b) => b.duration - a.duration);
          listTitle = "Sessões por Duração";

          const ranges = {'0-10s':0, '11-30s':0, '31-60s':0, '+60s':0};
          globalSessions.forEach(s => {
            if(s.duration<=10) ranges['0-10s']++;
            else if(s.duration<=30) ranges['11-30s']++;
            else if(s.duration<=60) ranges['31-60s']++;
            else ranges['+60s']++;
          });

          focusChartInstance = new Chart(ctx, {
            type: 'pie',
            data: { labels: Object.keys(ranges), datasets: [{ data: Object.values(ranges), backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981'] }] },
            options: { responsive: true, maintainAspectRatio: false }
          });
        }
        else if (filter === 'scroll') {
          titleEl.textContent = "Engajamento Médio de Scroll";
          numberEl.textContent = `${appStats.avgScroll}%`;
          descEl.textContent = "A média de rolagem máxima da página pelas sessões.";
          filteredSessions = globalSessions.sort((a,b) => b.maxScroll - a.maxScroll);
          listTitle = "Sessões por Profundidade de Scroll";

          const ranges = {'0-25%':0, '26-50%':0, '51-75%':0, '76-100%':0};
          globalSessions.forEach(s => {
            if(s.maxScroll<=25) ranges['0-25%']++;
            else if(s.maxScroll<=50) ranges['26-50%']++;
            else if(s.maxScroll<=75) ranges['51-75%']++;
            else ranges['76-100%']++;
          });

          focusChartInstance = new Chart(ctx, {
            type: 'bar',
            data: { labels: Object.keys(ranges), datasets: [{ label: 'Qtd de Sessões', data: Object.values(ranges), backgroundColor: '#8b5cf6', borderRadius: 4 }] },
            options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
          });
        }
        else if (filter === 'cta') {
          const ctaSessions = globalSessions.filter(s=>s.hasCta);
          const ctaRate = appStats.totalSessions ? ((ctaSessions.length / appStats.totalSessions)*100).toFixed(1) : 0;
          titleEl.textContent = "Taxa de Cliques em CTA";
          numberEl.textContent = `${ctaRate}%`;
          descEl.textContent = `${ctaSessions.length} das ${appStats.totalSessions} sessões clicaram em algum botão de ação na página.`;
          filteredSessions = ctaSessions;
          listTitle = "Sessões que clicaram em CTA";

          const ctaCounts = {};
          appStats.events.forEach(e => {
            if(e.type === 'cta_click' && e.section) { ctaCounts[e.section] = (ctaCounts[e.section] || 0) + 1; }
          });

          focusChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: { labels: Object.keys(ctaCounts), datasets: [{ data: Object.values(ctaCounts), backgroundColor: ['#f97316', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'] }] },
            options: { responsive: true, maintainAspectRatio: false }
          });
        }
      }

      document.getElementById('session-list-title').textContent = listTitle;
      document.getElementById('session-count').textContent = `${filteredSessions.length} total`;
      renderSessionList(filteredSessions);
    }

    function renderSessionList(sessions) {
      const container = document.getElementById('sessions-container');
      if (!sessions.length) {
        container.innerHTML = '<div style="padding: 20px; text-align: center; color: #888;">Nenhuma sessão encontrada.</div>';
        return;
      }
      container.innerHTML = sessions.map((s, idx) => `
        <div class="session-item" data-id="${s.id}" onclick="selectSession('${s.id}')">
          <div class="session-id">${s.id.split('-')[0] || s.id.substring(0,8)}...</div>
          <div class="session-meta">
            <span>${new Date(s.firstEventAt).toLocaleTimeString('pt-BR', {hour:'2-digit', minute:'2-digit'})}</span>
            <span>${s.duration}s ativos</span>
          </div>
          <div class="tags">
            ${s.hasCheckout ? '<span class="tag checkout">🛒 Checkout</span>' : ''}
            ${s.hasCta ? '<span class="tag cta">👆 CTA</span>' : ''}
            ${s.maxScroll > 50 ? `<span class="tag scroll">📜 ${s.maxScroll}%</span>` : ''}
          </div>
        </div>
      `).join('');
      
      // Auto-select first in the new list if exists
      if(sessions.length > 0) selectSession(sessions[0].id);
    }

    window.selectSession = function(id) {
      document.querySelectorAll('.session-item').forEach(el => el.classList.remove('active'));
      const activeEl = document.querySelector(`.session-item[data-id="${id}"]`);
      if (activeEl) activeEl.classList.add('active');
      const session = globalSessions.find(s => s.id === id);
      if (!session) return;
      document.getElementById('current-session-id').textContent = id;
      
      const timeline = document.getElementById('timeline-container');
      const icons = { 'page_view': '👁️', 'section_view': '🎯', 'scroll_percent': '📜', 'cta_click': '👆', 'checkout_click': '🛒' };
      const formatTime = (iso) => new Date(iso).toLocaleTimeString('pt-BR', {hour:'2-digit', minute:'2-digit', second:'2-digit'});

      const groupedEvents = [];
      let lastEv = null;
      session.events.forEach((ev) => {
        const isSameAsLast = lastEv && lastEv.type === ev.type && lastEv.section === ev.section && ev.type !== 'scroll_percent';
        if (isSameAsLast) { groupedEvents[groupedEvents.length - 1].count++; } 
        else { groupedEvents.push({ ...ev, count: 1 }); }
        lastEv = ev;
      });

      timeline.innerHTML = groupedEvents.map(ev => {
        const icon = icons[ev.type] || '📌';
        const typeClass = `icon-${ev.type}`;
        let details = '';
        if (ev.type === 'page_view') details = `Acessou <strong>${ev.path}</strong>`;
        else if (ev.type === 'section_view') details = `Visualizou a seção <strong>${ev.section}</strong>`;
        else if (ev.type === 'scroll_percent') details = `Rolou até <strong>${ev.scroll_percent}%</strong> da página`;
        else if (ev.type === 'cta_click') details = `Clicou no CTA da seção <strong>${ev.section || ev.path}</strong>`;
        else if (ev.type === 'checkout_click') details = `Iniciou o checkout!`;
        const badge = ev.count > 1 ? `<span style="background:#e2e8f0;color:#475569;padding:2px 6px;border-radius:10px;font-size:11px;margin-left:8px;">x${ev.count}</span>` : '';
        
        return `
          <div class="event-node">
            <div class="event-line"></div>
            <div class="event-icon ${typeClass}">${icon}</div>
            <div class="event-card">
              <div class="event-card-header">
                <div class="event-type">${formatType(ev.type)} ${badge}</div>
                <div class="event-time">${formatTime(ev.received_at)}</div>
              </div>
              <div class="event-details">${details}</div>
            </div>
          </div>
        `;
      }).join('');
    };

    function formatType(type) {
      const map = { 'page_view': 'Page View', 'section_view': 'Section View', 'scroll_percent': 'Scroll', 'cta_click': 'Click CTA', 'checkout_click': 'Checkout' };
      return map[type] || type;
    }

    loadData();
    setInterval(loadData, 5000);
  </script>
</body>
</html>"""


if __name__ == "__main__":
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Analytics mock rodando em http://{HOST}:{PORT}")
    print(f"Dashboard: http://{HOST}:{PORT}/dashboard")
    print(f"Eventos: {EVENTS_PATH}")
    ThreadingHTTPServer((HOST, PORT), AnalyticsHandler).serve_forever()
