# Cipher_Vortex_DDOS
# Cipher_Vortex_DDOS
Cipher Vortex DDOS

## ✨ Features

### 🔥 HTTP Flooding
- Send massive amounts of GET, POST, and HEAD requests.
- Custom headers and random user-agents support.
- Designed to simulate real traffic patterns.

### 💣 UDP Flooding
- Sends a high volume of UDP packets to the target host/port.
- Effective for volumetric stress testing.

### 📡 TCP Flooding
- Opens multiple TCP connections to exhaust server resources.
- Simulates real socket-level traffic.

### ⚡ Ping Test
- Verifies target reachability before initiating an attack.
- Ensures the host is online to avoid wasted operations.

### 🛠 Customizable Parameters
- Control over:
  - Request method (`GET`, `POST`, `UDP`, `TCP`)
  - Target URL or IP
  - Target port
  - Number of threads
  - Delay between requests
  - Duration of the attack

### 📊 Real-Time Feedback
- Displays live statistics:
  - Requests per second (RPS)
  - Success/Error counts
  - Colored logs using `rich`

---

## 🔧 Usage

```bash
git clone https://github.com/Cipher1security/Cipher_Vortex_DDOS.git
cd Cipher_Vortex_DDOS
pip install -r requirements.txt
```
