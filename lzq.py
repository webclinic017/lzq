# -*- coding: UTF-8 -*-

import importlib
import fire
from core.common.logger import logger
import os


class LazyQuant:
    '''A way to lazy quant'''

    def downloadall(self, period="daily", adjust="hfq"):
        '''下载所有数据：股票信息、股票历史行情'''
        from core.data.download import download_all_a_stock_k_data, download_all_a_stock

        download_all_a_stock()
        download_all_a_stock_k_data(period=period, adjust=adjust)

    def download(self, code, period="daily", adjust="hfq"):
        '''下载单个股票数据。period取值daily、weekly、monthly。adjust取值qfq、hfq或bfq'''
        from core.data.download import download_individual_stock, download_a_stock_k_data
        from datetime import datetime

        download_individual_stock(code)

        start_date = "19901219"
        end_date = datetime.now().strftime("%Y%m%d")
        download_a_stock_k_data((code, period, start_date, end_date, adjust))

    def list(self):
        '''查看策略列表'''
        strageies = os.listdir(f"stragies")
        index = 1
        for file in strageies:
            if not os.path.isfile(os.path.join("stragies", file)):
                continue
            stragey = file.split(".")[0]
            m = importlib.import_module(f"stragies.{stragey}")
            print(f"策略{index}:\t{m.start.__doc__}\t<{stragey}>")
            index += 1

    def run(self, stragey):
        '''运行策略'''
        m = importlib.import_module(f"stragies.{stragey}")
        logger.info(f"引入 {stragey} 模块")
        m.start()


if __name__ == '__main__':
    fire.Fire(LazyQuant)
