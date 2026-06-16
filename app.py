import streamlit as st

import pandas as pd

import numpy as np

import plotly.graph_objects as go

import plotly.express as px

from plotly.subplots import make_subplots



st.set_page_config(page_title="CRIX Crypto Dashboard", page_icon="₿",

                   layout="wide", initial_sidebar_state="expanded")



def hex_to_rgba(hex_color: str, alpha: float = 0.15) -> str:

    h = hex_color.lstrip("#")

    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)

    return f"rgba({r},{g},{b},{alpha})"



COIN_COLORS = {

    "btc":"#F7931A","eth":"#627EEA","bnb":"#F3BA2F","sol":"#9945FF",

    "xrp":"#00AAE4","ada":"#0033AD","avax":"#E84142","doge":"#C3A634",

    "dot":"#E6007A","trx":"#FF4444",

}

COIN_NAMES = {

    "btc":"Bitcoin","eth":"Ethereum","bnb":"BNB","sol":"Solana",

    "xrp":"XRP","ada":"Cardano","avax":"Avalanche","doge":"Dogecoin",

    "dot":"Polkadot","trx":"TRON",

}

BG="#0D1117"; CARD="#161B22"; BORDER="#30363D"; TEXT="#E6EDF3"

ACCENT="#00d2ff"; GREEN="#3FB950"; RED="#F85149"



st.markdown(f"""

<style>

  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html,body,[class*="css"]{{font-family:'Inter',sans-serif;background:{BG};color:{TEXT};}}

  .stApp{{background:{BG};}}

  section[data-testid="stSidebar"]{{background:linear-gradient(180deg,#0f1923 0%,{CARD} 100%);border-right:1px solid {BORDER};}}

  .kpi-card{{background:{CARD};border:1px solid {BORDER};border-radius:14px;padding:18px 12px;text-align:center;transition:transform .2s,box-shadow .2s;}}

  .kpi-card:hover{{transform:translateY(-4px);box-shadow:0 8px 32px rgba(0,210,255,.12);}}

  .kpi-label{{font-size:10px;color:#8B949E;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px;}}

  .kpi-value{{font-size:24px;font-weight:800;color:{TEXT};}}

  .kpi-pos{{color:{GREEN};font-size:12px;margin-top:4px;}}

  .kpi-neg{{color:{RED};font-size:12px;margin-top:4px;}}

  .sh{{font-size:16px;font-weight:700;color:{ACCENT};border-left:3px solid {ACCENT};padding-left:10px;margin:18px 0 10px;}}

  .coin-row{{background:{CARD};border:1px solid {BORDER};border-radius:9px;padding:9px 13px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;}}

  .stTabs [data-baseweb="tab-list"]{{gap:4px;background:{CARD};border-radius:10px;padding:4px;border:1px solid {BORDER};}}

  .stTabs [data-baseweb="tab"]{{height:38px;border-radius:8px;color:#8B949E;font-weight:500;font-size:13px;}}

  .stTabs [aria-selected="true"]{{background:rgba(0,210,255,.12)!important;color:{ACCENT}!important;font-weight:600!important;}}

  .insight{{background:rgba(0,210,255,.06);border:1px solid rgba(0,210,255,.2);border-radius:10px;padding:12px 16px;font-size:13px;color:{TEXT};margin:8px 0;}}

  .insight b{{color:{ACCENT};}}

</style>

""", unsafe_allow_html=True)



def base_layout(**kw):

    cfg = dict(

        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(22,27,34,0.6)",

        font=dict(color=TEXT, family="Inter"),

        margin=dict(l=50,r=30,t=55,b=45),

        xaxis=dict(gridcolor=BORDER,showgrid=True,gridwidth=.5,zeroline=False),

        yaxis=dict(gridcolor=BORDER,showgrid=True,gridwidth=.5,zeroline=False),

    )

    cfg.update(kw)

    return cfg



@st.cache_data

def load_data(path="crypto_2026_clean.csv"):

    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])

    df.set_index("Date", inplace=True)

    vol_cols   = [c for c in df.columns if "vol"   in c]

    price_cols = [c for c in df.columns if "price" in c]

    df["Total_Volume"] = df[vol_cols].sum(axis=1)

    returns = df[price_cols].pct_change().fillna(0)

    w_ret = pd.Series(0.0, index=returns.index)

    for vc in vol_cols:

        pc = vc.replace("vol_M","price")

        w_ret += (df[vc]/df["Total_Volume"]) * returns[pc]

    crix = [1000.0]

    for r in w_ret.iloc[1:]:

        crix.append(crix[-1]*(1+r))

    df["CRIX"] = crix

    for pc in price_cols:

        c = pc.replace("_price","")

        df[f"{c}_cum_ret"]   = (df[pc]/df[pc].iloc[0]-1)*100

        df[f"{c}_daily_ret"] = df[pc].pct_change()*100

    return df, price_cols, vol_cols



df, price_cols, vol_cols = load_data("crypto_2026_clean.csv")

coins = [c.replace("_price","") for c in price_cols]



# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    lang = st.radio("🌐 Language / Ngôn ngữ", ["EN 🇬🇧", "VN 🇻🇳"], horizontal=True)
    is_vn = lang == "VN 🇻🇳"
    def t(vn, en): return vn if is_vn else en

    st.markdown(f"<div style='text-align:center;padding:14px 0 22px'><div style='font-size:40px'>₿</div><div style='font-size:17px;font-weight:800;color:{ACCENT}'>CRIX Dashboard</div><div style='font-size:11px;color:#8B949E;margin-top:3px'>Crypto Market Analytics </div></div>",unsafe_allow_html=True)
    st.markdown(t("### 🎛️ Bộ lọc", "### 🎛️ Filters"))
    date_range = st.date_input(t("Khoảng thời gian", "Date Range"),
        value=(df.index.min().date(), df.index.max().date()),
        min_value=df.index.min().date(), max_value=df.index.max().date())
    selected_coins = st.multiselect(t("Chọn đồng coin", "Select Coins"), options=coins,
        default=["btc","eth","bnb","sol","xrp"],
        format_func=lambda c: f"{COIN_NAMES[c]} ({c.upper()})")
    if not selected_coins:
        selected_coins = ["btc","eth","bnb"]
    st.markdown("---")
    info_text = "📅 01/05/2022 – 01/05/2026<br>📊 Mô hình: CRIX (Volume-Weighted)<br>🏫 Môn: Trực quan hóa dữ liệu<br>🐍 Python · Streamlit · Plotly" if is_vn else "📅 05/01/2022 – 05/01/2026<br>📊 Model: CRIX (Volume-Weighted)<br>🏫 Course: Data Visualization<br>🐍 Python · Streamlit · Plotly"
    st.markdown(f"<div style='font-size:11px;color:#8B949E;line-height:1.7'>{info_text}</div>",unsafe_allow_html=True)

