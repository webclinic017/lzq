import akshare as ak
import functools
from core.common.config import Config
from core.common.logger import logger
from core.common.run_with_pool import run_with_pool
from core.common.utils import clock
from core.data.sql import safe_sessionmaker
from core.data.model import KData, Stock
from datetime import datetime
import pandas as pd
from typing import List


def download_individual_stock(symbol):
    """下载单个股票信息"""
    try:
        info = ak.stock_individual_info_em(symbol=symbol)
        logger.debug(f"下载 {symbol} 信息成功")
        return info
    except Exception as e:
        logger.error(f"下载 {symbol} 信息失败 {e}")
        return download_individual_stock(symbol)


@functools.lru_cache()
def download_stock_info_a_code_name():
    """下载股票代码和名称"""
    logger.debug("下载所有股票name和code")
    return ak.stock_info_a_code_name()


@functools.lru_cache()
@clock
def download_all_a_stock() -> List[Stock]:
    """下载所有股票信息"""
    logger.debug("开始下载所有股票")
    name_df = download_stock_info_a_code_name()
    results = run_with_pool(
        download_individual_stock,
        Config.RequestWorker,
        list(name_df["code"]),
        "下载所有股票信息",
    )

    stocks = []
    for result in results:
        info = {}
        for _, row in result.iterrows():
            info[row["item"]] = row["value"]
        stocks.append(
            Stock(
                code=info["股票代码"],
                name=info["股票简称"],
                launch_date=info["上市时间"],
                industry=info["行业"],
                total_capitalization=info["总市值"],
                flow_capitalization=info["流通市值"],
                total_capital=info["总股本"],
                flow_capital=info["流通股"],
            )
        )

    with safe_sessionmaker() as session:
        session.query(Stock).delete()
        session.add_all(stocks)
    logger.info("下载完成所有股票信息")
    return stocks


@functools.lru_cache()
def get_index_trading_infos():
    """获取交易日"""
    logger.debug("获取所有交易日信息")
    info = ak.stock_zh_index_daily(symbol="sh000001")
    info["datetime"] = pd.to_datetime(info["date"])
    return info.set_index("date", drop=False)


def download_a_stock_k_data(params):
    """下载单个股票行情数据"""
    try:
        (symbol, period, start_date, end_date, adjust) = params
        logger.debug(f"下载 {symbol} K线数据 {params}")
        k_data_pf = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            start_date=start_date,
            end_date=end_date,
            adjust=adjust,
        )
        k_data_dates = list(k_data_pf["日期"])
        start_datetime = pd.to_datetime(k_data_pf.loc[0, "日期"])
        end_datetime = pd.to_datetime(k_data_pf.loc[len(k_data_pf) - 1, "日期"])
        trading_infos = get_index_trading_infos()
        trading_info_dates = trading_infos.loc[
            (trading_infos["datetime"] >= start_datetime)
            & (trading_infos["datetime"] <= end_datetime)
        ]["date"].apply(lambda x: x.strftime("%Y-%m-%d"))

        k_data_pf = k_data_pf.set_index("日期", drop=False)

        # 设置不复权的标识
        adjust = adjust or "bfq"

        k_datas = []
        for date in trading_info_dates:
            if date in k_data_dates:
                # 交易日
                k_data = k_data_pf.loc[date]
                k_datas.append(
                    KData(
                        id=f"{symbol}_{period}_{adjust}_{date}",
                        code=symbol,
                        open=k_data["开盘"],
                        close=k_data["收盘"],
                        high=k_data["最高"],
                        low=k_data["最低"],
                        volume=k_data["成交量"],
                        amount=k_data["成交额"],
                        amplitude=k_data["振幅"],
                        ttm=k_data["涨跌幅"],
                        updown_price=k_data["涨跌额"],
                        turnover=k_data["换手率"],
                        period=period,
                        date=k_data["日期"],
                        adjust=adjust or "bfq",
                        is_trading=True,
                    )
                )
            else:
                # 停牌日
                k_data = k_datas[len(k_datas) - 1]
                k_datas.append(
                    KData(
                        id=f"{symbol}_{period}_{adjust}_{date}",
                        code=symbol,
                        open=k_data.close,
                        close=k_data.close,
                        high=k_data.close,
                        low=k_data.close,
                        volume=0,
                        amount=0,
                        amplitude=0,
                        ttm=0,
                        updown_price=0,
                        turnover=0,
                        period=period,
                        date=date,
                        adjust=adjust or "bfq",
                        is_trading=False,
                    )
                )
        # 入库
        with safe_sessionmaker() as session:
            session.query(KData).filter(
                KData.code == symbol, KData.period == period, KData.adjust == adjust,
            ).delete()
            session.add_all(k_datas)
        logger.debug(f"下载 {params} kdata 成功")
    except Exception as e:
        logger.error(f"下载 {params} kdata 失败 {e}")
        download_a_stock_k_data(params)


@clock
def download_all_a_stock_k_data(period="daily", adjust=""):
    """下载所有股票行情数据"""
    stocks = download_stock_info_a_code_name()
    codes = list(stocks["code"])
    params_list = []
    start_date = "19901219"
    end_date = datetime.now().strftime("%Y%m%d")
    for code in codes:
        params_list.append((code, period, start_date, end_date, adjust))
    run_with_pool(
        download_a_stock_k_data, Config.RequestWorker, params_list, "下载所有股票行情数据"
    )

    logger.info("下载完成所有股票行情数据")
