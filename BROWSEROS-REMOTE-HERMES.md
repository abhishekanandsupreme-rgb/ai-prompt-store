# BrowserOS Remote Hermes — Exact Setup Guide (Windows)

Verified on: **DESKTOP-K9RJFH8**  
BrowserOS version: **0.47.18.0** (Chromium 148.0.7966.97)  
BrowserClaw version: **0.49.5.0** (Chromium 148.0.7988.97)

---

## 1. What "Remote Hermes" means

BrowserOS ships a local HTTP/MCP server. By default it only accepts local connections
and the **Remote Hermes** feature (which lets an external Hermes agent drive the
browser over the network) is disabled.

The server logs confirm the exact gating condition:

```
Remote Hermes disabled: AGENT_RUNNER_JWT_SECRET not set
```

Two things must be true for Remote Hermes to work:

1. `AGENT_RUNNER_JWT_SECRET` must be set in the environment.
2. `flags.allow_remote_in_mcp` must be `true` in `config.json`.

---

## 2. Files inspected (read-only)

| Path | Purpose |
|------|---------|
| `C:\Users\asus\.browseros\server.json` | BrowserOS runtime state (ports, version, install ID) |
| `C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\config.json` | **Primary config** — contains `allow_remote_in_mcp` flag and port mapping |
| `C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\server_config.json` | Alternate/older server config snapshot |
| `C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\browseros-server.log` | Live server log — shows Remote Hermes status |
| `C:\Users\asus\AppData\Local\BrowserClaw\User Data\.browseros\config.json` | BrowserClaw (neo) equivalent config |
| `C:\Users\asus\AppData\Local\BrowserOS\User Data\Default\README` | States settings must not be modified except through BrowserOS APIs |
| `C:\Users\asus\BROWSEROS-AGENT-WIRING.md` | Existing local MCP wiring doc for reference |

---

## 3. Step-by-step setup

### Step A — Enable the config flag

Edit **`C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\config.json`** and change:

```json
"flags": { "allow_remote_in_mcp": false }
```

to:

```json
"flags": { "allow_remote_in_mcp": true }
```

> **Do not edit any other fields.** The README in `User Data\Default\README` warns that
> BrowserOS settings "MUST not be extracted, overwritten or modified except through
> BrowserOS defined APIs." Changing only the documented `allow_remote_in_mcp` flag is
> the minimal, supported surface for this feature.

### Step B — Set the JWT secret

**Exact environment variable name:** `AGENT_RUNNER_JWT_SECRET`

**Where to set it:**  
BrowserOS is a native Windows desktop app launched from a shortcut, not from a shell
that reads `.env`. Set it as a **Windows User Environment Variable** (or Machine variable
if every local user needs it).

1. Open **System Properties** → **Advanced** → **Environment Variables**.
2. Under *User variables for asus* (or *System variables*), click **New**.
3. Variable name: `AGENT_RUNNER_JWT_SECRET`
4. Variable value: a strong random string (see format below).
5. Click OK, then **restart BrowserOS** (the shortcut launcher) so the new env var is
   inherited by the server process.

**Expected JWT secret format:**

Any strong, high-entropy string works. The log only checks for presence, not length or
pattern, but follow standard secret hygiene:

- **Recommended:** 32+ random bytes, base64-encoded.  
  On Windows (PowerShell):
  ```powershell
  [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
  ```
- **Minimum:** 32 random printable characters.
- **Do not** use the example value literally; generate your own.

### Step C — Verify

1. Restart BrowserOS.
2. Open `C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\browseros-server.log`.
3. You should **no longer** see `Remote Hermes disabled: AGENT_RUNNER_JWT_SECRET not set`.
4. The server should still show:
   ```
   HTTP server listening on http://127.0.0.1:9200
   Health endpoint: http://127.0.0.1:9200/system/health
   ```

---

## 4. Current local endpoints (from config + logs)

| Instance | MCP URL | Server | CDP | Proxy |
|----------|---------|--------|-----|-------|
| **BrowserOS** | `http://127.0.0.1:9000/mcp` | `http://127.0.0.1:9200` | 9101 | 9000 |
| **BrowserClaw (neo)** | `http://127.0.0.1:9010/mcp` | `http://127.0.0.1:9210` | 9110 | 9010 |

---

## 5. Security caveats

1. **The server binds to `0.0.0.0`** per the log line `"host":"0.0.0.0"`, which means it is
   reachable from other machines on the same LAN. Restrict access with Windows Firewall
   if you do not need remote network access.

2. **`allow_remote_in_mcp: true` exposes the MCP surface** to whatever can reach the port.
   Keep the `AGENT_RUNNER_JWT_SECRET` secret and rotate it if it ever leaks.

3. **Do not hard-code the secret** in `config.json`, `server.json`, or any file tracked by
   Git. Environment variables are the correct place.

4. **The `.env` files searched under `AppData\Local\BrowserOS` and `AppData\Local\BrowserClaw`
   do not exist**, so do not create one expecting BrowserOS to read it — the native
   launcher does not load `.env` files. Use the Windows Environment Variable UI (or
   `setx`) instead.

5. **Restart required:** Changing the env var or `config.json` only takes effect after a
   full BrowserOS restart (close all windows and relaunch from the Start Menu shortcut).

6. **README warning:** `User Data\Default\README` states BrowserOS settings "MUST not be
   extracted, overwritten or modified except through BrowserOS defined APIs." This guide
   documents the only two supported knobs for Remote Hermes (`allow_remote_in_mcp` and
   `AGENT_RUNNER_JWT_SECRET`); avoid touching other keys in `config.json`.

---

## 6. Quick commands (PowerShell)

```powershell
# Generate a secret
$secret = [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Set user-level env var (persists across logins/reboots)
[System.Environment]::SetEnvironmentVariable('AGENT_RUNNER_JWT_SECRET', $secret, 'User')

# Verify it is stored
[System.Environment]::GetEnvironmentVariable('AGENT_RUNNER_JWT_SECRET', 'User')
```

---

## 7. Summary

| Item | Value |
|------|-------|
| Env var | `AGENT_RUNNER_JWT_SECRET` |
| Set via | Windows Environment Variable (User or Machine scope) |
| Secret format | 32+ random bytes, base64-encoded (or any strong random string ≥32 chars) |
| Config flag | `C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\config.json` → `allow_remote_in_mcp: true` |
| Restart needed | Yes — restart BrowserOS after any change |
| Security | Server binds to `0.0.0.0`; restrict firewall; never commit secret; do not use `.env` |
