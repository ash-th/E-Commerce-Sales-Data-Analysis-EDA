"""
app.py
------
Streamlit frontend for the Financial Default Risk Analytics Dashboard.
Run with:  streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from data_loader import load_and_clean
from analytics import (
    kpis,
    status_distribution,
    risk_by_category,
    risk_by_payment,
    risk_by_segment,
    monthly_trend,
    risk_by_age,
    top_risky_products,
    discount_vs_default,
    risk_by_city,
    generate_insights,
)

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Default Risk Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        /* Main background */
        .main { background-color: #f7f8fa; }

        /* KPI metric cards */
        div[data-testid="metric-container"] {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 14px 18px;
        }
        div[data-testid="metric-container"] label {
            font-size: 0.78rem !important;
            color: #57606a !important;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            font-size: 1.6rem !important;
            font-weight: 700;
            color: #1f2328;
        }

        /* Section dividers */
        .section-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #1f2328;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            border-left: 4px solid #3b82d4;
            padding-left: 10px;
        }

        /* Insight cards */
        .insight-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-left: 5px solid #3b82d4;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 10px;
            font-size: 0.93rem;
            line-height: 1.6;
            color: #1f2328;
        }

        /* Table styling */
        .dataframe thead th {
            background-color: #3b82d4 !important;
            color: white !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1f2328;
        }
        section[data-testid="stSidebar"] * {
            color: #f0f0f0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Load Data ────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "clean_final_data.csv")

@st.cache_data(show_spinner="Loading and cleaning dataset …")
def get_data(path):
    return load_and_clean(path)

raw_df, df, validation_report = get_data(DATA_PATH)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    # Year filter
    years = sorted(df["OrderYear"].dropna().unique().tolist())
    year_options = ["All Years"] + [str(int(y)) for y in years]
    sel_year = st.selectbox("Order Year", year_options)

    # Category filter
    categories = ["All Categories"] + sorted(df["Category"].dropna().unique().tolist())
    sel_category = st.selectbox("Product Category", categories)

    # Customer Segment filter
    segments = ["All Segments"] + sorted(df["CustomerSegment"].dropna().unique().tolist())
    sel_segment = st.selectbox("Customer Segment", segments)

    # Payment Method filter
    payments = ["All Methods"] + sorted(df["PaymentMethod"].dropna().unique().tolist())
    sel_payment = st.selectbox("Payment Method", payments)

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#aaa;'>Financial Default Risk Analytics v1.0</div>",
        unsafe_allow_html=True,
    )

# Apply filters
filtered = df.copy()
if sel_year != "All Years":
    filtered = filtered[filtered["OrderYear"] == int(sel_year)]
if sel_category != "All Categories":
    filtered = filtered[filtered["Category"] == sel_category]
if sel_segment != "All Segments":
    filtered = filtered[filtered["CustomerSegment"] == sel_segment]
if sel_payment != "All Methods":
    filtered = filtered[filtered["PaymentMethod"] == sel_payment]

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("# 📊 Financial Default Risk Analytics Dashboard")
st.markdown(
    f"Analysing **{len(filtered):,}** orders · Dataset: `clean_final_data.csv` · "
    f"Filters applied: Year={sel_year} | Category={sel_category} | "
    f"Segment={sel_segment} | Payment={sel_payment}"
)
st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# TAB NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
tab_overview, tab_risk, tab_trends, tab_products, tab_data, tab_insights = st.tabs([
    "📌 Overview",
    "⚠️ Risk Analysis",
    "📈 Trends",
    "🛍️ Products & Discounts",
    "🗂️ Data Quality",
    "💡 Business Insights",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

    kpi_vals = kpis(filtered)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders",         f"{kpi_vals['Total Orders']:,}")
    col2.metric("Unique Customers",     f"{kpi_vals['Unique Customers']:,}")
    col3.metric("Total Revenue",        f"${kpi_vals['Total Revenue (Sales)']:,.2f}")
    col4.metric("Avg Order Value",      f"${kpi_vals['Avg Order Value']:,.2f}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("At-Risk Orders",       f"{kpi_vals['Default / At-Risk Orders']:,}")
    col6.metric("Default Rate",         f"{kpi_vals['Default Rate (%)']:.1f}%")
    col7.metric("Avg Discount",         f"{kpi_vals['Avg Discount (%)']:.1f}%")
    col8.metric("Avg Customer Age",     f"{kpi_vals['Avg Customer Age']:.1f} yrs")

    st.markdown("---")

    # Status Distribution
    st.markdown('<div class="section-header">Order Status Distribution</div>', unsafe_allow_html=True)
    status_df = status_distribution(filtered)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        fig_pie = px.pie(
            status_df,
            values="Count",
            names="Status",
            color="Status",
            color_discrete_map={
                "Completed": "#3b82d4",
                "Returned":  "#f59e0b",
                "Cancelled": "#ef4444",
            },
            hole=0.45,
            title="Orders by Status",
        )
        fig_pie.update_layout(
            margin=dict(t=40, b=10, l=10, r=10),
            legend=dict(orientation="h", y=-0.1),
            paper_bgcolor="white",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        fig_bar_status = px.bar(
            status_df,
            x="Status",
            y="TotalSales",
            color="Status",
            color_discrete_map={
                "Completed": "#3b82d4",
                "Returned":  "#f59e0b",
                "Cancelled": "#ef4444",
            },
            text_auto=".2s",
            title="Revenue by Order Status",
            labels={"TotalSales": "Total Sales ($)", "Status": "Order Status"},
        )
        fig_bar_status.update_layout(
            showlegend=False,
            margin=dict(t=40, b=10),
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
        )
        st.plotly_chart(fig_bar_status, use_container_width=True)

    st.dataframe(
        status_df.rename(columns={
            "Count": "Orders", "TotalSales": "Total Sales ($)", "Percentage": "Share (%)"
        }),
        use_container_width=True,
        hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – RISK ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab_risk:
    st.markdown('<div class="section-header">Default Risk by Product Category</div>', unsafe_allow_html=True)
    rc_df = risk_by_category(filtered)

    fig_cat = px.bar(
        rc_df.sort_values("DefaultRate_%"),
        x="DefaultRate_%",
        y="Category",
        orientation="h",
        color="DefaultRate_%",
        color_continuous_scale=["#3b82d4", "#f59e0b", "#ef4444"],
        text_auto=".1f",
        title="Default Rate (%) by Category",
        labels={"DefaultRate_%": "Default Rate (%)", "Category": "Product Category"},
    )
    fig_cat.update_layout(
        coloraxis_showscale=False,
        margin=dict(t=40, b=10),
        paper_bgcolor="white",
        plot_bgcolor="#f7f8fa",
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    st.dataframe(
        rc_df.rename(columns={
            "TotalOrders": "Total Orders", "AtRiskOrders": "At-Risk Orders",
            "TotalSales": "Total Sales ($)", "AvgDiscount": "Avg Discount (%)",
            "AvgOrderValue": "Avg Order Value ($)", "DefaultRate_%": "Default Rate (%)",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown('<div class="section-header">Default Risk by Payment Method</div>', unsafe_allow_html=True)
        rp_df = risk_by_payment(filtered)
        fig_pay = px.bar(
            rp_df.sort_values("DefaultRate_%"),
            x="DefaultRate_%",
            y="PaymentMethod",
            orientation="h",
            color="DefaultRate_%",
            color_continuous_scale=["#3b82d4", "#ef4444"],
            text_auto=".1f",
            title="Default Rate (%) by Payment Method",
            labels={"DefaultRate_%": "Default Rate (%)", "PaymentMethod": "Payment Method"},
        )
        fig_pay.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=40, b=10),
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
        )
        st.plotly_chart(fig_pay, use_container_width=True)
        st.dataframe(
            rp_df.rename(columns={
                "TotalOrders": "Total Orders", "AtRiskOrders": "At-Risk",
                "TotalSales": "Total Sales ($)", "AvgDiscount": "Avg Disc (%)",
                "DefaultRate_%": "Default Rate (%)",
            }),
            use_container_width=True,
            hide_index=True,
        )

    with col_r2:
        st.markdown('<div class="section-header">Default Risk by Customer Segment</div>', unsafe_allow_html=True)
        rs_df = risk_by_segment(filtered)
        fig_seg = px.bar(
            rs_df.sort_values("DefaultRate_%"),
            x="DefaultRate_%",
            y="CustomerSegment",
            orientation="h",
            color="DefaultRate_%",
            color_continuous_scale=["#3b82d4", "#ef4444"],
            text_auto=".1f",
            title="Default Rate (%) by Customer Segment",
            labels={"DefaultRate_%": "Default Rate (%)", "CustomerSegment": "Customer Segment"},
        )
        fig_seg.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=40, b=10),
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
        )
        st.plotly_chart(fig_seg, use_container_width=True)
        st.dataframe(
            rs_df.rename(columns={
                "TotalOrders": "Total Orders", "AtRiskOrders": "At-Risk",
                "TotalRevenue": "Total Revenue ($)", "AvgOrderValue": "Avg Order Value ($)",
                "DefaultRate_%": "Default Rate (%)",
            }),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")
    st.markdown('<div class="section-header">Default Risk by City (Top 10)</div>', unsafe_allow_html=True)
    rc_city = risk_by_city(filtered, top_n=10)
    fig_city = px.bar(
        rc_city.sort_values("DefaultRate_%"),
        x="DefaultRate_%",
        y="City",
        orientation="h",
        color="TotalRevenue",
        color_continuous_scale="Blues",
        text_auto=".1f",
        title="Default Rate (%) by City — bubble sized by Revenue",
        labels={"DefaultRate_%": "Default Rate (%)", "TotalRevenue": "Revenue ($)"},
    )
    fig_city.update_layout(
        margin=dict(t=40, b=10),
        paper_bgcolor="white",
        plot_bgcolor="#f7f8fa",
    )
    st.plotly_chart(fig_city, use_container_width=True)

    st.markdown('<div class="section-header">Default Risk by Age Group</div>', unsafe_allow_html=True)
    ra_df = risk_by_age(filtered)
    fig_age = px.bar(
        ra_df,
        x="AgeBucket",
        y="DefaultRate_%",
        color="DefaultRate_%",
        color_continuous_scale=["#3b82d4", "#ef4444"],
        text_auto=".1f",
        title="Default Rate (%) by Customer Age Group",
        labels={"DefaultRate_%": "Default Rate (%)", "AgeBucket": "Age Group"},
    )
    fig_age.update_layout(
        coloraxis_showscale=False,
        margin=dict(t=40, b=10),
        paper_bgcolor="white",
        plot_bgcolor="#f7f8fa",
    )
    st.plotly_chart(fig_age, use_container_width=True)
    st.dataframe(
        ra_df.rename(columns={
            "AgeBucket": "Age Group", "TotalOrders": "Total Orders",
            "AtRiskOrders": "At-Risk Orders", "AvgOrderValue": "Avg Order Value ($)",
            "DefaultRate_%": "Default Rate (%)",
        }),
        use_container_width=True,
        hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – TRENDS
# ══════════════════════════════════════════════════════════════════════════════
with tab_trends:
    st.markdown('<div class="section-header">Monthly Order Volume & Revenue Trend</div>', unsafe_allow_html=True)
    mt_df = monthly_trend(filtered)

    if len(mt_df) == 0:
        st.info("No data available for the selected filters.")
    else:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=mt_df["OrderYearMonth"],
            y=mt_df["TotalRevenue"],
            name="Revenue ($)",
            marker_color="#3b82d4",
            opacity=0.75,
            yaxis="y",
        ))
        fig_trend.add_trace(go.Scatter(
            x=mt_df["OrderYearMonth"],
            y=mt_df["TotalOrders"],
            name="Order Count",
            mode="lines+markers",
            marker=dict(size=6),
            line=dict(color="#7c5cd8", width=2),
            yaxis="y2",
        ))
        fig_trend.update_layout(
            title="Monthly Revenue & Order Volume",
            xaxis_title="Month",
            yaxis=dict(title="Revenue ($)", showgrid=False),
            yaxis2=dict(title="Order Count", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", y=1.08),
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
            margin=dict(t=60, b=30),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown('<div class="section-header">Monthly Default Rate Trend</div>', unsafe_allow_html=True)
        fig_def_trend = px.line(
            mt_df,
            x="OrderYearMonth",
            y="DefaultRate_%",
            markers=True,
            title="Monthly Default Rate (%)",
            labels={"OrderYearMonth": "Month", "DefaultRate_%": "Default Rate (%)"},
            color_discrete_sequence=["#ef4444"],
        )
        fig_def_trend.add_hline(
            y=mt_df["DefaultRate_%"].mean(),
            line_dash="dash",
            line_color="#57606a",
            annotation_text=f"Avg: {mt_df['DefaultRate_%'].mean():.1f}%",
            annotation_position="bottom right",
        )
        fig_def_trend.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
            margin=dict(t=40, b=20),
        )
        st.plotly_chart(fig_def_trend, use_container_width=True)

        st.dataframe(
            mt_df.rename(columns={
                "OrderYearMonth": "Period", "TotalOrders": "Orders",
                "AtRiskOrders": "At-Risk Orders", "TotalRevenue": "Revenue ($)",
                "DefaultRate_%": "Default Rate (%)",
            }),
            use_container_width=True,
            hide_index=True,
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – PRODUCTS & DISCOUNTS
# ══════════════════════════════════════════════════════════════════════════════
with tab_products:
    st.markdown('<div class="section-header">Top 10 Highest Default-Risk Products</div>', unsafe_allow_html=True)
    tp_df = top_risky_products(filtered, top_n=10)

    fig_prod = px.bar(
        tp_df.sort_values("DefaultRate_%"),
        x="DefaultRate_%",
        y="ProductName",
        orientation="h",
        color="TotalSales",
        color_continuous_scale="RdYlGn_r",
        text_auto=".1f",
        title="Top Products by Default Rate",
        labels={"DefaultRate_%": "Default Rate (%)", "ProductName": "Product", "TotalSales": "Revenue ($)"},
    )
    fig_prod.update_layout(
        margin=dict(t=40, b=10),
        paper_bgcolor="white",
        plot_bgcolor="#f7f8fa",
    )
    st.plotly_chart(fig_prod, use_container_width=True)
    st.dataframe(
        tp_df.rename(columns={
            "ProductName": "Product", "TotalOrders": "Total Orders",
            "AtRiskOrders": "At-Risk Orders", "TotalSales": "Total Sales ($)",
            "AvgDiscount": "Avg Discount (%)", "DefaultRate_%": "Default Rate (%)",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.markdown('<div class="section-header">Discount Level vs Default Rate</div>', unsafe_allow_html=True)
    dd_df = discount_vs_default(filtered)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig_disc = px.bar(
            dd_df,
            x="DiscountBin",
            y="DefaultRate_%",
            color="DefaultRate_%",
            color_continuous_scale=["#3b82d4", "#ef4444"],
            text_auto=".1f",
            title="Default Rate by Discount Band",
            labels={"DiscountBin": "Discount Band", "DefaultRate_%": "Default Rate (%)"},
        )
        fig_disc.update_layout(
            coloraxis_showscale=False,
            margin=dict(t=40, b=10),
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
        )
        st.plotly_chart(fig_disc, use_container_width=True)

    with col_d2:
        fig_disc2 = px.bar(
            dd_df,
            x="DiscountBin",
            y="AvgSales",
            color="TotalOrders",
            color_continuous_scale="Blues",
            text_auto=".1f",
            title="Avg Sale Value by Discount Band",
            labels={"DiscountBin": "Discount Band", "AvgSales": "Avg Sales ($)", "TotalOrders": "Order Count"},
        )
        fig_disc2.update_layout(
            margin=dict(t=40, b=10),
            paper_bgcolor="white",
            plot_bgcolor="#f7f8fa",
        )
        st.plotly_chart(fig_disc2, use_container_width=True)

    st.dataframe(
        dd_df.rename(columns={
            "DiscountBin": "Discount Band", "TotalOrders": "Total Orders",
            "AtRiskOrders": "At-Risk Orders", "AvgSales": "Avg Sales ($)",
            "DefaultRate_%": "Default Rate (%)",
        }),
        use_container_width=True,
        hide_index=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 – DATA QUALITY
# ══════════════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown('<div class="section-header">Validation Report (Raw Dataset)</div>', unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)
    total_raw  = len(raw_df)
    total_dups = validation_report["duplicate_rows"]
    total_miss = sum(validation_report["missing_values"].values()) if validation_report["missing_values"] else 0
    bad_status = validation_report["invalid_status"]

    q1.metric("Raw Rows",          f"{total_raw:,}")
    q2.metric("Duplicate Rows",    f"{total_dups:,}")
    q3.metric("Missing Values",    f"{total_miss:,}")
    q4.metric("Invalid Statuses",  f"{bad_status:,}")

    if validation_report["missing_values"]:
        st.markdown("**Missing Values by Column:**")
        miss_df = pd.DataFrame(
            validation_report["missing_values"].items(),
            columns=["Column", "Missing Count"],
        )
        st.dataframe(miss_df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No missing values found in the dataset.")

    if validation_report["date_parse_errors"]:
        st.warning("**Date Parse Errors Detected:**")
        st.json(validation_report["date_parse_errors"])
    else:
        st.success("✅ All date values parsed successfully.")

    if validation_report["invalid_numerics"]:
        st.warning("**Negative Numeric Values Found:**")
        st.json(validation_report["invalid_numerics"])
    else:
        st.success("✅ No negative values in numeric columns.")

    st.markdown('<div class="section-header">Cleaned Dataset Preview</div>', unsafe_allow_html=True)
    st.markdown(f"**{len(df):,} rows × {len(df.columns)} columns** after cleaning")

    col_stats1, col_stats2 = st.columns(2)
    with col_stats1:
        st.markdown("**Numeric Summary Statistics**")
        num_cols = ["Age", "Quantity", "Discount", "UnitPrice", "Sales", "OrderValue"]
        st.dataframe(
            df[num_cols].describe().round(2),
            use_container_width=True,
        )
    with col_stats2:
        st.markdown("**Categorical Value Counts**")
        cat_summary = pd.DataFrame({
            "Column": ["Status", "Category", "PaymentMethod", "CustomerSegment", "City"],
            "Unique Values": [
                df["Status"].nunique(),
                df["Category"].nunique(),
                df["PaymentMethod"].nunique(),
                df["CustomerSegment"].nunique(),
                df["City"].nunique(),
            ],
        })
        st.dataframe(cat_summary, use_container_width=True, hide_index=True)

    st.markdown("**Sample of Cleaned Data (first 100 rows)**")
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 – BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
with tab_insights:
    st.markdown('<div class="section-header">AI-Assisted Business Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown(
        "The following insights are automatically derived from the current filtered dataset "
        "to support data-driven business decisions."
    )
    insights = generate_insights(filtered)
    for insight in insights:
        st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Risk Score Summary Table</div>', unsafe_allow_html=True)

    risk_summary = pd.DataFrame([
        {"Dimension": "Product Category",  "Highest Risk":    risk_by_category(filtered).iloc[0]["Category"],
         "Default Rate (%)": risk_by_category(filtered).iloc[0]["DefaultRate_%"]},
        {"Dimension": "Payment Method",    "Highest Risk":    risk_by_payment(filtered).iloc[0]["PaymentMethod"],
         "Default Rate (%)": risk_by_payment(filtered).iloc[0]["DefaultRate_%"]},
        {"Dimension": "Customer Segment",  "Highest Risk":    risk_by_segment(filtered).iloc[0]["CustomerSegment"],
         "Default Rate (%)": risk_by_segment(filtered).iloc[0]["DefaultRate_%"]},
        {"Dimension": "Age Group",         "Highest Risk":    str(risk_by_age(filtered).sort_values("DefaultRate_%", ascending=False).iloc[0]["AgeBucket"]),
         "Default Rate (%)": risk_by_age(filtered).sort_values("DefaultRate_%", ascending=False).iloc[0]["DefaultRate_%"]},
        {"Dimension": "City",              "Highest Risk":    risk_by_city(filtered).iloc[0]["City"],
         "Default Rate (%)": risk_by_city(filtered).iloc[0]["DefaultRate_%"]},
    ])
    st.dataframe(risk_summary, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Strategic Recommendations</div>', unsafe_allow_html=True)

    recommendations = [
        ("🔒 Fraud & Return Prevention",
         "Flag orders from the highest-risk payment method and category combination. "
         "Implement a secondary review process for orders above a discount threshold of 20%."),
        ("📦 Inventory & Supply Chain",
         "Prioritise stock protection for top-3 revenue categories. "
         "High return rates in specific categories may indicate quality or description mismatches."),
        ("🎯 Customer Segmentation Strategy",
         "Assign targeted onboarding, loyalty rewards, or credit limits per customer segment "
         "based on their historical default rate to reduce financial exposure."),
        ("💹 Discount Policy Reform",
         "Cap discounts at 15% for high-risk product categories to reduce incentive-driven "
         "cancellations and returns. Use dynamic discounting tied to customer risk scores."),
        ("📊 Real-Time Monitoring",
         "Establish monthly KPI dashboards with alerts when the default rate exceeds 15% "
         "in any single category, city, or payment channel for proactive intervention."),
    ]
    for title, body in recommendations:
        st.markdown(
            f'<div class="insight-card"><strong>{title}</strong><br>{body}</div>',
            unsafe_allow_html=True,
        )

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:0.78rem;color:#57606a;'>"
    "Financial Default Risk Analytics Dashboard · Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True,
)
