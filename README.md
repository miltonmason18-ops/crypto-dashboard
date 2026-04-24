# 📈 Crypto Price Dashboard v2.0

Live cryptocurrency tracker with Portfolio Calculator built using Python, Streamlit, and Plotly.

**🔗 Live Demo:** https://crypto-dashboard-pfh5jskkkjjqpwhclvudwg.streamlit.app

![Dashboard Screenshot](screenshot.png)

## ✨ Features

### v2.0 - Portfolio Tracker Update
- **My Portfolio Value**: Input BTC, ETH, SOL holdings → see instant total worth
- **Dual Currency Display**: Real-time portfolio value in USD + Nigerian Naira ₦
- **Visual Asset Breakdown**: Interactive donut chart showing % allocation per coin
- **Live Price Integration**: Auto-updates every 5 minutes from CoinGecko API
- **Smart Caching**: Uses `@st.cache_data` to prevent API rate limits

### v1.0 - Core Dashboard  
- **Multi-Coin Tracking**: Bitcoin, Ethereum, Solana, Dogecoin, Cardano
- **Historical Charts**: 7-90 day price history with interactive Plotly graphs
- **Key Market Metrics**: Current price, 24h % change, Market capitalization
- **Responsive Design**: Works seamlessly on mobile and desktop

## 🛠️ Tech Stack

| Technology | Purpose |
| --- | --- |
| **Python 3.10+** | Core language |
| **Streamlit** | Web app framework & UI components |
| **Plotly Express** | Interactive data visualizations |
| **Pandas** | DataFrame manipulation for API data |
| **Requests** | HTTP calls to CoinGecko API |
| **CoinGecko API** | Free real-time cryptocurrency data |

## 🚀 Run This Project Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/miltonmason18-ops/crypto-dashboard.git
   cd crypto-dashboard
