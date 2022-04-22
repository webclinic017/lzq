import fire


class LazyQuant:
    '''A way to lazy quant'''
    def downloadall(self):
        '''下载所有数据：股票信息、股票历史行情'''
        from lzq.data.download import download_all_a_stock_k_data, download_all_a_stock

        download_all_a_stock()
        download_all_a_stock_k_data()

    def download(self, code, period="daily", adjust=""):
        '''下载单个股票数据。period取值daily、weekly、monthly。adjust取值qfq、hfq或空'''
        from lzq.data.download import download_individual_stock, download_a_stock_k_data
        from datetime import datetime

        download_individual_stock(code)

        start_date = "19901219"
        end_date = datetime.now().strftime("%Y%m%d")
        download_a_stock_k_data((code, period, start_date, end_date, adjust))


if __name__ == '__main__':
    fire.Fire(LazyQuant)