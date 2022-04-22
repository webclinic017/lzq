# encoding=utf-8
from os import path, getcwd
from configparser import ConfigParser

from lzq.common.utils import mkdir_if_not_exists

_base_path = getcwd()
_config_path = path.join(_base_path, '.config.ini')

_config = ConfigParser()
_config.read(_config_path, encoding='UTF-8')


class Config():
    '''配置'''
    DB_URL = _config.get("db", 'url')

    # 日志
    LogDirPath = path.join(_base_path, _config.get("log", "output"))
    LogLevel = _config.get("log", "level")
    LogFormat = _config.get("log", "format", raw=True)

mkdir_if_not_exists(Config.LogDirPath)