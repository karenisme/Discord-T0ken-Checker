# Karenisme — Discord Token Checker

```
██╗  ██╗ █████╗ ██████╗ ███████╗███╗   ██╗██╗███████╗███╗   ███╗███████╗
██║ ██╔╝██╔══██╗██╔══██╗██╔════╝████╗  ██║██║██╔════╝████╗ ████║██╔════╝
█████╔╝ ███████║██████╔╝█████╗  ██╔██╗ ██║██║███████╗██╔████╔██║█████╗  
██╔═██╗ ██╔══██║██╔══██╗██╔══╝  ██║╚██╗██║██║╚════██║██║╚██╔╝██║██╔══╝  
██║  ██╗██║  ██║██║  ██║███████╗██║ ╚████║██║███████║██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝     ╚═╝╚══════╝
```

> A fast, multi-threaded Discord token checker with proxy support, detailed classification by status, account age, Nitro subscription, and server boosts.

---

## ✨ Features

- ✅ Checks tokens and classifies them as **Valid**, **Invalid**, **Locked**, or **Flagged**
- 🔐 Verification type detection: `unclaimed`, `email verified`, `phone verified`, `fully verified`
- 🎂 Account age sorting by months or years
- 💎 Nitro detection with days remaining
- 🚀 Available server boost slot detection
- 🔄 HTTP proxy support with auto-rotation on rate limit
- ⚡ Multi-threaded for high-speed checking (configurable thread count)
- 🎨 Colorized console output with real-time title bar stats (Windows)
- 📁 Organized output files sorted by type, age, and boost count

---

## 📁 Project Structure

```
├── main.py
├── data/
│   ├── config.toml       # Main configuration (threads, proxyless mode)
│   ├── settings.json     # Feature toggles (flagged, type, age, nitro)
│   ├── tokens.txt        # Input tokens (one per line)
│   └── proxies.txt       # Proxy list (one per line, user:pass@host:port or host:port)
└── output/
    └── YYYY-MM-DD HH-MM-SS/
        ├── valid.txt
        ├── invalid.txt
        ├── locked.txt
        ├── flagged.txt
        ├── email verified.txt
        ├── phone verified.txt
        ├── fully verified.txt
        ├── age/
        │   └── {X months | X years}/
        │       └── {type}.txt
        └── boosts/
            └── {X days}/
                └── {Y boosts}.txt
```

---

## ⚙️ Configuration

### `data/config.toml`

```toml
[main]
threads = 50        # Number of concurrent threads
proxyless = false   # Set to true to run without proxies
```

### `data/settings.json`

```json
{
  "flagged": true,   # Detect and separate flagged accounts
  "type": true,      # Classify by verification type
  "age": true,       # Sort by account age
  "nitro": true      # Detect Nitro subscriptions and boosts
}
```

---

## 📋 Input Format

**`data/tokens.txt`** — One token per line. Supports both raw tokens and `email:password:token` format:

```
mfa.xxxxxxxxxxxxxxxx...
user@email.com:password:xxxxxxxxxxxxxxxx...
```

**`data/proxies.txt`** — One proxy per line:

```
host:port
user:password@host:port
```

---

## 🚀 Installation & Usage

### Requirements

- Python 3.8+

### Install dependencies

```bash
pip install tls-client colorama toml
```

### Run

```bash
python main.py
```

---

## 📊 Console Output

The checker displays real-time colored logs for each token:

| Status | Description |
|--------|-------------|
| `[VALID]` | Token is active and usable |
| `[INVALID]` | Token is expired or incorrect |
| `[LOCKED]` | Account has been locked by Discord |
| `[FLAGGED]` | Account is flagged (spammer flag detected) |
| `[RATE LIMITED]` | Too many requests — proxy rotated automatically |

Each valid token log displays: `token` · `username` · `user ID` · `guild count` · `age` · `nitro` · `boosts`

**Windows title bar** updates in real-time with:
```
Token Checker - Valid: X | Invalid: X | Locked: X | Flagged: X | Remaining: X | Progress: XX.XX% | CPM: X
```

---

## 📤 Output

Results are saved to a timestamped folder under `output/` after each run. Files are automatically created only when tokens of that category are found.

---

## ⚠️ Disclaimer

This tool is provided for **educational purposes only**. Using this tool may violate [Discord's Terms of Service](https://discord.com/terms). The author is not responsible for any misuse or consequences arising from the use of this software. Use at your own risk.

---

## 👤 Author

**fufuyaunn**
- Telegram: [@swllette](https://t.me/swllette)
- Website: [karenhoyoshi.asia](https://karenhoyoshi.asia)
- Discord: `fufuyaunn`
