import tushare as ts
from vnpy.trader.object import HistoryRequest,BarData
from vnpy.trader.constant import Exchange
from datetime import  datetime
class TushareData:
    def __init__(self):
        ts.set_token('你的token')
        return
    def exchange_bond(self,exchange:Exchange):
        if exchange.value == "SHFE":
            return "SHF"
        elif exchange.value == "CZCE":
            return  "ZCE"
        else :
            return  exchange.value
        
    def tuquery(self,req:HistoryRequest):
        symbol = req.symbol
        exchange = req.exchange
        interval = req.interval
        start = req.start.strftime('%Y%m%d')
        end = req.end.strftime('%Y%m%d')
        tcode = f'{symbol}'+'.'+ self.exchange_bond(exchange)
        pro = ts.pro_api();
        df = pro.fut_daily(ts_code= tcode, start_date= start, end_date= end)
        data: List[BarData] = []

        if df is not None:
            for ix, row in df.iterrows():
                date = datetime.strptime(row.trade_date,'%Y%m%d')
                bar = BarData(
                    symbol=symbol,
                    exchange=exchange,
                    interval=interval,
                    datetime=date,
                    open_price=row["open"],
                    high_price=row["high"],
                    low_price=row["low"],
                    close_price=row["close"],
                    volume=row["amount"],
                    gateway_name="TU"
                )
                print(bar)
                data.append(bar)
        return data

tusharedata = TushareData()