if len(date_range)==2:
    s,e = pd.Timestamp(date_range[0]),pd.Timestamp(date_range[1])
else:
    s,e = df.index.min(),df.index.max()
dff = df.loc[s:e].copy()

# ── HEADER ────────────────────────────────────
header_title = "Trực quan hóa chỉ số thị trường Tiền Mã Hóa" if is_vn else "Cryptocurrency Market Index Visualization"
header_sub = "📈 Mô hình <b style=\"color:{ACCENT}\">CRIX (CRyptocurrency IndeX)</b> — Phân tích xu hướng dòng tiền &nbsp;|&nbsp; 10 đồng coin hàng đầu &nbsp;|&nbsp;" if is_vn else "📈 <b style=\"color:{ACCENT}\">CRIX (CRyptocurrency IndeX)</b> Model — Money Flow Trend Analysis &nbsp;|&nbsp; Top 10 Coins &nbsp;|&nbsp;"

st.markdown(f"""<div style='background:linear-gradient(135deg,#0D1117 0%,#1a2332 100%);border:1px solid {BORDER};border-radius:16px;padding:26px 30px;margin-bottom:20px;box-shadow:0 4px 40px rgba(0,210,255,.07)'>
<div style='font-size:26px;font-weight:800;background:linear-gradient(90deg,{ACCENT},{ACCENT}77);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:5px'>{header_title}</div>
<div style='color:#8B949E;font-size:13px'>{header_sub}</div></div>""",unsafe_allow_html=True)



# ── KPIs ─────────────────────────────────────

crix_now=dff["CRIX"].iloc[-1]; crix_start=dff["CRIX"].iloc[0]

crix_chg=(crix_now/crix_start-1)*100

crix_max=dff["CRIX"].max(); crix_min=dff["CRIX"].min()

vol_avg=dff["Total_Volume"].mean()

vol_peak=dff["Total_Volume"].idxmax().strftime("%d/%m")

# Daily return của CRIX

crix_d = dff["CRIX"].pct_change().dropna()



# Risk-free rate (crypto -> giả định 0%)

risk_free = 0.0



# Annualization cho crypto (365 ngày)

TRADING_DAYS = 365



# Annual return và annual volatility

annual_return = crix_d.mean() * TRADING_DAYS

annual_vol = crix_d.std() * np.sqrt(TRADING_DAYS)



# Sharpe Ratio

sharpe = (

    (annual_return - risk_free) / annual_vol

    if annual_vol != 0

    else 0

)



def kpi(label,val,delta=None,suffix=""):

    d=""

    if delta is not None:

        cls="kpi-pos" if delta>=0 else "kpi-neg"

        arr="▲" if delta>=0 else "▼"

        d=f'<div class="{cls}">{arr} {abs(delta):.2f}%</div>'

    return f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{val}{suffix}</div>{d}</div>'



c1,c2,c3,c4,c5,c6=st.columns(6)
c1.markdown(kpi(t("CRIX Hiện tại", "Current CRIX"),f"{crix_now:,.0f}",crix_chg),unsafe_allow_html=True)
c2.markdown(kpi(t("CRIX Cao nhất", "Highest CRIX"),f"{crix_max:,.0f}"),unsafe_allow_html=True)
c3.markdown(kpi(t("CRIX Thấp nhất", "Lowest CRIX"),f"{crix_min:,.0f}"),unsafe_allow_html=True)
c4.markdown(kpi(t("Volume TB/ngày", "Avg Vol/Day"),f"{vol_avg:,.0f}",suffix=" M$"),unsafe_allow_html=True)
c5.markdown(kpi(t("Ngày cao trào", "Peak Volume Day"),vol_peak),unsafe_allow_html=True)
c6.markdown(kpi("Sharpe Ratio",f"{sharpe:.2f}"),unsafe_allow_html=True)
st.markdown("<br>",unsafe_allow_html=True)



# ── SHARPE RATIO BREAKDOWN ───────────────────
sh_text = "Giải thích Sharpe Ratio (CRIX)" if is_vn else "Sharpe Ratio Breakdown (CRIX)"
st.markdown(f'<div class="sh">{sh_text}</div>',unsafe_allow_html=True)



col_s1, col_s2, col_s3, col_s4 = st.columns(4)



col_s1.markdown(kpi(t("Mean Return/ngày", "Daily Mean Return"), f"{crix_d.mean()*100:.3f}", suffix="%"), unsafe_allow_html=True)



col_s2.markdown(kpi(t("Volatility/ngày", "Daily Volatility"), f"{crix_d.std()*100:.3f}", suffix="%"), unsafe_allow_html=True)



col_s3.markdown(

    kpi(

        "Annual Return",

        f"{annual_return*100:.2f}",

        suffix="%"

    ),

    unsafe_allow_html=True

)



col_s4.markdown(

    kpi(

        "Annual Volatility",

        f"{annual_vol*100:.2f}",

        suffix="%"

    ),

    unsafe_allow_html=True

)

daily_vol = crix_d.std()

daily_vol_pct = daily_vol * 100



# Lấy 3 ngày cuối cùng làm ví dụ minh họa

last_3_dates = crix_d.index[-3:]

r1, r2, r3 = crix_d.iloc[-3:] * 100

avg_3 = (r1 + r2 + r3) / 3



# Tính Volatility cho 3 ngày (Phương sai mẫu n-1)

var_3 = ((r1 - avg_3)**2 + (r2 - avg_3)**2 + (r3 - avg_3)**2) / 2

std_3 = np.sqrt(var_3)



