import fire



class LazyQuant():
    '''A way to lazy quant'''
    def downloaddata():
        '''下载所有数据：股票信息、股票历史行情'''
        from lzq.data.download import download_a_stock_k_data, download_all_a_stock

        download_all_a_stock()
        download_a_stock_k_data()


if __name__ == '__main__':
    fire.Fire(LazyQuant)