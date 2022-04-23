from concurrent.futures import ThreadPoolExecutor
import sys
from time import sleep
from core.common.utils import every
from core.common.logger import logger
from tqdm import tqdm
import threading


def run_with_pool(worker, max_works, paramses, desc):
    pbar = tqdm(total=len(paramses), desc=desc)
    quite = False

    def _worer(params):
        if not quite:
            logger.debug(f"[{threading.currentThread()}] 开始执行")
            r = worker(params)
            pbar.update(1)
            return r
        else:
            logger.debug("程序正在退出")

    with ThreadPoolExecutor(max_workers=max_works) as pool:
        fs = [pool.submit(_worer, params) for params in paramses]

        try:
            while not every(fs, lambda x: x.done()):
                sleep(1)
            return [f.result() for f in fs]
        except KeyboardInterrupt as e:
            logger.info("\r\n退出程序...")
            quite = True
            [f.cancel() for f in fs]
            pool.shutdown()
            sys.exit(1)
            raise e
