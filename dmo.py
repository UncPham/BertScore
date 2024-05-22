import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import plotly.express as px

# Hàm mô phỏng dự đoán giá
def predict_price(asset):
    return round(np.random.uniform(0.95, 1.05) * 100, 2)

# Tạo DataFrame mẫu
data = {
    'Asset': ['BTC-USDT', 'ETH-USDT', 'XRP-USDT', 'SOL-USDT', 'DOT-USDT', 'ADA-USDT', 'BNB-USDT', 'TRX-USDT', 'DOGE-USDT', 'LTC-USDT'],
    '17:00': [predict_price(asset) for asset in range(10)],
    '18:00': [predict_price(asset) for asset in range(10)],
    '18:10:53': [predict_price(asset) for asset in range(10)],
    '19:00': [predict_price(asset) for asset in range(10)],
    'Accuracy 4 weeks': [f"{np.random.uniform(50, 60):.1f}%" for _ in range(10)],
    'Stake 24h': [f"{np.random.randint(50000, 120000)} (±{np.random.uniform(1, 5):.2f}%)" for _ in range(10)],
    'Action': ['BUY' if np.random.rand() > 0.5 else 'SELL' for _ in range(10)]
}

df = pd.DataFrame(data)

# Streamlit app
st.title('Giá tiền điện tử')

# Sidebar for user inputs
st.sidebar.header('Tùy chọn người dùng')
update_interval = st.sidebar.selectbox('Khoảng thời gian cập nhật', ['1 phút', '1 giờ'])

# Multiselect for choosing assets to display on the chart
selected_assets = st.sidebar.multiselect(
    'Chọn tài sản để hiển thị trên biểu đồ',
    options=df['Asset'].unique(),
    default=['BTC-USDT', 'ETH-USDT', 'XRP-USDT']
)

# Define a color map for the 'Action' column
def color_rows(row):
    color = 'background-color: yellow' if row['Action'] == 'BUY' else 'background-color: red'
    return [color] * len(row)

# Apply the color map to the entire DataFrame
styled_df = df.style.apply(color_rows, axis=1)

# Display the styled DataFrame
st.write("### Dự đoán hiện tại")
st.dataframe(styled_df)

# Add options to simulate live updates
if st.button('Cập nhật dự đoán'):
    df['17:00'] = [predict_price(asset) for asset in range(10)]
    df['18:00'] = [predict_price(asset) for asset in range(10)]
    df['18:10:53'] = [predict_price(asset) for asset in range(10)]
    df['19:00'] = [predict_price(asset) for asset in range(10)]
    styled_df = df.style.apply(color_rows, axis=1)
    st.write(styled_df)

# Add a chart for better visualization
st.write("### Giá theo thời gian")

# Create data for the chart with daily intervals for the past 7 days
time_now_utc = datetime.now(pytz.utc)
time_now_vn = time_now_utc.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))

# Generate data for the past 7 days
time_intervals_daily = [time_now_vn - timedelta(days=i) for i in range(7)][::-1]

data_daily = {
    'Time': [t.strftime('%Y-%m-%d %H:%M') for t in time_intervals_daily],
    'BTC-USDT': [predict_price('BTC-USDT') for _ in time_intervals_daily],
    'ETH-USDT': [predict_price('ETH-USDT') for _ in time_intervals_daily],
    'XRP-USDT': [predict_price('XRP-USDT') for _ in time_intervals_daily]
}

df_daily = pd.DataFrame(data_daily)

# Ensure selected assets exist in the chart_data
selected_assets = [asset for asset in selected_assets if asset in df_daily.columns]

# Filter chart data based on selected assets
chart_data = df_daily[['Time'] + selected_assets]

# Calculate moving average for selected assets
for asset in selected_assets:
    chart_data[f'{asset}_MA'] = chart_data[asset].rolling(window=2).mean()

# Sort the data by time to ensure the latest time is on the right
chart_data = chart_data.sort_values(by='Time')

# Plot the chart using Plotly
fig = px.line(chart_data, x='Time', y=selected_assets + [f'{asset}_MA' for asset in selected_assets],
              labels={'value': 'Giá', 'variable': 'Loại tiền điện tử'})

# Update layout to fit the chart
fig.update_layout(autosize=True, margin=dict(l=20, r=20, t=30, b=20))

# Enable range slider for 7 days and scroll zoom
fig.update_xaxes(rangeslider_visible=True)
fig.update_layout(xaxis=dict(rangeselector=dict(buttons=list([
    dict(count=1, label="1d", step="day", stepmode="backward"),
    dict(count=7, label="7d", step="day", stepmode="backward"),
    dict(step="all")
])),
    rangeslider=dict(visible=True),
    type="date"
))

# Enable scroll zoom
fig.update_layout(hovermode='x unified', dragmode='pan', xaxis=dict(fixedrange=False))

st.plotly_chart(fig)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: ;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    .stDataFrame {
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)