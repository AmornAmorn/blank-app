import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

# 1. โหลดข้อมูล (สมมติว่าไฟล์ชื่อ Product-Sales-Region.csv)
@st.cache_data
def load_data():
    df = pd.read_csv('Product-Sales-Region.xlsx - Sheet1.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("ตัวกรองข้อมูล")
    region = st.sidebar.multiselect(
        "เลือกภูมิภาค:",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    product = st.sidebar.multiselect(
        "เลือกสินค้า:",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    # กรองข้อมูลตามที่เลือก
    df_selection = df.query("Region == @region & Product == @product")

    # --- MAIN PAGE ---
    st.title("📊 Sales Performance Dashboard")
    st.markdown("## สรุปภาพรวมยอดขาย")

    # Metrics (KPIs)
    total_sales = df_selection["TotalPrice"].sum()
    total_units = df_selection["Quantity"].sum()
    avg_order = df_selection["TotalPrice"].mean()

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("ยอดขายรวม:")
        st.subheader(f"฿ {total_sales:,.2f}")
    with middle_column:
        st.subheader("จำนวนชิ้นที่ขายได้:")
        st.subheader(f"{total_units:,}")
    with right_column:
        st.subheader("ค่าเฉลี่ยต่อออเดอร์:")
        st.subheader(f"฿ {avg_order:,.2f}")

    st.markdown("---")

    # --- CHARTS ---
    # 1. ยอดขายตามสินค้า (Bar Chart)
    sales_by_product = df_selection.groupby(by=["Product"])[["TotalPrice"]].sum().sort_values(by="TotalPrice")
    fig_product_sales = px.bar(
        sales_by_product,
        x="TotalPrice",
        y=sales_by_product.index,
        orientation="h",
        title="<b>ยอดขายแยกตามประเภทสินค้า</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product),
        template="plotly_white",
    )

    # 2. ยอดขายตามภูมิภาค (Pie Chart)
    fig_region_sales = px.pie(
        df_selection,
        values="TotalPrice",
        names="Region",
        title="<b>สัดส่วนยอดขายตามภูมิภาค</b>",
        hole=0.4
    )

    left_chart, right_chart = st.columns(2)
    left_chart.plotly_chart(fig_product_sales, use_container_width=True)
    right_chart.plotly_chart(fig_region_sales, use_container_width=True)

    # 3. แนวโน้มยอดขายตามเวลา (Line Chart)
    sales_by_date = df_selection.groupby(by=["Date"])[["TotalPrice"]].sum()
    fig_date_sales = px.line(
        sales_by_date,
        x=sales_by_date.index,
        y="TotalPrice",
        title="<b>แนวโน้มยอดขายตามเวลา</b>",
        template="plotly_white"
    )
    st.plotly_chart(fig_date_sales, use_container_width=True)

    # แสดงตารางข้อมูล
    with st.expander("ดูข้อมูลทั้งหมด"):
        st.dataframe(df_selection)

except Exception as e:
    st.error(f"กรุณาตรวจสอบว่ามีไฟล์ข้อมูลอยู่ในโฟลเดอร์เดียวกันหรือไม่: {e}")
