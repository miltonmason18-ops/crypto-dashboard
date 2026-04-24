import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Crypto Dashboard", page_icon="📈", layout="wide")

st.title("📈 Crypto Price Dashboard")
st.caption("Live crypto prices powered by CoinGecko API")

# --- Coin Selection ---
col1, col2 = st.columns([1, 2])
with col1:
    coin = st.selectbox(
        "Choose a coin",
        ["bitcoin", "ethereum", "solana", "dogecoin", "cardano"],
        format_func=lambda x: x.capitalize()
    )
with col2:
    days = st.slider("Days of history", 7, 90, 30)

# --- Fetch Data ---
@st.cache_data(ttl=300)
def get_coin_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    r = requests.get(url, params=params)
    data = r.json()
    
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # Get current stats
    url2 = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    stats = requests.get(url2).json()
    
    return df, stats

try:
    df, stats = get_coin_data(coin, days)
    
    # --- Metrics ---
    price = stats['market_data']['current_price']['usd']
    change_24h = stats['market_data']['price_change_percentage_24h']
    market_cap = stats['market_data']['market_cap']['usd']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Market Cap", f"${market_cap/1e9:.2f}B")
    col2.metric("24h Change", f"{change_24h:.2f}%")
    col3.metric("Current Price", f"${price:,.2f}")
    
    st.divider()
    
    # --- Portfolio Tracker ---
    st.subheader("💼 My Portfolio Value")
    st.caption("Enter how many coins you own to see total USD + Naira value")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        btc_amount = st.number_input("Bitcoin (BTC)", min_value=0.0, value=0.1, step=0.001, format="%.4f")
    with col2:
        eth_amount = st.number_input("Ethereum (ETH)", min_value=0.0, value=1.0, step=0.01, format="%.3f")
    with col3:
        sol_amount = st.number_input("Solana (SOL)", min_value=0.0, value=10.0, step=0.1, format="%.2f")
    
    # Get live prices for portfolio coins
    @st.cache_data(ttl=300)
    def get_prices():
        coins = "bitcoin,ethereum,solana"
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coins}&vs_currencies=usd"
        return requests.get(url).json()
    
    prices = get_prices()
    
    btc_value = btc_amount * prices['bitcoin']['usd']
    eth_value = eth_amount * prices['ethereum']['usd'] 
    sol_value = sol_amount * prices['solana']['usd']
    
    total_usd = btc_value + eth_value + sol_value
    total_ngn = total_usd * 1600  # USD to NGN rate
    
    if total_usd > 0:
        c1, c2 = st.columns(2)
        c1.metric("Total Portfolio Value", f"${total_usd:,.2f}")
        c2.metric("Value in Naira", f"₦{total_ngn:,.0f}")
        
        portfolio_df = pd.DataFrame({
            'Coin': ['Bitcoin', 'Ethereum', 'Solana'],
            'Value USD': [btc_value, eth_value, sol_value]
        })
        portfolio_df = portfolio_df[portfolio_df['Value USD'] > 0]
        
        fig_pie = px.pie(portfolio_df, values='Value USD', names='Coin',
                         title='Portfolio Breakdown', hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()
    
    # --- Price Chart ---
    st.subheader(f"{coin.capitalize()} Price - Last {days} Days")
    fig = px.line(df, x='date', y='price', 
                  labels={'date': 'Date', 'price': 'Price (USD)'})
    fig.update_layout(hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("Data: CoinGecko API | Built with Streamlit")

except Exception as e:
    st.error("Error loading data. CoinGecko API might be rate limited. Try again in 1 minute.")
    st.caption(f"Error: {e}")
