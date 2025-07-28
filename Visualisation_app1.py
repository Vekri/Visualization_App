import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Store Data Visualizer", layout="wide")

st.title("📊 Store Data Dashboard")

# Upload section
file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if file is not None:
    # Load data
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("🔍 Raw Data")
    st.dataframe(df)

    st.subheader("📌 Summary Statistics")
    st.write(df.describe())

    # Column selection for visualizations
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    st.subheader("📉 Bar Chart")
    x_col = st.selectbox("X-axis (categorical)", cat_cols, key='bar_x')
    y_col = st.selectbox("Y-axis (numeric)", numeric_cols, key='bar_y')
    if x_col and y_col:
        fig_bar = px.bar(df, x=x_col, y=y_col, color=x_col, title=f"{y_col} by {x_col}")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🥧 Pie Chart")
    pie_col = st.selectbox("Column for Pie Chart", cat_cols, key='pie')
    if pie_col:
        pie_data = df[pie_col].value_counts().reset_index()
        pie_data.columns = [pie_col, 'Count']
        fig_pie = px.pie(pie_data, values='Count', names=pie_col, title=f"Distribution of {pie_col}")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("📈 Line Plot")
    time_col = st.selectbox("X-axis (Date/Time or Categorical)", df.columns, key='line_x')
    line_y = st.selectbox("Y-axis (numeric)", numeric_cols, key='line_y')
    if time_col and line_y:
        fig_line = px.line(df.sort_values(by=time_col), x=time_col, y=line_y, title=f"{line_y} over {time_col}")
        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📊 Correlation Heatmap")
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)

else:
    st.info("Please upload a CSV or Excel file to begin.")
