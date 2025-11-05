import streamlit as st
import pandas as pd
import plotly.express as px  # ✅ Make sure this line is correct — no closing parenthesis!

st.set_page_config(page_title="Store Compliance Dashboard", layout="wide")
st.title("📊 Store-wise Monthly Compliance Dashboard")

# CSV Upload
uploaded_file = st.file_uploader("Upload your monthly compliance CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='latin1')


    # Validate required columns
    required_cols = ['Store', 'Period', 'Compliance', 'الجودة والسلامة الغذائية', 'خدمات', 'نظافة']
    if not all(col in df.columns for col in required_cols):
        st.error("CSV must contain: Store, Period, Compliance, الجودة والسلامة الغذائية, خدمات, نظافة")
    else:
        # Grouped Bar Chart
        st.subheader("📍 Monthly Compliance by Store")
        grouped_df = df.groupby(['Store', 'Period'])['Compliance'].mean().reset_index()

        fig = px.bar(
            grouped_df,
            x='Store',
            y='Compliance',
            color='Period',
            barmode='group',
            title='Compliance Scores by Store and Month',
            labels={'Compliance': 'Compliance %'},
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # Drilldown Section
        st.subheader("🔍 Section-wise Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            selected_store = st.selectbox("Select Store", sorted(df['Store'].unique()))
        with col2:
            selected_month = st.selectbox("Select Month", sorted(df['Period'].unique()))

        filtered = df[(df['Store'] == selected_store) & (df['Period'] == selected_month)]

        if not filtered.empty:
            section_scores = filtered[['الجودة والسلامة الغذائية', 'خدمات', 'نظافة']].mean()
            section_df = pd.DataFrame({
                'Section': section_scores.index,
                'Score': section_scores.values
            })

            fig2 = px.bar(
                section_df,
                x='Section',
                y='Score',
                color='Section',
                title=f"Section-wise Compliance for {selected_store} in {selected_month}",
                labels={'Score': 'Compliance %'},
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data available for selected store and month.")
