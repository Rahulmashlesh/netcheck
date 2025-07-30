# NetCheck - Real-time Network Monitor

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, real-time terminal-based network connectivity monitor with beautiful ASCII graphs and detailed statistics.

![NetCheck Demo](https://via.placeholder.com/800x400/1a1a1a/00ff00?text=NetCheck+Demo)

## ✨ Features

- **Real-time monitoring** - 2-second ping intervals for immediate feedback
- **Beautiful ASCII graphs** - 3-minute visual trend display with color coding
- **Multi-timeframe averages** - 1m, 5m, 15m, 30m response time statistics
- **Smart color coding** - Instant visual feedback on connection quality
- **Lightweight** - Minimal resource usage (~2-5MB RAM)
- **15-minute history** - Rolling window of detailed connectivity data
- **Cross-platform** - Works on macOS, Linux, and Windows

## 🎨 Color Legend

- 🟢 **Dark Green** - Excellent (<30ms)
- 🟡 **Yellow** - Good (30-50ms)
- ⚪ **White** - Fair (50-100ms)
- 🔴 **Red** - Slow (100-300ms)
- 🟣 **Magenta** - Very Slow (>300ms)
- ❌ **Red X** - Disconnected

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/netcheck.git
   cd netcheck
   ```

2. **Install dependencies:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run NetCheck:**
   ```bash
   python3 netcheck.py
   ```
4. **Add an alias:**
   ```bash
   #echo "alias netcheck='cd /Users/rahul.ashlesh/netCheck && source venv/bin/activate && python3 netcheck.py'" >> ~/.bashrc
   echo "alias netcheck='cd /Users/rahul.ashlesh/netCheck && source venv/bin/activate && python3 netcheck.py'" >> ~/.zshrc
   ```
## 📊 Sample Output

```
┌─────────────────────────────── NetCheck ───────────────────────────────┐
│ Network Monitor - 14:32:15                                             │
│                                                                         │
│ Status: ✓ Excellent (28ms)  Uptime: 98.2%                             │
│ Averages: 1m:32ms  5m:35ms  15m:38ms  30m:42ms                        │
│                                                                         │
│ Response Time Trend (Last 3 minutes) (25-45ms)                        │
│  45ms ┤                                                                │
│  40ms ┤     ●─●                                                        │
│  35ms ┤   ●─●   ●─●                                                    │
│  30ms ┤ ●─●       ●─●─●                                                │
│  25ms ┤●             ●─●─●                                             │
│       └────────────────────────────────────────────────────────────    │
│        3m ago                                                    now    │
│                                                                         │
│ Legend: ● <30ms  ● 30-50ms  ● 50-100ms  ● 100-300ms  ● >300ms  × Disc │
│                                                                         │
│ Recent: ●●●●●●●●●●●●●●●●●●●● (450 checks)                              │
│                                                                         │
│ Press Ctrl+C to stop                                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## ⚙️ Configuration

Edit `netcheck.py` to customize:

```python
class NetworkMonitor:
    def __init__(self, host="8.8.8.8", interval=2, max_history=450):
        self.host = host          # Target server to ping
        self.interval = interval  # Seconds between checks
        self.max_history = max_history  # Data points to keep
```

### Common Targets
- `8.8.8.8` - Google DNS (default)
- `1.1.1.1` - Cloudflare DNS
- `208.67.222.222` - OpenDNS
- `your-router-ip` - Local network gateway

## 🔧 Usage

- **Start monitoring:** `python3 netcheck.py`
- **Stop monitoring:** Press `Ctrl+C`
- **View final stats:** Displayed automatically on exit

## 📋 Requirements

- Python 3.8+
- ping3==4.0.4
- rich==13.7.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Uses [ping3](https://github.com/kyan001/ping3) for cross-platform ping functionality

## 📞 Support

If you encounter any issues or have questions:
- Open an [issue](https://github.com/rahulmashlesh/netcheck/issues)
- Check existing [discussions](https://github.com/rahulmashlesh/netcheck/discussions)

---

⭐ **Star this repo if you find it useful!**