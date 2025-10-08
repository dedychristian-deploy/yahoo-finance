import yfinance as yf
import json
from datetime import datetime

symbols = {
    "Gold": "GC=F",
    "CrudeOil": "CL=F",
    "Silver": "SI=F",
    "NaturalGas": "NG=F",
    "Copper": "HG=F"
}

result = {
    "source": "yahoo-finance",
    "updated": datetime.now().isoformat(),
    "period": "1mo",
    "interval": "1d",
    "data": []
}

for name, symbol in symbols.items():
    try:
        df = yf.download(symbol, period="1mo", interval="1d", progress=False)
        if not df.empty:
            data = [
                {
                    "date": str(idx.date()),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"])
                }
                for idx, row in df.iterrows()
            ]
            result["data"].append({
                "name": name,
                "symbol": symbol,
                "records": data
            })
        else:
            print(f"⚠️ No data for {symbol}")
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")

with open("commodity_history.json", "w") as f:
    json.dump(result, f, indent=2)
