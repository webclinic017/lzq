import pandas as pd
from sqlalchemy import Column, String, Boolean, Float
from lzq.data.sql import ModelBase, engine, safe_sessionmaker


class Mixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def query_all(cls, *query):
        with safe_sessionmaker() as session:
            raw_list = session.query(cls).filter(*query).all()
            result = []
            for item in raw_list:
                result.append(item.to_dict())
            return pd.DataFrame(result)


class Stock(ModelBase, Mixin):
    '''股票'''
    __tablename__ = 'stock'
    code = Column(String(16), primary_key=True)  # 股票代码
    name = Column(String(16))  # 简称
    launch_date = Column(String(10))  # 上市日期
    industry = Column(String(16))  # 行业
    total_capitalization = Column(Float)  # 总市值
    flow_capitalization = Column(Float)  # 流通市值
    total_capital = Column(Float)  # 总股本
    flow_capital = Column(Float)  # 流通股本


Stock.metadata.create_all(engine)


class KData(ModelBase, Mixin):
    '''K线，日/周/月'''
    __tablename__ = 'k_data'
    id = Column(String(32), primary_key=True)
    code = Column(String(16))  # 股票代码
    open = Column(Float)  # 开盘价
    close = Column(Float)  # 收盘价
    high = Column(Float)  # 最高价
    low = Column(Float)  # 最低价
    volume = Column(Float)  # 成交量
    amount = Column(Float)  # 成交额
    amplitude = Column(Float)  # 振幅
    ttm = Column(Float)  # 涨跌幅
    updown_price = Column(Float)  # 涨跌额
    turnover = Column(Float)  # 换手率
    period = Column(String(8))  # 周期：daily、weekly、monthly
    date = Column(String(16))  # 时间
    adjust = Column(String(4))  # 复权，qfq、hfq、bfq
    is_trading = Column(Boolean)  # 是否处于交易日


KData.metadata.create_all(engine)
