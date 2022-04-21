from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine('sqlite:///stock.db', echo=False)
Session = sessionmaker(bind=engine)
ModelBase = declarative_base()


@contextmanager
def safe_sessionmaker(session=Session()):
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Stock(ModelBase):
    __tablename__ = 'stock'
    code = Column(String, primary_key=True)  # 股票代码
    name = Column(String)  # 简称
    launch_date = Column(String)  # 上市日期
    industry = Column(String)  # 行业
    total_capitalization = Column(Float)  # 总市值
    flow_capitalization = Column(Float)  # 流通市值
    total_capital = Column(Float)  # 总股本
    flow_capital = Column(Float)  # 流通股本

Stock.metadata.create_all(engine)


class KData(ModelBase):
    __tablename__ = 'k_data'
    id = Column(String, primary_key=True)
    code = Column(Integer)  # 股票代码
    open = Column(Float)  # 开盘价
    close = Column(Float)  # 收盘价
    high = Column(Float)  # 最高价
    low = Column(Float)  # 最低价
    volume = Column(Integer)  # 成交量
    amount = Column(Float)  # 成交额
    amplitude = Column(Float)  # 振幅
    ttm = Column(Float)  # 涨跌幅
    updown_price = Column(Float)  # 涨跌额
    turnover = Column(Float)  # 换手率
    period = Column(String)  # 周期：daily、weekly、monthly
    date = Column(String)  # 时间
    adjust = Column(String)  # 复权，qfq、hfq、bfq
    is_trading = Column(Boolean) # 是否处于交易日

 
KData.metadata.create_all(engine)


class Cache(ModelBase):
    __tablename__ = 'cache'
    id = Column(String, primary_key=True)
    value = Column(String)


Cache.metadata.create_all(engine)
