import yfinance as yf
import streamlit as st


st.write(" # Simple Stock Price App")

tickerSymbol = 'GOOGL'

tickeData = yf.Ticker(tickerSymbol)

tickerDf = tickeData.history(period='id', start='2010-5-31', end='2020-5-31')

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)