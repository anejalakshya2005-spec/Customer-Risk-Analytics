
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Customer Risk Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("customer_risk_predictions.csv")

# =====================================================
# TITLE
# =====================================================

st.title("📊 Customer Risk & Churn Analytics")
st.markdown(
    "### Machine Learning Powered Customer Risk Dashboard"
)

st.divider()

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_customers = len(df)

high_risk = len(
    df[df["Risk_Category"] == "High Risk"]
)

medium_risk = len(
    df[df["Risk_Category"] == "Medium Risk"]
)

low_risk = len(
    df[df["Risk_Category"] == "Low Risk"]
)

high_risk_percentage = (
    high_risk / total_customers * 100
)

# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Customers",
        total_customers
    )

with col2:
    st.metric(
        "🔴 High Risk",
        high_risk
    )

with col3:
    st.metric(
        "🟡 Medium Risk",
        medium_risk
    )

with col4:
    st.metric(
        "🟢 Low Risk",
        low_risk
    )

st.divider()

# =====================================================
# SIDEBAR FILTER
# =====================================================

st.sidebar.header("🔎 Dashboard Filters")

risk_options = [
    "All",
    "High Risk",
    "Medium Risk",
    "Low Risk"
]

selected_risk = st.sidebar.selectbox(
    "Risk Category",
    risk_options
)

# Apply filter

if selected_risk == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["Risk_Category"] == selected_risk
    ].copy()

st.sidebar.write(
    f"Customers shown: {len(filtered_df)}"
)

# =====================================================
# RISK DISTRIBUTION
# =====================================================

st.subheader("📈 Risk Distribution")

risk_counts = (
    filtered_df["Risk_Category"]
    .value_counts()
    .reset_index()
)

risk_counts.columns = [
    "Risk_Category",
    "Customer_Count"
]

fig1 = px.bar(
    risk_counts,
    x="Risk_Category",
    y="Customer_Count",
    text="Customer_Count",
    title="Customer Risk Categories"
)

fig1.update_layout(
    xaxis_title="Risk Category",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================================
# RISK PROBABILITY
# =====================================================

st.subheader("🎯 Risk Probability Distribution")

fig2 = px.histogram(
    filtered_df,
    x="Risk_Probability",
    nbins=20,
    title="Customer Risk Probability"
)

fig2.update_layout(
    xaxis_title="Risk Probability (%)",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# HIGH RISK CUSTOMERS
# =====================================================

st.subheader("🔴 High-Risk Customers")

high_risk_df = filtered_df[
    filtered_df["Risk_Category"] == "High Risk"
].sort_values(
    "Risk_Probability",
    ascending=False
)

if len(high_risk_df) > 0:

    st.dataframe(
        high_risk_df,
        use_container_width=True
    )

else:

    st.info(
        "No high-risk customers in the selected filter."
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Customer Risk & Churn Analytics | "
    "Machine Learning + Python + Streamlit + Plotly"
)
