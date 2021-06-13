from vnpy.trader.constant import (Exchange, Interval)
import pandas as pd
import pdb
from vnpy.trader.database import database_manager
from vnpy.trader.object import BarData
import datetime


def move_df_to_mongodb(imported_data:pd.DataFrame,collection_name:str):
    bars = []
    start = None
    count = 0

    for row in imported_data.itertuples():
        d = datetime.datetime.strptime(row.datetime, "%Y-%m-%d %H:%M:%S")
        bar = BarData(
              symbol=row.symbol,
              exchange=row.exchange,
              datetime=d,
              interval=row.interval,
              volume=row.volume,
              open_price=row.open,
              high_price=row.high,
              low_price=row.low,
              close_price=row.close,
              open_interest=row.open_interest,
              gateway_name="DB",
        )
        bars.append(bar)

        # do some statistics
        count += 1
        if not start:
            start = bar.datetime
    end = bar.datetime

    # pdb.set_trace()
    # insert into database
    database_manager.save_bar_data(bars)
    print(f'Insert Bar: {count} from {start} - {end}')


if __name__ == "__main__":
    src = '/tmp/data.csv'
    ex = Exchange.HUOBI
    vt = 'eth'

    # 读取需要入库的csv文件，该文件是用gbk编码
    imported_data = pd.read_csv(src, encoding='UTF-8')
    # 将csv文件中 `市场代码`的 SC 替换成 Exchange.SHFE SHFE
    # imported_data['市场代码'] = Exchange.SHFE
    imported_data['市场代码'] = ex
    # 增加一列数据 `inteval`，且该列数据的所有值都是 Interval.MINUTE
    imported_data['interval'] = Interval.MINUTE
    # 明确需要是float数据类型的列
    pdb.set_trace()
    float_columns = ['开', '高', '低', '收', '成交量', '持仓量']
    for col in float_columns:
        imported_data[col] = imported_data[col].astype('float')
    imported_data['时间'] = imported_data['时间']
    # 因为没有用到 成交额 这一列的数据，所以该列列名不变
    imported_data.columns = ['exchange', 'symbol', 'datetime', 'open', 'high', 'low', 'close', 'volume', '成交额', 'open_interest', 'interval']
    imported_data['symbol'] = vt
    # pdb.set_trace()
    move_df_to_mongodb(imported_data, ex)
