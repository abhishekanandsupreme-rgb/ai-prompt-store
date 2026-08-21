# BrowserOS Agent MCP Wiring

Maps local agent/MCP integration files to BrowserOS endpoints and identifies exact edits required.

## Local BrowserOS Endpoints

| Server        | URL                     | Transport |
|---------------|-------------------------|-----------|
| `browseros`   | `http://127.0.0.1:9000/mcp` | HTTP      |
| `browseros-neo` | `http://127.0.0.1:9010/mcp` | HTTP      |

---

## Client Status Summary

| Client        | Config Path                                              | Status   |
|---------------|----------------------------------------------------------|----------|
| **Codex**     | `C:\Users\asus\.codex\config.toml`                       | ✅ Wired |
| **VSCode**    | `C:\Users\asus\AppData\Roaming\Code\User\mcp.json`        | ✅ Wired |
| **Claude**    | `C:\Users\asus\.claude.json`                             | ⚠️ Partial |
| **Gemini**    | `C:\Users\asus\.gemini\config\mcp_config.json`            | ⚠️ Partial |
| **Hermes**    | `C:\Users\asus\AppData\Local\hermes\config.yaml`          | ⚠️ Partial |

---

## 1. Codex — Already Wired

**File:** `C:\Users\asus\.codex\config.toml`

**Current entries (lines 55-59):**
```toml
[mcp_servers.browseros]
url = "http://127.0.0.1:9000/mcp"

[mcp_servers.browseros-neo]
url = "http://127.0.0.1:9010/mcp"
```

**Edits needed:** None. Both `browseros` and `browseros-neo` are already present.

---

## 2. VSCode — Already Wired

**File:** `C:\Users\asus\AppData\Roaming\Code\User\mcp.json`

**Current entries (lines 117-124):**
```json
"browseros": {
  "url": "http://127.0.0.1:9000/mcp",
  "type": "http"
},
"browseros-neo": {
  "url": "http://127.0.0.1:9010/mcp",
  "type": "http"
}
```

**Edits needed:** None. Both `browseros` and `browseros-neo` are already present.

---

## 3. Claude Code — Missing `browseros`

**File:** `C:\Users\asus\.claude.json`

**Current `mcpServers` block (lines 986-998):**
```json
"mcpServers": {
  "browseros-neo": {
    "url": "http://127.0.0.1:9010/mcp",
    "type": "http"
  },
  "omniroute": {
    "type": "http",
    "url": "http://localhost:20128/api/mcp/stream",
    "headers": {
      "Authorization": "Bearer omniroute"
    }
  }
}
```

**Exact edit needed:** Add the `browseros` entry to the `mcpServers` object.

```json
"mcpServers": {
  "browseros": {
    "url": "http://127.0.0.1:9000/mcp",
    "type": "http"
  },
  "browseros-neo": {
    "url": "http://127.0.0.1:9010/mcp",
    "type": "http"
  },
  "omniroute": {
    "type": "http",
    "url": "http://localhost:20128/api/mcp/stream",
    "headers": {
      "Authorization": "Bearer omniroute"
    }
  }
}
```

**Placement:** Insert `"browseros"` as the first key inside `mcpServers` (before `browseros-neo`) for consistency with other clients.

---

## 4. Gemini CLI — Missing `browseros`

**File:** `C:\Users\asus\.gemini\config\mcp_config.json`

**Current content:**
```json
{
  "mcpServers": {
    "browseros-neo": {
      "serverUrl": "http://127.0.0.1:9010/mcp"
    }
  }
}
```

**Exact edit needed:** Add the `browseros` entry.

```json
{
  "mcpServers": {
    "browseros-neo": {
      "serverUrl": "http://127.0.0.1:9010/mcp"
    },
    "browseros": {
      "serverUrl": "http://127.0.0.1:9000/mcp"
    }
  }
}
```

**Placement:** Insert after the existing `browseros-neo` block.

---

## 5. Hermes — Missing `browseros`

**File:** `C:\Users\asus\AppData\Local\hermes\config.yaml`

**Current `mcp_servers` block (lines 204-225):**
```yaml
mcp_servers:
  figma:
    url: https://mcp.figma.com/mcp
    auth: oauth
    enabled: true
  blender:
    command: uvx
    args:
      - blender-mcp==1.6.4
    env:
      DISABLE_TELEMETRY: 'true'
    enabled: true
    tools:
      include:
        - get_scene_info
        - get_object_info
        - get_viewport_screenshot
        - execute_blender_code
  browseros-neo:
    url: http://127.0.0.1:9210/mcp
    timeout: 180
    connect_timeout: 30
```

**Exact edit needed:** Add the `browseros` entry under `mcp_servers`.

```yaml
mcp_servers:
  figma:
    url: https://mcp.figma.com/mcp
    auth: oauth
    enabled: true
  blender:
    command: uvx
    args:
      - blender-mcp==1.6.4
    env:
      DISABLE_TELEMETRY: 'true'
    enabled: true
    tools:
      include:
        - get_scene_info
        - get_object_info
        - get_viewport_screenshot
        - execute_blender_code
  browseros:
    url: http://127.0.0.1:9000/mcp
    timeout: 180
    connect_timeout: 30
  browseros-neo:
    url: http://127.0.0.1:9210/mcp
    timeout: 180
    connect_timeout: 30
```

**Placement:** Insert `browseros` before `browseros-neo`. Note that Hermes already uses port `9210` for `browseros-neo` (vs `9010` used by other clients); keep that existing value unchanged.

---

## Additional Notes

- **BrowserOS Manifest** (`C:\Users\asus\.browseros\mcp-manager\manifest.json`) already declares the canonical `browseros` endpoint at `http://127.0.0.1:9000/mcp` and tracks linked configs for VSCode, Claude Code, and Codex. It does **not** track Hermes or Gemini.
- **`.gemini/settings.json`** (48 lines, 3,476 bytes) contains only `BeforeAgent` / `AfterAgent` / `BeforeTool` / `AfterTool` PowerShell hooks and carries **no MCP server definitions**. The actual Gemini MCP wiring lives in `.gemini/config/mcp_config.json`.
- No config files were modified; this document is read-only reporting.
