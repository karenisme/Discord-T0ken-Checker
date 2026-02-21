# 🚀 Discord Token Checker

A fast and multi-threaded token checker for Discord accounts using `tls_client`.

---

## 📌 Features

- ✅ Check token validity (Valid / Invalid / Locked)
- 🚩 Detect flagged accounts
- 💎 Detect Nitro subscriptions and remaining days
- 🚀 High performance with multi-threading
- 🌐 Proxy support (HTTP)
- 📊 Live statistics (CPM, progress, remaining)
- 📁 Automatically sorted output:
  - valid
  - invalid
  - locked
  - flagged
  - categorized by age and boosts

---

## 📂 Project Structure

```
.
├── main.py
├── data/
│   ├── tokens.txt
│   ├── proxies.txt
│   ├── config.toml
│   └── settings.json
└── output/
```

---

## ⚙️ Configuration

### config.toml

```toml
[main]
threads = 10        # number of threads
proxyless = false   # true = no proxy
```

---

### settings.json

```json
{
  "flagged": true,
  "type": true,
  "age": true,
  "nitro": true
}
```

| Option   | Description |
|----------|------------|
| flagged  | Detect flagged accounts |
| type     | Show verification type |
| age      | Sort accounts by age |
| nitro    | Check Nitro and boosts |

---

## 📥 Input Files

### tokens.txt

Supported formats:

```
token
email:password:token
anything:token
```

The tool automatically extracts the token using:
```
split(":")[-1]
```

---

### proxies.txt

Supported formats:

```
ip:port
user:pass@ip:port
```

---

## ▶️ Usage

### 1. Install dependencies

```bash
pip install tls-client colorama toml
```

---

### 2. Run the tool

```bash
python main.py
```

---

## 📊 Example Output

```
[12:00:01] → [VALID] → [FULLY VERIFIED] → token: [abc123]
→ user: [username] → id: [123456789]
→ guilds: [5] → nitro: [30d] → boosts: [2]
```

---

## 📁 Output

Results are saved in:

```
output/YYYY-MM-DD HH-MM-SS/
```

Files include:

- valid.txt
- invalid.txt
- locked.txt
- flagged.txt
- age/
- boosts/

---

## ⚡ Performance

- Multi-threaded using ThreadPoolExecutor
- Automatic retry on:
  - rate limit (429)
  - proxy errors
- Real-time stats:
  - CPM (checks per minute)
  - Progress %
  - Remaining tokens

---

## ⚠️ Notes

- Using proxies is recommended to avoid rate limits
- Duplicate tokens are automatically removed
- Uses unofficial API endpoints (may break in the future)

---

## 🧠 Credits

- Original author: fufuyaunn
- Improvements: logging, formatting, and performance tweaks

---
