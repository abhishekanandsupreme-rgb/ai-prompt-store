# BrowserOS Neo — Local Setup Summary

**Date:** 2026-08-22  
**Host:** DESKTOP-K9RJFH8  
**Project Root:** `C:\Users\asus\ai-prompt-store`

---

## 1. Installation Status

| Component | Path | Version | Status |
|-----------|------|---------|--------|
| **BrowserOS Neo** (a.k.a. BrowserClaw) | `C:\Users\asus\AppData\Local\BrowserClaw` | BrowserOS 0.49.5.0 / Chromium 148.0.7988.97 | **Installed & Running** |
| BrowserOS Neo Server | `…\BrowserClaw\User Data\.browseros\BrowserClawServer\versions\0.0.44` | `browseros-claw-server.exe` 0.0.44 | **Running** (PID 19048) |
| Legacy BrowserOS | `C:\Users\asus\AppData\Local\BrowserOS` | BrowserOS 0.47.18.0 / Chromium 148.0.7966.97 | **Installed, Not Running** |
| Installer | `C:\Users\asus\Downloads\BrowserOS_neo_installer.exe` | 148.0.7988.97 | Present (not executed during this inspection) |

**Key finding:** BrowserOS Neo is the product distributed as **BrowserClaw**. The `BrowserOS_neo_installer.exe` matches the installed BrowserClaw Chromium version (148.0.7988.97).

---

## 2. Runtime State

### Running Processes
- `browseros-claw-server.exe` — PID **19048**
  - Command: `browseros-claw-server.exe --config="C:\Users\asus\AppData\Local\BrowserClaw\User Data\.browseros\config.json"`
- `chrome.exe` (BrowserClaw) — PID **3296** (+ ~30 other BrowserClaw Chrome processes)
  - Command: `chrome.exe --startup-foreground-launch`
- Google Chrome — multiple processes from `C:\Program Files\Google\Chrome\Application\chrome.exe`

### Legacy BrowserOS
- No `browseros-server.exe` process found.
- `server.lock` is empty.
- Ports **9000**, **9200**, **9101** are **not listening**.

---

## 3. Endpoints

### BrowserOS Neo (BrowserClaw)
| Service | Port | URL | Notes |
|---------|------|-----|-------|
| **MCP (proxy)** | 9010 | `http://127.0.0.1:9010/mcp` | Primary MCP endpoint used by Codex / VSCode / Claude |
| **Server** | 9210 | `http://127.0.0.1:9210` | Backend server; also serves MCP (used by Hermes) |
| CDP | 9110 | — | Chrome DevTools Protocol |
| Health | — | `http://127.0.0.1:9210/system/health` | Server health check |

### Legacy BrowserOS (not running)
| Service | Port | URL | Notes |
|---------|------|-----|-------|
| **MCP (proxy)** | 9000 | `http://127.0.0.1:9000/mcp` | Not currently reachable |
| Server | 9200 | `http://127.0.0.1:9200` | Not currently reachable |
| CDP | 9101 | — | Not currently reachable |

### Shared Manifest
- Path: `C:\Users\asus\.browseros\mcp-manager\manifest.json`
- **Only** registers the legacy `browseros` server at `http://127.0.0.1:9000/mcp`.
- **Does not track** BrowserOS Neo / BrowserClaw.

---

## 4. Client Wiring Status

Verified against actual on-disk configs:

| Client | Config Path | `browseros` (9000) | `browseros-neo` (9010/9210) | Status |
|--------|-------------|-------------------|----------------------------|--------|
| **Codex** | `C:\Users\asus\.codex\config.toml` | ✅ Present | ✅ Present | Fully wired |
| **VSCode** | `C:\Users\asus\AppData\Roaming\Code\User\mcp.json` | ✅ Present | ✅ Present | Fully wired |
| **Claude Code** | `C:\Users\asus\.claude.json` | ❌ Missing | ✅ Present | Partial |
| **Gemini CLI** | `C:\Users\asus\.gemini\config\mcp_config.json` | ❌ Missing | ✅ Present | Partial |
| **Hermes** | `C:\Users\asus\AppData\Local\hermes\config.yaml` | ❌ Missing | ✅ Present (port 9210) | Partial |

> **Note:** Hermes uses port **9210** for `browseros-neo` while Codex/VSCode/Claude use **9010**. Both ports are currently serving MCP.

---

## 5. Remaining Manual Steps

### A. Wire Legacy `browseros` to Missing Clients
These edits add the legacy BrowserOS MCP endpoint (`http://127.0.0.1:9000/mcp`) to clients that only have `browseros-neo`. **Only do this if you intend to run the legacy BrowserOS server.**

1. **Claude Code** — `C:\Users\asus\.claude.json`
   - Add `"browseros": { "url": "http://127.0.0.1:9000/mcp", "type": "http" }` as the first key inside `mcpServers`.

2. **Gemini CLI** — `C:\Users\asus\.gemini\config\mcp_config.json`
   - Add `"browseros": { "serverUrl": "http://127.0.0.1:9000/mcp" }` after the existing `browseros-neo` block.

3. **Hermes** — `C:\Users\asus\AppData\Local\hermes\config.yaml`
   - Add a `browseros:` entry under `mcp_servers:` pointing to `http://127.0.0.1:9000/mcp`.

### B. Start Legacy BrowserOS (If Needed)
If you need the `browseros` (port 9000) endpoint active:
- Launch the legacy BrowserOS browser from `C:\Users\asus\AppData\Local\BrowserOS`.
- The server will bind to 9000/9200/9101 automatically.

### C. Update Shared Manifest (Optional)
If you want the shared `C:\Users\asus\.browseros\mcp-manager\manifest.json` to track BrowserOS Neo:
- Add a `browseros-neo` server entry pointing to `http://127.0.0.1:9010/mcp`.
- This is not required for functionality (clients are already wired directly), but it keeps the manifest in sync with what is actually running.

---

## 6. Quick Health Check

```powershell
# Verify BrowserOS Neo is listening
netstat -ano | findstr "9010\|9210"

# Check BrowserOS Neo server health
curl http://127.0.0.1:9210/system/health

# Verify legacy BrowserOS is NOT running
netstat -ano | findstr "9000\|9200\|9101"
```

---

## 7. Related Docs
- `BROWSEROS-AGENT-WIRING.md` — Detailed per-client wiring guide with exact JSON/YAML snippets.
