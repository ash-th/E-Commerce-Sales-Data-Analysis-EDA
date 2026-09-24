# 📊 Financial Default Risk Analytics

A Python-based data analytics project that explores **financial default and order risk** patterns using a retail transactions dataset. The project includes full data loading, cleaning, grouping/summarising, interactive visualisations, and a **Streamlit** web dashboard.

---

## 🗂️ Project Structure

```
├── app.py                  # Streamlit frontend (main entry point)
├── data_loader.py          # Data loading, validation, and cleaning
├── analytics.py            # Grouping, summaries, KPIs, and business insights
├── clean_final_data.csv    # Source dataset
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 📁 Dataset

**File:** `clean_final_data.csv`  
**Columns:**

| Column | Type | Description |
|---|---|---|
| OrderID | int | Unique order identifier |
| CustomerID | int | Customer identifier |
| OrderDate | date | Date the order was placed |
| ProductID | int | Product identifier |
| Quantity | float | Units ordered |
| Discount | float | Discount percentage applied |
| PaymentMethod | str | Payment channel (Gateway, Wallet, Cash, CardToCard) |
| Status | str | Order outcome: **Completed**, **Returned**, **Cancelled** |
| Age | float | Customer age |
| City | str | Customer city |
| SignupDate | date | Customer account registration date |
| CustomerSegment | str | Segment: New, Regular, VIP |
| ProductName | str | Product name |
| Category | str | Product category |
| UnitPrice | float | Per-unit price |
| Sales | float | Net sale value |
| OrderValue | float | Gross order value |

> **Default / At-Risk** = orders with Status `Returned` or `Cancelled`.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- pip

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`.

---

## 🧩 Features

### Data Pipeline
- **Load** CSV dataset automatically on startup.
- **Validate** for missing values, duplicates, invalid statuses, and out-of-range numerics.
- **Clean** by filling missing values, parsing dates, removing invalid rows, and deriving new columns (e.g., `IsDefaultRisk`, `AgeBucket`, `OrderYearMonth`).

### Analytics
- **KPIs** — total orders, revenue, default rate, average order value, discount, and customer age.
- **Status Distribution** — pie and bar charts showing Completed / Returned / Cancelled breakdown.
- **Risk by Category** — which product categories drive the most cancellations and returns.
- **Risk by Payment Method** — payment channels associated with higher risk.
- **Risk by Customer Segment** — New, Regular, and VIP risk profiles.
- **Risk by City** — geographic risk hotspots (top 10 cities).
- **Risk by Age Group** — age-bracket-level default rates.
- **Monthly Trends** — revenue, order volume, and default rate over time.
- **Top Risky Products** — products with the highest default rates.
- **Discount vs Default Rate** — relationship between discount bands and order risk.

### Business Insights
Auto-generated, data-driven recommendations covering:
- Fraud and return prevention
- Inventory and supply chain protection
- Customer segmentation strategy
- Discount policy reform
- Real-time monitoring recommendations

---

## 📊 Dashboard Tabs

| Tab | Contents |
|---|---|
| 📌 Overview | KPIs, status distribution |
| ⚠️ Risk Analysis | Category, payment, segment, city, age risk |
| 📈 Trends | Monthly revenue, volume, and default rate trends |
| 🛍️ Products & Discounts | Top risky products, discount vs default |
| 🗂️ Data Quality | Validation report, cleaned data preview |
| 💡 Business Insights | Auto-generated insights and recommendations |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Pandas | Data loading, cleaning, and grouping |
| NumPy | Numerical operations |
| Plotly Express | Interactive charts |
| Streamlit | Web dashboard frontend |
| python-docx | Project report generation |

---

## 📝 License

This project is for educational and analytical purposes only.
