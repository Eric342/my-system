import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import numpy as np
import cv2
from sklearn.linear_model import LinearRegression

# 初始化 session_state
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "首页"



# 美化主题
# ====================== 全局美化：海洋主题风格 ======================
st.markdown("""
    <style>
    /* 整体背景 - 浅海蓝渐变 */
    .stApp {
        background: linear-gradient(to bottom, #e6f4ff, #b3d9ff);
        background-attachment: fixed;
    }

    /* 标题 - 深蓝 + 阴影 */
    h1, h2, h3 {
        color: #004080 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* 按钮 - 蓝色 + 圆角 + 悬停效果 */
    .stButton > button {
        background-color: #0066cc !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        border: none !important;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #0052a3 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* 侧边栏 - 半透明浅蓝 */
    section[data-testid="stSidebar"] {
        background-color: rgba(240, 248, 255, 0.85) !important;
        border-right: 1px solid #cce0ff;
    }

    /* 卡片容器 - 用于仪表盘和内容块 */
    div.block-container {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }

    /* metric 卡片美化 */
    div[data-testid="stMetric"] {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# 解决图片切换页面后消失的问题
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

st.set_page_config(page_title="A09 海洋智能分析系统", layout="wide")
st.title("A09 面向海洋环境现象识别与多要素智能分析系统")
st.subheader("Eric")

# ====================== 首页：综合风险仪表盘 ======================
if st.session_state.current_tab == "首页":
    st.markdown("""
    # A09 海洋智能分析系统 - 综合仪表盘

    欢迎使用！本系统实现海洋现象识别、多要素融合分析与风险预测。  
    下面是当前最新状态汇总（实时更新）。

    **快速导航**：使用标签页换功能。
    """)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style="background:#e6f3ff; padding:1.5rem; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); text-align:center;">
            <h3 style="color:#0066cc; margin-bottom:0.5rem;">最近图片识别</h3>
            <p style="font-size:1.2rem; color:#004080;">{}</p >
        </div>
    """.format(st.session_state.get('last_recognition', '尚未识别')), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="background:#fff0e6; padding:1.5rem; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); text-align:center;">
            <h3 style="color:#cc6600; margin-bottom:0.5rem;">多要素关键指标</h3>
            <p style="font-size:1.1rem;">平均温度: 28.5°C<br>最大叶绿素: 12.8 mg/m³</p >
        </div>
    """, unsafe_allow_html=True)

with col3:
    risk = st.session_state.get('last_risk', 5.0)
    risk_color = "#ff4d4d" if risk > 15 else "#ffa500" if risk > 8 else "#28a745"
    st.markdown(f"""
        <div style="background:#e6ffe6; padding:1.5rem; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); text-align:center;">
            <h3 style="color:#006600; margin-bottom:0.5rem;">当前风险预测</h3>
            <p style="font-size:1.8rem; color:{risk_color}; font-weight:bold;">{risk:.1f}</p >
            <p style="color:#006600;">{'高风险！' if risk > 15 else '中风险' if risk > 8 else '低风险'}</p >
        </div>
    """, unsafe_allow_html=True)

# ====================== 美化：用 Tabs 横向标签页 ======================
tab1, tab2, tab3 = st.tabs(["1. 现象识别", "2. 多要素分析", "3. 趋势预测"])

with tab1:  # 或 if page == "1. 现象识别":
    st.header("现象识别（支持批量上传）")
    st.info("可一次上传多张图片，系统会逐一分析")

    uploaded_files = st.file_uploader("上传卫星图或照片（可多选）", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        for idx, uploaded in enumerate(uploaded_files):
            st.subheader(f"图片 {idx+1}: {uploaded.name}")
            img = Image.open(uploaded)
            st.image(img, width=500, caption="原图")

            # OpenCV 识别（你的原代码）
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)

            lower_redtide = np.array([35, 40, 40])
            upper_redtide = np.array([90, 255, 255])
            mask_redtide = cv2.inRange(hsv, lower_redtide, upper_redtide)
            redtide_area = cv2.countNonZero(mask_redtide)

            lower_oil = np.array([0, 0, 0])
            upper_oil = np.array([180, 50, 80])
            mask_oil = cv2.inRange(hsv, lower_oil, upper_oil)
            oil_area = cv2.countNonZero(mask_oil)

            total_pixels = img_cv.shape[0] * img_cv.shape[1]
            redtide_ratio = redtide_area / total_pixels if total_pixels > 0 else 0
            oil_ratio = oil_area / total_pixels if total_pixels > 0 else 0

            if oil_ratio > 0.02 and oil_ratio > redtide_ratio * 1.2:
                st.error(f"检测到【油污】！风险：高（占比 {oil_ratio:.1%}）")
            elif redtide_ratio > 0.02:
                st.warning(f"检测到【赤潮】！风险：中（占比 {redtide_ratio:.1%}）")
            else:
                st.success("正常海洋环境")

            st.info(f"调试：油污占比 {oil_ratio:.2%} | 赤潮占比 {redtide_ratio:.2%}")
            st.session_state.last_recognition = f"检测到：{'油污' if oil_ratio > redtide_ratio else '赤潮' if redtide_ratio > 0.02 else '正常'} (油污占比 {oil_ratio:.1%} / 赤潮占比 {redtide_ratio:.1%})"
            # 加掩码显示（可视化AI检测区域）
            col_mask1, col_mask2 = st.columns(2)
            with col_mask1:
                st.image(mask_oil, caption="油污检测掩码（白=疑似油污）", width=300, clamp=True)
            with col_mask2:
                st.image(mask_redtide, caption="赤潮检测掩码（白=疑似赤潮）", width=300, clamp=True)

            st.markdown("---")  # 分隔不同图片

with tab2:
    st.header("多要素智能分析仪表盘")
    st.markdown("模拟海洋赤潮期典型数据：温度升高 → 叶绿素暴增 → 盐度略降")

    dates = pd.date_range(start='2025-06-01', periods=60, freq='D')
    temp = 26 + 4 * np.sin(np.linspace(0, 3*np.pi, 60)) + np.random.normal(0, 0.8, 60)
    days_from_peak = (dates - pd.to_datetime('2025-07-20')).days
    chlorophyll = 0.5 + 15 * np.exp(-days_from_peak**2 / (2*15**2)) + np.random.normal(0, 1.5, 60)
    chlorophyll = np.clip(chlorophyll, 0.1, 25)
    salinity = 33.5 - 1.5 * (chlorophyll / 20) + np.random.normal(0, 0.4, 60)
    salinity = np.clip(salinity, 30, 35)

    data = pd.DataFrame({
        '日期': dates,
        '海表温度 (°C)': temp.round(1),
        '叶绿素浓度 (mg/m³)': chlorophyll.round(2),
        '盐度 (psu)': salinity.round(2),
    })

    fig = px.line(data, x='日期', y=['海表温度 (°C)', '叶绿素浓度 (mg/m³)', '盐度 (psu)'],
                  title="海洋要素趋势（模拟赤潮期）")
    fig.update_layout(legend_title_text='要素', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(data.style.format({"日期": lambda x: x.strftime("%Y-%m-%d")}))

    col1, col2, col3 = st.columns(3)
    col1.metric("平均海表温度", f"{data['海表温度 (°C)'].mean():.1f} °C")
    col2.metric("最大叶绿素浓度", f"{data['叶绿素浓度 (mg/m³)'].max():.1f} mg/m³", delta="赤潮高发阈值>10")
    col3.metric("赤潮风险指数", f"{(data['叶绿素浓度 (mg/m³)'].mean() * 1.8):.1f}", delta=">15为高风险")

with tab3:
    st.header("AI趋势预测与智能推荐")
    st.markdown("基于当前温度和叶绿素浓度预测30天后赤潮风险（非线性模型，更接近真实爆发）")

    col1, col2 = st.columns(2)
    with col1:
        current_temp = st.slider("当前海表温度 (°C)", 15.0, 35.0, 28.0, step=0.5)
    with col2:
        current_chla = st.slider("当前叶绿素浓度 (mg/m³)", 0.1, 25.0, 5.0, step=0.5)

    temp_factor = (current_temp - 25) ** 2 / 50
    chla_factor = current_chla ** 1.5 / 5
    interaction = (current_temp > 28) * (current_chla > 8) * 8
    predicted_risk = 2 + temp_factor + chla_factor + interaction
    predicted_risk = round(min(max(predicted_risk, 0), 20), 1)
    # 加这一行：更新首页的风险值
    st.session_state.last_risk = predicted_risk

    if predicted_risk > 15:
        st.error(f"预测30天后赤潮风险指数：**{predicted_risk}** （高风险！）")
    elif predicted_risk > 8:
        st.warning(f"预测30天后赤潮风险指数：**{predicted_risk}** （中风险）")
    else:
        st.success(f"预测30天后赤潮风险指数：**{predicted_risk}** （低风险）")

    st.info("**推荐措施**：")
    if predicted_risk > 12:
        st.markdown("立即启动无人机/船舶巡查监测")
        st.markdown("通知渔业/环保部门加强预警")
        st.markdown("准备投放生态调控剂或物理清除")
    else:
        st.markdown("继续日常卫星遥感与现场监测即可")

    temp_range = np.linspace(15, 35, 50)
    risks_fixed_chla = [2 + ((t-25)**2 / 50) + (current_chla**1.5 / 5) + ((t>28)*(current_chla>8)*8) for t in temp_range]
    risks_fixed_chla = np.clip(risks_fixed_chla, 0, 20)

    fig = px.line(x=temp_range, y=risks_fixed_chla,
                  title=f"固定叶绿素 {current_chla} mg/m³ 时，温度对风险的影响",
                  labels={'x': '海表温度 (°C)', 'y': '预测风险指数'})
    fig.add_vline(x=current_temp, line_dash="dash", line_color="red", annotation_text=f"当前温度 {current_temp}°C")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
