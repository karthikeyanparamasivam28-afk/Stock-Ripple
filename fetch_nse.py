import json, time, csv, os
import yfinance as yf

stocks_out = []
symbols = []

# equity.csv la irundhu Symbols edukkurom
try:
    with open('equity.csv', newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Un equity.csv la SYMBOL nu column irukkanum
            s = row.get('SYMBOL') or row.get('Symbol') or row.get('symbol')
            if s:
                symbols.append(s.strip() + ".NS")
except Exception as e:
    print("CSV Error:", e)
    symbols = ["【entity-RELIANCE¦canonical_name=RELIANCE】.NS","TCS.NS","JSWINFRA.NS","DABUR.NS"]

print(f"Total Symbols: {len(symbols)}")

# First 100 mattum - Free limit ku
for sym in symbols[:120]:
    try:
        t = yf.Ticker(sym)
        info = t.fast_info
        ltp = float(info.get('lastPrice') or 0)
        prev = float(info.get('previousClose') or ltp)
        if ltp > 100:
            chg = round(((ltp-prev)/prev*100), 2) if prev else 0
            stocks_out.append({"symbol": sym.replace(".NS",""), "ltp": round(ltp,2), "chgPct": chg})
    except:
        continue

# Sort - Periya Change mela
stocks_out = sorted(stocks_out, key=lambda x: abs(x['chgPct']), reverse=True)

data = {"timestamp": int(time.time()), "updated": time.strftime("%d %b %Y, %I:%M %p IST", time.localtime()), "stocks": stocks_out}
with open('nse_data.json','w') as f:
    json.dump(data, f, indent=2)
print(f"Saved {len(stocks_out)} stocks")
