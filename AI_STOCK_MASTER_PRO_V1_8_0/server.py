"""AI STOCK MASTER PRO demo historical data proxy. Standard library only.
Run: python server.py ; open http://127.0.0.1:8765 in a browser.
Yahoo chart endpoint is unofficial and may fail/change; NOT real-time.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone
import json, os, math, time, threading

CACHE = {}
CACHE_LOCK = threading.Lock()
CACHE_SECONDS = 900
SYMBOLS = {'005930.KS', '000660.KS', '035420.KS', 'NVDA', 'AAPL', 'MSFT'}
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path == '/api/health': return self.send_json(200,{'service':'AI STOCK MASTER PRO','version':'V1.8.0','status':'ok'})
        if parsed.path in ('/', '/index.html'):
            self.path='/index.html'
            return super().do_GET()
        if parsed.path != '/api/history': return self.send_json(404,{'error':'경로를 찾을 수 없습니다.'})
        symbol=parse_qs(parsed.query).get('symbol',[''])[0]
        if symbol not in SYMBOLS: return self.send_json(400,{'error':'지원하지 않는 종목입니다.'})
        with CACHE_LOCK:
            cached=CACHE.get(symbol)
            if cached and time.monotonic()-cached[0]<CACHE_SECONDS:
                return self.send_json(200,{**cached[1],'cached':True})
        try:
            url='https://query1.finance.yahoo.com/v8/finance/chart/'+quote(symbol)+'?range=2y&interval=1d'
            req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; StockMasterResearch/1.0)','Accept':'application/json'})
            with urlopen(req,timeout=10) as r: payload=json.load(r)
            obj=payload['chart']['result'][0]
            timestamps=obj.get('timestamp') or []
            quote_data=obj['indicators']['quote'][0]
            rows=[]
            for i,ts in enumerate(timestamps):
                values={k:quote_data.get(k,[None]*len(timestamps))[i] for k in ('open','high','low','close','volume')}
                if any(v is None or not isinstance(v,(int,float)) or not math.isfinite(v) for v in values.values()):continue
                if values['volume']<0 or values['high']<max(values['open'],values['close'],values['low']) or values['low']>min(values['open'],values['close'],values['high']):continue
                if min(values[k] for k in ('open','high','low','close'))<=0:continue
                rows.append({'date':datetime.fromtimestamp(ts,timezone.utc).strftime('%Y-%m-%d'),**values})
            if len(rows)<35: raise ValueError('유효한 거래일이 35개 미만입니다.')
            result={'symbol':symbol,'source':'Yahoo Finance 비공식 차트 API','rows':rows,'asof':datetime.now(timezone.utc).isoformat(),'cached':False}
            with CACHE_LOCK: CACHE[symbol]=(time.monotonic(),result)
            return self.send_json(200,result)
        except Exception as e:
            return self.send_json(502,{'error':'외부 시세 제공처에서 데이터를 가져오지 못했습니다 ('+type(e).__name__+'). 네트워크와 제공처 상태를 확인하세요.'})
    def send_json(self,status,payload):
        raw=json.dumps(payload,ensure_ascii=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('Open http://127.0.0.1:8765 (LAN access requires network/firewall setup)')
    ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8765'))),Handler).serve_forever()
