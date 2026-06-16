<div align="center">
  <img src="https://img.icons8.com/color/120/000000/bitcoin--v1.png" width="80px"/>
  <h1>CRIX Crypto Market Dashboard 📊</h1>
  <p><i>Trực quan hóa Dữ liệu Thị trường Tiền Mã Hóa (Mô hình CRIX)</i></p>
</div>

> 🚀 **TRẢI NGHIỆM TRỰC TIẾP LIVE APP TẠI ĐÂY:**  
> 👉 **[https://crix-crypto-aaron.streamlit.app/](https://crix-crypto-aaron.streamlit.app/)** 👈

<div align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python 3.9+"></a>
</div>

---

## 🌟 Giới thiệu Dự án
**CRIX Crypto Dashboard** là một đồ án của môn **Trực quan hóa Dữ liệu (Data Visualization)**. 

Dự án này không chỉ dừng lại ở việc trực quan hóa dữ liệu bằng các biểu đồ, mà còn áp dụng các thuật toán tài chính để xây dựng chỉ số **CRIX (CRyptocurrency IndeX)**. Đây là một chỉ số được tính theo phương pháp trọng số khối lượng giao dịch (Volume-Weighted), giúp phản ánh mức độ tăng trưởng chung của thị trường tiền mã hóa. Có thể xem CRIX như một phiên bản tương tự VN-Index trên thị trường chứng khoán Việt Nam hay S&P 500 tại Mỹ, nhưng được thiết kế riêng cho thị trường tiền điện tử.

Dự án thu thập, làm sạch và xử lý dữ liệu của 10 đồng tiền mã hóa phổ biến trên thị trường từ năm 2022 đến 2026.

### 🪙 Danh sách 10 đồng coin được phân tích:
- **BTC (Bitcoin)**: Đồng tiền điện tử lớn nhất thị trường, thường được xem như "vàng kỹ thuật số".
- **ETH (Ethereum)**: Nền tảng blockchain hàng đầu cho hợp đồng thông minh và các ứng dụng phi tập trung.
- **BNB (Binance Coin)**: Đồng coin thuộc hệ sinh thái Binance, một trong những sàn giao dịch lớn nhất thế giới.
- **SOL (Solana)**: Blockchain nổi bật với tốc độ xử lý nhanh và chi phí giao dịch thấp.
- **XRP (Ripple)**: Được phát triển nhằm hỗ trợ thanh toán và chuyển tiền quốc tế.
- **ADA (Cardano)**: Blockchain chú trọng vào nghiên cứu học thuật, tính bền vững và bảo mật.
- **AVAX (Avalanche)**: Nền tảng blockchain có khả năng mở rộng cao, được sử dụng nhiều trong lĩnh vực DeFi.
- **DOGE (Dogecoin)**: Meme coin nổi tiếng với cộng đồng đông đảo và mức độ nhận diện cao.
- **DOT (Polkadot)**: Dự án tập trung vào việc kết nối và trao đổi dữ liệu giữa các blockchain khác nhau.
- **TRX (TRON)**: Blockchain hướng đến lĩnh vực giải trí, nội dung số và chia sẻ dữ liệu trực tuyến.

## 💼 Ứng dụng 

> Sản phẩm này không chỉ dừng lại ở việc hiển thị dữ liệu, mà còn biến dữ liệu thô thành những thông tin có giá trị, hỗ trợ người dùng trong quá trình phân tích và ra quyết định đầu tư.

**Thông tin chi tiết (Insights)**

1. **Dành cho Nhà phân tích / Trader:** Hệ thống cung cấp cái nhìn tổng quan về toàn bộ thị trường thông qua chỉ số CRIX. Từ đó, người dùng có thể nhận biết được khi nào dòng tiền đang đổ mạnh vào thị trường, thể hiện tâm lý lạc quan, và khi nào thị trường đang có dấu hiệu suy giảm hoặc thận trọng.
2. **Quản trị Rủi ro (Risk Management):** Thay vì chỉ quan sát biến động giá, hệ thống còn tính toán các chỉ số chuyên sâu như Sharpe Ratio và Rolling Volatility 7 ngày. Những chỉ số này giúp nhà đầu tư đánh giá mức độ rủi ro cũng như hiệu quả đầu tư của từng tài sản một cách định lượng hơn.
3. **Phân bổ vốn (Portfolio Allocation):** Hệ thống cung cấp ma trận tương quan giữa các đồng tiền điện tử. Thông qua đó, nhà đầu tư có thể biết những đồng coin nào thường tăng giảm cùng nhau và những đồng nào có xu hướng biến động khác nhau. Đây là cơ sở quan trọng để xây dựng danh mục đa dạng, giảm thiểu rủi ro thay vì tập trung toàn bộ vốn vào một nhóm tài sản.

## 🚀 Tính năng 

| Tính năng | Phân tích & Ý nghĩa |
|:---:|:---|
| 📈 **Chỉ số CRIX (Volume-Weighted)** | Trực quan hóa đường CRIX cùng các đường trung bình động (MA7, MA20). Bắt mạch xu hướng thị trường chính xác hơn việc chỉ nhìn vào Bitcoin. |
| 🔥 **Ma trận Tương quan (Heatmap)** | Đo lường mức độ biến động cùng nhau của 10 đồng coin bằng hệ số Pearson (r). Dữ liệu được chuyển sang Daily Returns để tăng độ chính xác của kết quả. |
| 📊 **Bản đồ Rủi ro (Risk-Return Map)** | Biểu đồ Scatter Plot giúp so sánh trực tiếp giữa lợi suất và rủi ro của từng đồng coin, từ đó hỗ trợ tìm ra những tài sản có tiềm năng sinh lời tốt với mức rủi ro hợp lý. |
| 📦 **Phân tích Thanh khoản** | Phân tích khối lượng giao dịch theo từng tuần, giúp nhận diện các giai đoạn dòng tiền tăng mạnh trên thị trường. |
| 💡 **Giải thích thuật toán trực quan** | Tích hợp tính năng mở rộng để xem công thức, giúp giải thích cách tính các chỉ số như Sharpe Ratio và Volatility một cách dễ hiểu. |

---

## 🛠 Tech Stack (Công nghệ sử dụng)
- **Ngôn ngữ:** Python
- **Xử lý Dữ liệu:** Pandas, NumPy
- **Trực quan hóa:** Plotly (Graph Objects & Express)
- **Xây dựng Web App:** Streamlit
- **Môi trường:** Jupyter Notebook (Cho quá trình EDA ban đầu)

---

## 💻 Hướng dẫn Cài đặt & Chạy cục bộ (Local)

Nếu bạn muốn chạy trực tiếp mã nguồn trên máy tính cá nhân:

**Bước 1: Clone kho lưu trữ này về máy**
```bash
git clone https://github.com/Tungmessi/CRIX-Crypto-Dashboard.git
cd CRIX-Crypto-Dashboard
```

**Bước 2: Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

**Bước 3: Chạy ứng dụng Streamlit**
```bash
streamlit run app.py
```
*Trình duyệt sẽ tự động mở trang web tại địa chỉ `http://localhost:8501`*

---
*Dự án được phát triển với mục đích học thuật và nghiên cứu phân tích dữ liệu thị trường.*
