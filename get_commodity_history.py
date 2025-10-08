import yfinance as yf
import json
from datetime import datetime

# Daftar simbol dan nama buat chart
symbols = {
    "BZ=F": "Brent Crude Oil",
    "CL=F": "WTI Crude Oil",
    "GC=F": "Gold Futures",
    "SI=F": "Silver Futures",
    "HG=F": "Copper Futures",
    "NG=F": "Natural Gas Futures"
}

output = {
    "source": "yahoo-finance",
    "updated": datetime.now().isoformat(),
    "period": "1mo",
    "interval": "1d",
    "data": []
}

for sym, name in symbols.items():
    print(f"Fetching {sym} ({name})...")
    try:
        df = yf.download(sym, period="1mo", interval="1d", progress=False)
        df = df.reset_index()

        records = [
            {
                "date": r["Date"].strftime("%Y-%m-%d"),
                "open": round(r["Open"], 2),
                "high": round(r["High"], 2),
                "low": round(r["Low"], 2),
                "close": round(r["Close"], 2)
            }
            for _, r in df.iterrows()
        ]

        output["data"].append({
            "symbol": sym,
            "name": name,
            "records": records
        })
    except Exception as e:
        print(f"❌ Error {sym}: {e}")

# Simpan hasil
with open("commodity_history.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("✅ Done! Saved to commodity_history.json")