with st.expander(t("Giải thích chi tiết và các bước tính toán KPI", "Detailed Explanation and KPI Calculation Steps")):
    if is_vn:
        st.markdown(f"""
        **1. Volume TB/ngày:** Khối lượng giao dịch trung bình mỗi ngày của toàn bộ 10 đồng coin trong khoảng thời gian được chọn.
        - Công thức: Trung bình cộng(Volume BTC + Volume ETH + ...) = **{vol_avg:,.0f} M$**
        
        **2. Mean Return/ngày:** Lợi suất sinh lời trung bình mỗi ngày của chỉ số CRIX.
        - Ví dụ 3 ngày cuối: `{r1:.2f}%`, `{r2:.2f}%`, `{r3:.2f}%`. Trung bình = **{avg_3:.2f}%**.
        - Thực tế trên toàn bộ dữ liệu: **{crix_d.mean()*100:.3f}%**
        
        **3. Volatility/ngày:** Mức độ rủi ro (độ lệch chuẩn) của lợi suất hàng ngày.
        - Ví dụ 3 ngày cuối: Độ rủi ro là {std_3:.2f}%.
        - Thực tế trên toàn bộ dữ liệu: **{daily_vol_pct:.3f}%**.
        
        **4. Sharpe Ratio (Quy năm):** Hiệu quả đầu tư (Lợi suất trên mỗi 1 đơn vị rủi ro).
        - Công thức: `(Mean Return × 365) / (Volatility × √365)` = **{sharpe:.2f}**
        """)
    else:
        st.markdown(f"""
        **1. Avg Vol/Day:** Average daily trading volume of all 10 coins in the selected period.
        - Formula: Average(Volume BTC + Volume ETH + ...) = **{vol_avg:,.0f} M$**
        
        **2. Daily Mean Return:** Average daily return of the CRIX index.
        - Example last 3 days: `{r1:.2f}%`, `{r2:.2f}%`, `{r3:.2f}%`. Average = **{avg_3:.2f}%**.
        - Actual on full data: **{crix_d.mean()*100:.3f}%**
        
        **3. Daily Volatility:** The risk level (standard deviation) of daily returns.
        - Example last 3 days: Risk is {std_3:.2f}%.
        - Actual on full data: **{daily_vol_pct:.3f}%**.
        
        **4. Sharpe Ratio (Annualized):** Investment efficiency (Return per unit of risk).
        - Formula: `(Mean Return × 365) / (Volatility × √365)` = **{sharpe:.2f}**
        """)



tab_names = ["📈 Chỉ số CRIX", "💰 Giá coin", "📦 Khối lượng", "🔥 Tương quan", "📊 Lợi suất & Rủi ro", "🥧 Thị phần"] if is_vn else ["📈 CRIX Index", "💰 Prices", "📦 Volume", "🔥 Correlation", "📊 Risk & Return", "🥧 Market Share"]
t1,t2,t3,t4,t5,t6 = st.tabs(tab_names)



# ════ TAB 1 ═══════════════════════════════════

