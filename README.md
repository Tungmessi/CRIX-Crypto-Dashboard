<div align="center">
  <img src="https://img.icons8.com/color/120/000000/bitcoin--v1.png" width="80px"/>
  <h1>CRIX Crypto Market Dashboard 📊</h1>
  <p><i>Visualizing Cryptocurrency Market Data (CRIX Model)</i></p>
</div>

> 🚀 **EXPERIENCE THE LIVE APP HERE:**  
> 👉 **[https://crix-crypto-aaron.streamlit.app/](https://crix-crypto-aaron.streamlit.app/)** 👈  
> *(Tip: Hold **Ctrl** or **middle-click** to open in a new tab)*

<div align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+"></a>
</div>

---

## 🌟 Project Overview
**CRIX Crypto Dashboard** is a project for the **Data Visualization** course. 

This project goes beyond simple data charting by applying financial algorithms to construct the **CRIX (CRyptocurrency IndeX)**. This is a volume-weighted index that reflects the overall growth of the cryptocurrency market. CRIX can be thought of as a crypto-equivalent to traditional market indices like the S&P 500 or VN-Index.

The project involves scraping, cleaning, and processing historical data for 10 popular cryptocurrencies from 2022 to 2026.

### 🪙 Top 10 Analyzed Cryptocurrencies:
- **BTC (Bitcoin)**: The largest cryptocurrency by market cap, often considered "digital gold".
- **ETH (Ethereum)**: The leading blockchain platform for smart contracts and decentralized applications (dApps).
- **BNB (Binance Coin)**: The native ecosystem coin of Binance, one of the world's largest exchanges.
- **SOL (Solana)**: A high-performance blockchain known for fast processing speeds and low transaction costs.
- **XRP (Ripple)**: Developed to facilitate rapid cross-border payments and remittances.
- **ADA (Cardano)**: A blockchain platform focused on peer-reviewed academic research, sustainability, and security.
- **AVAX (Avalanche)**: A highly scalable blockchain platform widely used in the DeFi sector.
- **DOGE (Dogecoin)**: The most famous meme coin with a massive community and high brand recognition.
- **DOT (Polkadot)**: A project focused on interoperability and seamless data exchange between different blockchains.
- **TRX (TRON)**: A blockchain dedicated to digital content sharing and the entertainment industry.

## 💼 Applications

> This product not only displays raw data but also transforms it into valuable insights, supporting users in their analysis and investment decision-making processes.

**Key Insights**

1. **For Analysts / Traders:** The system provides a macro view of the entire market through the CRIX index. Users can identify when capital is flowing strongly into the market (bullish sentiment) or when the market shows signs of decline and caution.
2. **Risk Management:** Instead of just observing price fluctuations, the system calculates advanced metrics like the Sharpe Ratio and 7-day Rolling Volatility. These indicators help investors quantitatively assess the risk levels and investment efficiency of each asset.
3. **Portfolio Allocation:** The system features a correlation matrix among the cryptocurrencies. Through this, investors can discover which coins tend to move together and which diverge, serving as a crucial foundation for building a diversified portfolio that minimizes risk.

## 🚀 Features

| Feature | Analysis & Significance |
|:---:|:---|
| 📈 **CRIX Index (Volume-Weighted)** | Visualizes the CRIX line alongside Moving Averages (MA7, MA20). Captures the market trend far more accurately than just tracking Bitcoin. |
| 🔥 **Correlation Matrix (Heatmap)** | Measures the co-movement of 10 coins using the Pearson correlation coefficient (r). Data is converted to Daily Returns to maximize accuracy. |
| 📊 **Risk-Return Map** | A Scatter Plot comparing the return versus risk of each coin, assisting in identifying assets with high potential returns at acceptable risk levels. |
| 📦 **Liquidity Analysis** | Analyzes weekly trading volumes to spot periods of massive capital inflows. |
| 💡 **Visual Algorithm Explanations** | Integrated expanders that explain the mathematical formulas and calculations behind KPIs like the Sharpe Ratio and Volatility in an easy-to-understand manner. |

---

## 🛠 Tech Stack
- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly (Graph Objects & Express)
- **Web App Framework:** Streamlit
- **Environment:** Jupyter Notebook (For initial EDA)

---

## 💻 Local Installation & Setup

If you want to run the source code directly on your local machine:

**Step 1: Clone the repository**
```bash
git clone https://github.com/Tungmessi/CRIX-Crypto-Dashboard.git
cd CRIX-Crypto-Dashboard
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run the Streamlit app**
```bash
streamlit run app.py
```
*Your browser will automatically open the app at `http://localhost:8501`*

---
*This project was developed for academic purposes and market data analysis research.*
