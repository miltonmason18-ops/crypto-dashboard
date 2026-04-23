import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("Live Crypto Dashboard")
st.caption("Real-time Bitcoin & Ethereum prices from CoinGecko API")

@st.cache_data(ttl=60)
def get_crypto_data(coin_id, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    r = requests.get(url, params=params)
    data = r.json()
    
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["MA7"] = df["price"].rolling(24*7).mean()
    return df

coin = st.sidebar.selectbox("Select Coin", ["bitcoin", "ethereum"])
days = st.sidebar.slider("Days of History", 1, 90, 7)

df = get_crypto_data(coin, days)

col1, col2, col3 = st.columns(3)
current_price = df["price"].iloc[-1]
price_change = df["price"].iloc[-1] - df["price"].iloc[-2]
col1.metric(f"{coin.capitalize()} Price", f"${current_price:,.2f}")
col2.metric("24h Change", f"${price_change:,.2f}", f"{price_change/current_price*100:.2f}%")
col3.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))

fig = go.Figure()
fig.add_trace(go.Scatter(x=df["date"], y=df["price"], name="Price", line=dict(color="#00D1FF")))
fig.add_trace(go.Scatter(x=df["date"], y=df["MA7"], name="7-Day MA", line=dict(color="#FF6B6B", dash="dash")))
fig.update_layout(title=f"{coin.capitalize()} Price - Last {days} Days", xaxis_title="Date", yaxis_title="Price USD")
st.plotly_chart(fig, use_container_width=True)

st.caption("Data updates every 60 seconds. Built with Python + Streamlit")