with t1:
    sh_crix = "Diễn biến chỉ số CRIX (Volume-Weighted)" if is_vn else "CRIX Index Trend (Volume-Weighted)"
    st.markdown(f'<div class="sh">{sh_crix}</div>',unsafe_allow_html=True)
    ma7=dff["CRIX"].rolling(7).mean(); ma20=dff["CRIX"].rolling(20).mean()
    idx_max=dff["CRIX"].idxmax(); idx_min=dff["CRIX"].idxmin()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=dff.index,y=dff["CRIX"],fill="tozeroy",
        fillcolor=hex_to_rgba(ACCENT,0.07),line=dict(color=ACCENT,width=2.5),name="CRIX Index",
        hovertemplate="<b>%{x|%d/%m/%Y}</b><br>CRIX: <b>%{y:.2f}</b><extra></extra>"))
    fig.add_trace(go.Scatter(x=dff.index,y=ma7,line=dict(color="#F7931A",width=1.8,dash="dash"),name="MA 7"))
    fig.add_trace(go.Scatter(x=dff.index,y=ma20,line=dict(color="#9945FF",width=1.8,dash="dot"),name="MA 20"))
    
    t_peak = "Đỉnh" if is_vn else "Peak"
    t_btm = "Đáy" if is_vn else "Bottom"
    fig.add_annotation(x=idx_max,y=dff["CRIX"].max(),text=f"▲ {t_peak}: {dff['CRIX'].max():.0f}",
        showarrow=True,arrowhead=2,arrowcolor=GREEN,font=dict(color=GREEN,size=12),ay=-44,ax=0)
    fig.add_annotation(x=idx_min,y=dff["CRIX"].min(),text=f"▼ {t_btm}: {dff['CRIX'].min():.0f}",
        showarrow=True,arrowhead=2,arrowcolor=RED,font=dict(color=RED,size=12),ay=44,ax=0)
    
    chart_title = "<b>Chỉ số CRIX — Thị trường tiền mã hóa</b>" if is_vn else "<b>CRIX Index — Cryptocurrency Market</b>"
    fig.update_layout(**base_layout(title=dict(text=chart_title,font=dict(size=15)),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),height=420,hovermode="x unified"))

    st.plotly_chart(fig,use_container_width=True)

    last_date = dff.index[-1].strftime('%d/%m/%Y')
    last_crix = dff["CRIX"].iloc[-1]
    ma7_val = dff["CRIX"].rolling(7).mean().iloc[-1]

    with st.expander(t("Xem thuật toán và công thức tính biểu đồ này", "View Algorithm and Calculation Formula")):
        if is_vn:
            st.markdown(f"""
            **1. Chỉ số CRIX (Volume-Weighted):** Tính lợi suất của từng đồng coin, nhân với trọng số khối lượng giao dịch tương ứng, sau đó cộng dồn vào giá trị CRIX của ngày hôm trước.
            **2. Đường MA7 và MA20:**
            - **MA7:** Cộng điểm CRIX 7 ngày gần nhất rồi chia 7.
            - **MA20:** Cộng điểm CRIX 20 ngày gần nhất rồi chia 20.
            **Ví dụ cụ thể ngày {last_date}:**
            Điểm CRIX hiện tại là **{last_crix:,.0f}**. 
            Đường MA7 nằm ở mốc **{ma7_val:,.0f}**.
            """)
        else:
            st.markdown(f"""
            **1. CRIX Index (Volume-Weighted):** Calculate the return of each coin, multiply by its volume weight, then accumulate into the previous day's CRIX value.
            **2. MA7 and MA20 Lines:**
            - **MA7:** Average of the last 7 days.
            - **MA20:** Average of the last 20 days.
            **Example for {last_date}:**
            Current CRIX is **{last_crix:,.0f}**. 
            MA7 line is at **{ma7_val:,.0f}**.
            """)



    st.markdown(f'<div class="sh">{t("Biến động CRIX theo ngày (%)", "Daily CRIX Volatility (%)")}</div>',unsafe_allow_html=True)
    d_chg=dff["CRIX"].pct_change()*100
    fig2=go.Figure(go.Bar(x=dff.index,y=d_chg,
        marker_color=[GREEN if v>=0 else RED for v in d_chg],
        hovertemplate="<b>%{x|%d/%m}</b><br>%{y:.2f}%<extra></extra>"))
    fig2.add_hline(y=0,line_color="#8B949E",line_width=0.8)
    
    ct2 = "<b>Thay đổi CRIX hàng ngày (%)</b>" if is_vn else "<b>Daily CRIX Change (%)</b>"
    yt2 = "% thay đổi" if is_vn else "% change"
    fig2.update_layout(**base_layout(height=240,title=dict(text=ct2,font=dict(size=14)),yaxis_title=yt2))

    st.plotly_chart(fig2,use_container_width=True)



    up_d=int((d_chg>0).sum()); dn_d=int((d_chg<0).sum())
    best=d_chg.idxmax().strftime("%d/%m"); worst=d_chg.idxmin().strftime("%d/%m")
    
    if is_vn:
        t_insight = f'📌 <b>Insight:</b> CRIX có <b>{up_d} ngày tăng</b> và <b>{dn_d} ngày giảm</b>. Ngày tăng mạnh nhất: <b>{best}</b> (+{d_chg.max():.2f}%), ngày giảm mạnh nhất: <b>{worst}</b> ({d_chg.min():.2f}%). CRIX tổng thể {"giảm" if crix_chg<0 else "tăng"} <b>{abs(crix_chg):.1f}%</b> so với đầu kỳ.'
    else:
        t_insight = f'📌 <b>Insight:</b> CRIX had <b>{up_d} up days</b> and <b>{dn_d} down days</b>. Best day: <b>{best}</b> (+{d_chg.max():.2f}%), worst day: <b>{worst}</b> ({d_chg.min():.2f}%). CRIX overall {"decreased" if crix_chg<0 else "increased"} by <b>{abs(crix_chg):.1f}%</b> from the start.'
    st.markdown(f'<div class="insight">{t_insight}</div>',unsafe_allow_html=True)

    with st.expander(t("Cách tính biểu đồ biến động hàng ngày", "How to calculate daily volatility chart")):
        if is_vn:
            st.markdown(f"""
            Biểu đồ đo lường sự tăng trưởng của chỉ số CRIX so với ngày trước.
            - **Cách tính:** `(CRIX hôm nay / CRIX hôm qua - 1) * 100`.
            - Tổng cộng có **{up_d} ngày** sinh lời dương (xanh) và **{dn_d} ngày** sinh lời âm (đỏ).
            - Đỉnh cao nhất là **+{d_chg.max():.2f}%** và thấp nhất là **{d_chg.min():.2f}%**.
            """)
        else:
            st.markdown(f"""
            This chart measures the growth of the CRIX index compared to the previous day.
            - **Formula:** `(CRIX today / CRIX yesterday - 1) * 100`.
            - Total of **{up_d} days** with positive return (green) and **{dn_d} days** with negative return (red).
            - Highest peak is **+{d_chg.max():.2f}%** and lowest is **{d_chg.min():.2f}%**.
            """)



# ════ TAB 2 ═══════════════════════════════════

