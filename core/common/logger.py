# -*- coding: UTF-8 -*-

import logging
from core.common.config import Config
from os import path
from datetime import datetime


def get_logger(name="Default"):
    '''设置日志logger'''
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt=Config.LogFormat)

    # 控制台输出
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # 日志文件输出 logs/2022-02-02.log
    log_file = f'{datetime.now().strftime("%Y-%m-%d")}.log'
    fh = logging.FileHandler(path.join(Config.LogDirPath, log_file),
                             encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # 设置级别
    logger.setLevel(Config.LogLevel)
    return logger


logger = get_logger()