import csv, json, datetime
import yfinance as yf

stocks=[]
with open('equity.csv') as f:
    reader = csv.DictReader(f)
    symbols = [r['SYMBOL'] for r in reader][:300]

# Batch ah edukkrom - 50 50 ah
for i in range(0, len(symbols), 50):
    batch = symbols[i:i+50]
    tickers = " ".join([s+".NS" for s in batch])
    try:
        data = yf.download(tickers, period="2d", group_by='ticker', progress=False, threads=True)
        for s in batch:
            try:
                df = data[s+".NS"] if len(batch)>1 else data
                if len(df) < 2: continue
                ltp = float(df['Close'].iloc[-1])
                prev = float(df['Close'].iloc[-2])
                if ltp < 100: continue
                chg = round(((ltp-prev)/prev)*100, 2)
                stocks.append({"symbol":s,"ltp":round(ltp,2),"chgPct":chg})
            except: continue
    except: continue
    print(f"Done {i} -> Total {len(stocks)}")

stocks = sorted(stocks, key=lambda x: x['symbol'])
out = {"updated": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"), "count": len(stocks), "stocks": stocks}
with open('nse_data.json','w') as f: json.dump(out, f)
print(f"FINAL: {len(stocks)} stocks saved")