with t2:

    col_a,col_b=st.columns([2.2,1])

    with col_a:
        st.markdown(f'<div class="sh">{t("Diễn biến giá theo thời gian", "Price Trend over Time")}</div>',unsafe_allow_html=True)
        v_opts = ["Giá tuyệt đối (USD)","Lợi suất tích lũy (%)"] if is_vn else ["Absolute Price (USD)", "Cumulative Return (%)"]
        view=st.radio(t("Chế độ xem", "View Mode"),v_opts,horizontal=True,key="pv")
        fig3=go.Figure()
        for coin in selected_coins:
            yc=f"{coin}_price" if view in ["Giá tuyệt đối (USD)", "Absolute Price (USD)"] else f"{coin}_cum_ret"
            fig3.add_trace(go.Scatter(x=dff.index,y=dff[yc],name=f"{COIN_NAMES[coin]} ({coin.upper()})",
                line=dict(color=COIN_COLORS[coin],width=2),
                hovertemplate=f"<b>{coin.upper()}</b> %{{x|%d/%m}}<br>%{{y:,.2f}}<extra></extra>"))
        if view in ["Lợi suất tích lũy (%)", "Cumulative Return (%)"]:
            fig3.add_hline(y=0,line_dash="dash",line_color="#8B949E",line_width=0.8)
        yt3 = "Giá (USD)" if view in ["Giá tuyệt đối (USD)", "Absolute Price (USD)"] else "Lợi suất (%)" if is_vn else "Return (%)"
        fig3.update_layout(**base_layout(height=400,
            title=dict(text=f"<b>{view}</b>",font=dict(size=14)),
            yaxis_title="Price (USD)" if view == "Absolute Price (USD)" else yt3,
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0),hovermode="x unified"))
        st.plotly_chart(fig3,use_container_width=True)

        with st.expander(t("Thuật toán hiển thị diễn biến giá", "Price Trend Algorithm")):
            if is_vn:
                st.markdown("""
                - **Giá tuyệt đối (USD):** Trích xuất trực tiếp giá đóng cửa hàng ngày.
                - **Lợi suất tích lũy (%):** Chọn ngày đầu tiên làm mốc 0%. Các ngày tiếp theo tính bằng: `(Giá hiện tại / Giá ngày đầu - 1) * 100`.
                """)
            else:
                st.markdown("""
                - **Absolute Price (USD):** Extracted directly from daily closing prices.
                - **Cumulative Return (%):** First day is 0%. Subsequent days calculated as: `(Current Price / First Day Price - 1) * 100`.
                """)

        st.markdown(f'<div class="sh">{t("Candlestick BTC (giả lập từ giá đóng cửa)", "BTC Candlestick (Simulated from Close)")}</div>',unsafe_allow_html=True)
        btc=dff[["btc_price"]].copy()
        btc["open"]=btc["btc_price"].shift(1).fillna(btc["btc_price"])
        btc["high"]=btc[["btc_price","open"]].max(axis=1)*1.003
        btc["low"]=btc[["btc_price","open"]].min(axis=1)*0.997
        figc=go.Figure(go.Candlestick(x=btc.index,open=btc["open"],high=btc["high"],
            low=btc["low"],close=btc["btc_price"],
            increasing_line_color=GREEN,decreasing_line_color=RED,name="BTC"))
        figc.update_layout(**base_layout(height=300,
            title=dict(text="<b>BTC — Candlestick Chart</b>",font=dict(size=14)),
            yaxis_title=t("Giá USD", "Price USD"),xaxis_rangeslider_visible=False))
        st.plotly_chart(figc,use_container_width=True)

        btc_last_date = btc.index[-1].strftime('%d/%m/%Y')
        btc_c = btc["btc_price"].iloc[-1]
        btc_o = btc["open"].iloc[-1]
        btc_h = btc["high"].iloc[-1]
        btc_l = btc["low"].iloc[-1]

        with st.expander(t("Giải thích nguồn dữ liệu và công thức", "Data Source and Formula Explanation")):
            if is_vn:
                st.markdown(f"""
                **Xử lý dữ liệu:** Chỉ có giá Close. Nến được **giả lập** từ giá Close.
                **Ví dụ ngày {btc_last_date}:**
                - **Đóng cửa:** {btc_c:,.0f} USD
                - **Mở cửa:** Giá hôm trước = **{btc_o:,.0f} USD**
                - **Cao nhất:** Max(Open, Close) + 0.3% = **{btc_h:,.0f} USD**
                - **Thấp nhất:** Min(Open, Close) - 0.3% = **{btc_l:,.0f} USD**""")
            else:
                st.markdown(f"""
                **Data Processing:** Only Close price is available. Candles are **simulated**.
                **Example for {btc_last_date}:**
                - **Close:** {btc_c:,.0f} USD
                - **Open:** Previous day price = **{btc_o:,.0f} USD**
                - **High:** Max(Open, Close) + 0.3% = **{btc_h:,.0f} USD**
                - **Low:** Min(Open, Close) - 0.3% = **{btc_l:,.0f} USD**""")



    with col_b:
        st.markdown(f'<div class="sh">{t("Bảng giá cuối kỳ", "End of Period Prices")}</div>',unsafe_allow_html=True)
        rows=[{"coin":c,"price":dff[f"{c}_price"].iloc[-1],"chg":(dff[f"{c}_price"].iloc[-1]/dff[f"{c}_price"].iloc[0]-1)*100} for c in coins]
        rows.sort(key=lambda x:x["chg"],reverse=True)
        for r in rows:
            c=r["coin"]; color=GREEN if r["chg"]>=0 else RED; arr="▲" if r["chg"]>=0 else "▼"
            fp=f"${r['price']:,.0f}" if r['price']>1 else f"${r['price']:.4f}"
            st.markdown(f'<div class="coin-row"><div><span style="font-weight:700;color:{COIN_COLORS[c]};font-size:14px">{c.upper()}</span><span style="color:#8B949E;font-size:11px;margin-left:5px">{COIN_NAMES[c]}</span></div><div style="text-align:right"><div style="font-weight:600;font-size:13px">{fp}</div><div style="color:{color};font-size:12px">{arr} {abs(r["chg"]):.1f}%</div></div></div>',unsafe_allow_html=True)

        with st.expander(t("Công thức xếp hạng", "Ranking Formula")):
            if is_vn:
                st.markdown("""
                Bảng này tự động sắp xếp theo **Tỷ lệ tăng trưởng** từ cao xuống thấp.
                - **Công thức:** `(Giá ngày cuối / Giá ngày đầu - 1) * 100`.
                """)
            else:
                st.markdown("""
                This table automatically sorts coins by **Growth Rate** from highest to lowest.
                - **Formula:** `(Last Day Price / First Day Price - 1) * 100`.
                """)



# ════ TAB 3 ═══════════════════════════════════

with t3:



    col3a,col3b=st.columns(2)

    with col3a:
        st.markdown(f'<div class="sh">{t("Tổng volume theo tuần", "Total Weekly Volume")}</div>',unsafe_allow_html=True)
        wk=dff["Total_Volume"].resample("W").sum().reset_index(); wk.columns=["Week","Vol"]
        fig5=go.Figure(go.Bar(x=wk["Week"].dt.strftime("%d/%m"),y=wk["Vol"],
            marker_color=ACCENT,marker_line_width=0,
            hovertemplate="%{x}<br>%{y:,.0f} M$<extra></extra>"))
        fig5.update_layout(**base_layout(height=280,title=dict(text=t("<b>Volume theo tuần</b>", "<b>Weekly Volume</b>"),font=dict(size=13)),yaxis_title="M$"))
        st.plotly_chart(fig5,use_container_width=True)



    with col3b:
        st.markdown(f'<div class="sh">{t("Volume TB / coin", "Avg Volume / coin")}</div>',unsafe_allow_html=True)
        av=sorted([(c,dff[f"{c}_vol_M"].mean()) for c in coins],key=lambda x:x[1])
        fig6=go.Figure(go.Bar(x=[v for _,v in av],y=[c.upper() for c,_ in av],orientation="h",
            marker_color=[COIN_COLORS[c] for c,_ in av],
            hovertemplate="%{y}: %{x:,.0f} M$<extra></extra>"))
        fig6.update_layout(**base_layout(height=280,title=dict(text=t("<b>Volume TB / Ngày</b>", "<b>Avg Daily Volume</b>"),font=dict(size=13)),xaxis_title="M$"))
        st.plotly_chart(fig6,use_container_width=True)

    with st.expander(t("Thuật toán đo lường Khối lượng (Volume)", "Volume Measurement Algorithms")):
        if is_vn:
            st.markdown("""
            **1. Tổng volume theo tuần:** Cộng dồn toàn bộ khối lượng giao dịch của 10 đồng coin lại mỗi tuần.
            **2. Volume TB / Ngày:** Khối lượng giao dịch trung bình mỗi ngày của từng đồng coin để đo lường thanh khoản.
            """)
        else:
            st.markdown("""
            **1. Total Weekly Volume:** Sums up the total trading volume of all 10 coins for each week.
            **2. Avg Daily Volume:** Average daily trading volume of each coin to measure liquidity.
            """)

