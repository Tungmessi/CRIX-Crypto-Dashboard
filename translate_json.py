import json

path = "Data_visualization.json"
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'markdown':
        src = "".join(cell['source'])
        
        # 1. 📈 **Phân tích Tương quan
        if "📈 **Phân tích Tương quan (Correlation Matrix):**" in src:
            cell['source'] = [
                "📈 **Correlation Matrix Analysis:**\n",
                "\n",
                "* **Market-wide synchronization:** Most coins (except Stablecoins or special cases like XRP which occasionally diverges due to lawsuits) have a strong positive correlation (dark blue color, coefficient > 0.7). This proves that Crypto is a \"rise together, fall together\" market.\n",
                "* **The BTC - ETH duo:** The correlation between BTC and ETH is usually very high (>0.85), indicating that money flow frequently runs in parallel between these two leading coins.\n",
                "* **Decoupling of small Altcoins:** Certain coins like Dogecoin (DOGE) might have a slightly lower correlation coefficient compared to the rest, as they are heavily influenced by news (news-driven) or social media trends rather than general macroeconomic factors."
            ]
            print("Replaced chunk 1")
            
        # 2. **SỰ DỊCH CHUYỂN DÒNG TIỀN VÀO CÁC HỆ SINH THÁI (AREA CHART)**
        if "**SỰ DỊCH CHUYỂN DÒNG TIỀN VÀO CÁC HỆ SINH THÁI (AREA CHART)**" in src:
            cell['source'] = [
                "**MONEY FLOW SHIFT INTO ECOSYSTEMS (AREA CHART)**"
            ]
            print("Replaced chunk 2")
            
        # 3. 📊 **Phân tích Sự phân bổ dòng tiền (Area Chart):**
        if "📊 **Phân tích Sự phân bổ dòng tiền (Area Chart):**" in src:
            cell['source'] = [
                "📊 **Money Flow Distribution Analysis (Area Chart):**\n",
                "\n",
                "* **Bitcoin Dominance Cycle:** During downtrends or high-risk periods (like late 2022, early 2023), BTC's area usually tends to expand. Money flow takes refuge in the safest asset.\n",
                "* **Altcoin Season:** From mid-2024 to mid-2025, we can see the area of coins like SOL, AVAX, or BNB expanding. This is evidence of profit-taking money flow from BTC/ETH shifting to emerging platform projects in search of higher return on investment (ROI).\n",
                "* **Continuous rotation:** The Area chart allows clear observation of the \"expansion - contraction\" of each asset class over time, realistically recreating the psychological picture of money flow shifting from \"Safe (BTC)\" $\\rightarrow$ \"Bluechip (ETH, BNB)\" $\\rightarrow$ \"High-risk Mid-cap/Meme (SOL, AVAX, DOGE)\"."
            ]
            print("Replaced chunk 3")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Translation completed.")
