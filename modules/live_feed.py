import yfinance as yf

def get_live_data(symbols=["^GSPC","GC=F","CL=F","USDINR=X"]):
    """
    Returns latest market indicators:
    S&P 500, Gold, Oil, USD/INR
    """
    data = {}
    for sym in symbols:
        ticker = yf.Ticker(sym)
        info = ticker.history(period="1d", interval="1m")
        data[sym] = info['Close'].iloc[-1] if not info.empty else None
    return data