# ════ TAB 4 ═══════════════════════════════════

with t4:

    st.markdown(f'<div class="sh">{t("Ma trận tương quan lợi suất hàng ngày", "Daily Return Correlation Matrix")}</div>',unsafe_allow_html=True)
    ret_df=dff[[f"{c}_price" for c in coins]].pct_change().dropna()
    ret_df.columns=[c.upper() for c in coins]
    corr=ret_df.corr()
    fig7=go.Figure(go.Heatmap(z=corr.values,x=corr.columns.tolist(),y=corr.columns.tolist(),
        colorscale=[[0,RED],[0.5,"#1a2332"],[1,GREEN]],zmin=-1,zmax=1,
        text=corr.values.round(2),texttemplate="<b>%{text}</b>",textfont=dict(size=12),
        hovertemplate="<b>%{x} ↔ %{y}</b><br>r = %{z:.3f}<extra></extra>",
        colorbar=dict(title=t("Hệ số r", "r-value"),tickfont=dict(color=TEXT),len=0.9)))
    fig7.update_layout(**base_layout(height=480,
        title=dict(text="<b>Heatmap tương quan — Daily Returns (Pearson r)</b>",font=dict(size=15)),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),yaxis=dict(gridcolor="rgba(0,0,0,0)")))
    st.plotly_chart(fig7,use_container_width=True)

    corr_btc_eth = corr.loc["BTC", "ETH"]
    corr_btc_trx = corr.loc["BTC", "TRX"]

    with st.expander(t("Thuật toán tính Hệ số tương quan Pearson", "Pearson Correlation Coefficient Algorithm")):
        if is_vn:
            st.markdown(f"""
            **1. Chuyển đổi dữ liệu:** Thuật toán tự động chuyển đổi Giá thành **Lợi suất hàng ngày (Daily Returns)** để tránh sai lệch xu hướng.
            **2. Hệ số tương quan Pearson ($r$):** Đo lường hai đồng coin có đi chung đường hay không (từ -1 đến 1).
            **Nhìn vào số liệu thực tế trên hình:**
            - Cặp **BTC & ETH** có hệ số là **{corr_btc_eth:.2f}** (rất gần 1, màu xanh). BTC tăng thì ETH cũng tăng!
            - Ngược lại, cặp **BTC & TRX** có hệ số chỉ là **{corr_btc_trx:.2f}**. Hai đồng này có mối liên hệ với nhau rất thấp.
            """)
        else:
            st.markdown(f"""
            **1. Data Conversion:** The algorithm converts Prices to **Daily Returns** to avoid trend bias.
            **2. Pearson Correlation ($r$):** Measures whether two coins move together (from -1 to 1).
            **Looking at actual data:**
            - **BTC & ETH** pair has a correlation of **{corr_btc_eth:.2f}** (close to 1, green). When BTC rises, ETH rises too!
            - Conversely, **BTC & TRX** pair has a correlation of only **{corr_btc_trx:.2f}**. These two coins have a very weak relationship.
            """)




# ════ TAB 5 ═══════════════════════════════════

