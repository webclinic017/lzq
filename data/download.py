import akshare as ak
import functools
from data.utils import clock
from .sql import safe_sessionmaker, Stock
from concurrent.futures import ThreadPoolExecutor


def download_individual_stock(symbol):
    try:
        return ak.stock_individual_info_em(symbol=symbol)
    except Exception as e:
        print(f"下载 {symbol} 失败 {e}")
        return download_individual_stock(symbol)


@functools.lru_cache()
def download_stock_info_a_code_name():
    return ak.stock_info_a_code_name()


@clock
def download_all_a_stock():
    name_df = download_stock_info_a_code_name()
    results = []
    with ThreadPoolExecutor(max_workers=100) as pool:
        results = pool.map(download_individual_stock, tuple(name_df['code']))

    stocks = []
    for result in results:
        info = {}
        for _, row in result.iterrows():
            info[row['item']] = row["value"]
        stocks.append(
            Stock(
                code=info['股票代码'],
                name=info["股票简称"],
                launch_date=info["上市时间"],
                industry=info["行业"],
                total_capitalization=info["总市值"],
                flow_capitalization=info["流通市值"],
                total_capital=info["总股本"],
                flow_capital=info["流通股"],
            ))

    with safe_sessionmaker() as session:
        session.query(Stock).delete()
        session.add_all(stocks)
    print("下载所有信息")