with t5:

    st.markdown('<div class="sh">Độ biến động 7 ngày (Rolling Std)</div>',unsafe_allow_html=True)

    fig10=go.Figure()

    for coin in selected_coins:

        vol7=dff[f"{coin}_price"].pct_change().rolling(7).std()*100

        # ✅ FIX: hex_to_rgba thay vì hex+alpha string

        fig10.add_trace(go.Scatter(x=dff.index,y=vol7,name=coin.upper(),

            line=dict(color=COIN_COLORS[coin],width=2),

            fillcolor=hex_to_rgba(COIN_COLORS[coin],0.12),
            hovertemplate=f"<b>{coin.upper()}</b> %{{x|%d/%m}}<br>σ=%{{y:.2f}}%<extra></extra>"))
    fig10.update_layout(**base_layout(height=360,
        title=dict(text=t("<b>Độ biến động 7 ngày (Rolling Std %)</b>", "<b>Volatility 7D Rolling Std (%)</b>"),font=dict(size=14)),
        yaxis_title=t("Biến động (%)", "Volatility (%)"),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0),hovermode="x unified"))
    st.plotly_chart(fig10,use_container_width=True)

    btc_ret_7 = dff["btc_price"].pct_change().dropna().iloc[-7:] * 100
    btc_vol7_last = btc_ret_7.std()
    btc_avg7_last = btc_ret_7.mean()
    sq_diffs = sum((x - btc_avg7_last)**2 for x in btc_ret_7)
    var_7 = sq_diffs / 6

    with st.expander(t("Cách tính Độ biến động 7 ngày (Rolling Std)", "How to calculate 7D Rolling Volatility")):
        ret_str = ', '.join([f'{x:.2f}%' for x in btc_ret_7])
        if is_vn:
            st.markdown(f"""
            Để có được một điểm vẽ trên biểu đồ sóng này, máy tính sẽ làm 3 bước. Ví dụ cụ thể với Bitcoin (BTC) trong 7 ngày cuối cùng:
            - **Bước 1:** Lấy lợi suất 7 ngày liên tiếp: `[{ret_str}]`
            - **Bước 2:** Trung bình 7 ngày = `{btc_avg7_last:.2f}%`
            - **Bước 3:** Đo lường độ lệch chuẩn (căn bậc 2 phương sai): `√{var_7:.2f}` = **{btc_vol7_last:.2f}%**
            Kết luận: Mức {btc_vol7_last:.2f}% là điểm neo cuối cùng. Cột sóng càng cao tức là giá dao động cực kỳ mạnh.
            """)
        else:
            st.markdown(f"""
            To plot a single point on this chart, the system performs 3 steps. Example for Bitcoin (BTC) in the last 7 days:
            - **Step 1:** Get daily returns for 7 days: `[{ret_str}]`
            - **Step 2:** Calculate average return = `{btc_avg7_last:.2f}%`
            - **Step 3:** Calculate standard deviation: `√{var_7:.2f}` = **{btc_vol7_last:.2f}%**
            Conclusion: The value {btc_vol7_last:.2f}% is the final plotted point. Higher waves indicate extreme price volatility.
            """)



    st.markdown(f'<div class="sh">{t("Biểu đồ Rủi ro – Lợi nhuận (Risk-Return Map)", "Risk-Return Map")}</div>',unsafe_allow_html=True)
    rr=[]
    for coin in coins:
        dr=dff[f"{coin}_price"].pct_change().dropna()
        rr.append({"Coin":coin.upper(),"ck":coin,"Return":dr.mean()*100,"Risk":dr.std()*100,"Vol":dff[f"{coin}_vol_M"].mean()})
    rr_df=pd.DataFrame(rr)
    fig11=go.Figure()
    for _,row in rr_df.iterrows():
        fig11.add_trace(go.Scatter(x=[row["Risk"]],y=[row["Return"]],mode="markers+text",
            marker=dict(size=max(14,row["Vol"]/250),color=COIN_COLORS.get(row["ck"],"#aaa"),
                        line=dict(width=1.5,color="white"),opacity=0.88),
            text=[row["Coin"]],textposition="top center",textfont=dict(size=11,color=TEXT),
            name=row["Coin"],showlegend=False,
            hovertemplate=f"<b>{row['Coin']}</b><br>Return: {row['Return']:.3f}%<br>Risk σ: {row['Risk']:.3f}%<br>Vol: {row['Vol']:,.0f} M$<extra></extra>"))
    fig11.add_hline(y=0,line_dash="dash",line_color="#8B949E",line_width=0.8)
    fig11.update_layout(**base_layout(height=400,
        title=dict(text=t("<b>Rủi ro–Lợi nhuận (bong bóng = Volume TB)</b>", "<b>Risk–Return Map (bubble = Avg Vol)</b>"),font=dict(size=14)),
        xaxis_title=t("Rủi ro — Độ lệch chuẩn (%)", "Risk — Standard Deviation (%)"),yaxis_title=t("Lợi nhuận TB/ngày (%)", "Avg Daily Return (%)")))
    st.plotly_chart(fig11,use_container_width=True)

    btc_risk = rr_df.loc[rr_df["Coin"]=="BTC", "Risk"].values[0]
    btc_ret = rr_df.loc[rr_df["Coin"]=="BTC", "Return"].values[0]
    sol_risk = rr_df.loc[rr_df["Coin"]=="SOL", "Risk"].values[0]
    sol_ret = rr_df.loc[rr_df["Coin"]=="SOL", "Return"].values[0]

    with st.expander(t("Giải thích Biểu đồ Rủi ro - Lợi nhuận", "Risk-Return Chart Explanation")):
        if is_vn:
            st.markdown(f"""
            Mỗi bong bóng đặt ở tọa độ xác định bằng 3 phép tính tổng quát:
            **Ví dụ Bitcoin (BTC):** Lợi nhuận = **{btc_ret:.2f}%**, Rủi ro = **{btc_risk:.2f}%**, Vol = **{dff['btc_vol_M'].mean():,.0f} M$**.
            **Ví dụ Solana (SOL):** Lợi nhuận = **{sol_ret:.2f}%**, Rủi ro = **{sol_risk:.2f}%**.
            **Cách đọc:** BTC an toàn (rủi ro thấp), SOL nằm tít góc ngoài (rủi ro cao, lợi nhuận cao).
            """)
        else:
            st.markdown(f"""
            Each bubble is plotted using 3 calculated metrics:
            **Bitcoin (BTC) Example:** Return = **{btc_ret:.2f}%**, Risk = **{btc_risk:.2f}%**, Vol = **{dff['btc_vol_M'].mean():,.0f} M$**.
            **Solana (SOL) Example:** Return = **{sol_ret:.2f}%**, Risk = **{sol_risk:.2f}%**.
            **How to read:** BTC is safe (low risk). SOL is an outlier with much higher risk and higher potential returns.
            """)



    st.markdown(f'<div class="sh">{t("Phân phối lợi suất hàng ngày (Histogram)", "Daily Return Distribution (Histogram)")}</div>',unsafe_allow_html=True)
    fig_h=go.Figure()
    for coin in selected_coins:
        dr=dff[f"{coin}_price"].pct_change().dropna()*100
        fig_h.add_trace(go.Histogram(x=dr,name=coin.upper(),nbinsx=25,opacity=0.65,
            marker_color=COIN_COLORS[coin],
            hovertemplate=f"<b>{coin.upper()}</b><br>%{{x:.2f}}%: %{{y}} " + t("ngày", "days") + "<extra></extra>"))
    fig_h.update_layout(**base_layout(barmode="overlay",height=300,
        title=dict(text=t("<b>Phân phối lợi suất hàng ngày (%)</b>", "<b>Daily Returns Distribution (%)</b>"),font=dict(size=14)),
        xaxis_title="Daily Return (%)",yaxis_title=t("Số ngày", "Number of days"),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0)))
    st.plotly_chart(fig_h,use_container_width=True)

    max_ret = -999.0
    max_coin = ""
    min_ret = 999.0
    min_coin = ""
    for coin in selected_coins:
        dr = dff[f"{coin}_price"].pct_change().dropna() * 100
        if not dr.empty:
            c_max = dr.max()
            c_min = dr.min()
            if c_max > max_ret:
                max_ret = c_max
                max_coin = coin.upper()
            if c_min < min_ret:
                min_ret = c_min
                min_coin = coin.upper()

    with st.expander(t("Cách đọc và phân tích biểu đồ phân phối", "How to read and analyze the distribution chart")):
        if is_vn:
            st.markdown(f"""
            - **Hình dáng quả chuông đối xứng:** Các cột tập trung cao nhất ở xung quanh mốc 0%. Đa số các ngày giá coin chỉ biến động rất nhỏ.
            - Mức tăng lớn nhất 1 ngày: Đồng {max_coin} ({max_ret:.2f}%).
            - Mức giảm lớn nhất 1 ngày: Đồng {min_coin} ({min_ret:.2f}%).
            """)
        else:
            st.markdown(f"""
            - **Symmetrical Bell Shape:** Most bars are clustered around the 0% mark. In most days, the price fluctuation is minimal.
            - Highest single-day gain: {max_coin} ({max_ret:.2f}%).
            - Deepest single-day loss: {min_coin} ({min_ret:.2f}%).
            """)



# ════ TAB 6 ═══════════════════════════════════
with t6:
    col6a,col6b=st.columns(2)
    with col6a:
        st.markdown(f'<div class="sh">{t("Thị phần Volume trung bình", "Average Volume Market Share")}</div>',unsafe_allow_html=True)
        avg_vol={c:dff[f"{c}_vol_M"].mean() for c in coins}
        fig12=go.Figure(go.Pie(labels=[c.upper() for c in avg_vol],values=list(avg_vol.values()),hole=0.50,
            marker=dict(colors=[COIN_COLORS[c] for c in avg_vol],line=dict(color=BG,width=2)),
            textinfo="label+percent",textfont=dict(size=12),
            pull=[0.05 if c=="btc" else 0 for c in coins],
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} M$<br>%{percent}<extra></extra>"))
        fig12.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT,family="Inter"),margin=dict(l=20,r=20,t=55,b=20),
            title=dict(text=t("<b>Thị phần Volume (%)</b>", "<b>Volume Market Share (%)</b>"),font=dict(size=15,color=TEXT)),
            showlegend=False,height=400)
        st.plotly_chart(fig12,use_container_width=True)

    with col6b:
        st.markdown(f'<div class="sh">{t("Treemap — Dominance theo Volume", "Treemap — Volume Dominance")}</div>',unsafe_allow_html=True)
        tm=pd.DataFrame([{"Coin":c.upper(),"Volume":dff[f"{c}_vol_M"].mean()} for c in coins])
        fig13=px.treemap(tm,path=["Coin"],values="Volume",color="Volume",
            color_continuous_scale=[[0,"#1a2332"],[0.5,"#004d99"],[1,ACCENT]])
        fig13.update_traces(texttemplate="<b>%{label}</b><br>%{value:,.0f}M$",textfont=dict(size=13),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} M$<extra></extra>",
            marker_line_color=BG,marker_line_width=2)
        fig13.update_layout(paper_bgcolor="rgba(0,0,0,0)",margin=dict(l=10,r=10,t=55,b=10),
            title=dict(text="<b>Treemap Volume Dominance</b>",font=dict(size=15,color=TEXT)),
            font=dict(color=TEXT,family="Inter"),height=400,coloraxis_showscale=False)
        st.plotly_chart(fig13,use_container_width=True)

    st.markdown(f'<div class="sh">{t("Dòng tiền theo thời gian — Stacked Area Chart", "Money Flow over Time — Stacked Area Chart")}</div>',unsafe_allow_html=True)
    fig14=go.Figure()
    for coin in coins:
        fig14.add_trace(go.Scatter(x=dff.index,y=dff[f"{coin}_vol_M"],stackgroup="one",name=coin.upper(),
            line=dict(width=0.5,color=COIN_COLORS[coin]),fillcolor=COIN_COLORS[coin],
            hovertemplate=f"<b>{coin.upper()}</b> %{{x|%d/%m}}: %{{y:,.0f}}M$<extra></extra>"))
    fig14.update_layout(**base_layout(height=360,
        title=dict(text=t("<b>Tổng dòng tiền tích lũy theo ngày (Stacked Area)</b>", "<b>Cumulative Daily Money Flow (Stacked Area)</b>"),font=dict(size=14)),
        yaxis_title=t("Volume (Triệu USD)", "Volume (Million USD)"),
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0),hovermode="x unified"))
    st.plotly_chart(fig14,use_container_width=True)

    st.markdown(f'<div class="sh">{t("Thị phần Volume theo tháng", "Monthly Volume Market Share")}</div>',unsafe_allow_html=True)
    dff["Month"]=dff.index.strftime("%m/%Y")
    monthly=dff.groupby("Month")[[f"{c}_vol_M" for c in coins]].sum()
    fig15=go.Figure()
    for coin in coins:
        fig15.add_trace(go.Bar(x=monthly.index,y=monthly[f"{coin}_vol_M"],name=coin.upper(),
            marker_color=COIN_COLORS[coin],
            hovertemplate=f"<b>{coin.upper()}</b> %{{x}}<br>%{{y:,.0f}}M$<extra></extra>"))
    fig15.update_layout(**base_layout(barmode="stack",height=300,
        title=dict(text=t("<b>Volume theo tháng — Market Share</b>", "<b>Monthly Volume — Market Share</b>"),font=dict(size=14)),
        yaxis_title="Volume (M$)",
        legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0)))
    st.plotly_chart(fig15,use_container_width=True)

    with st.expander(t("Cách tính các biểu đồ thị phần (Market Share)", "Market Share Charts Calculation")):
        if is_vn:
            st.markdown("""
            **1. Pie Chart & Treemap:** Tính trung bình từng coin, cộng lại thành 100% rồi chia tỷ trọng.
            **2. Stacked Area:** Xếp chồng dòng tiền các coin lên nhau theo thời gian.
            **3. Stacked Bar:** Gom các khối lượng theo tháng.
            """)
        else:
            st.markdown("""
            **1. Pie Chart & Treemap:** Averages each coin, totals 100%, and calculates weight.
            **2. Stacked Area:** Stacks daily money flows of all coins chronologically.
            **3. Stacked Bar:** Aggregates and stacks trading volumes by month.
            """)

# ── FOOTER ────────────────────────────────────
st.markdown("---")
footer_text = "🎓 Đồ án môn <b>Trực quan hóa dữ liệu</b> &nbsp;|&nbsp; Mô hình <b>CRIX (Volume-Weighted Cryptocurrency Index)</b>" if is_vn else "🎓 <b>Data Visualization</b> Course Project &nbsp;|&nbsp; <b>CRIX (Volume-Weighted Cryptocurrency Index)</b> Model"
st.markdown(f"<div style='text-align:center;color:#8B949E;font-size:12px;padding:10px 0'>{footer_text} &nbsp;|&nbsp; Data: Yahoo Finance &nbsp;|&nbsp; Built with ❤️ using <b>Streamlit + Plotly</b></div>",unsafe_allow_html=True)
