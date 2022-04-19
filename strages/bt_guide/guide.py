import backtrader as bt
import os
import datetime


class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def __init__(self):
        print(self.data0)
        print(self.data)
        print(self.datas)
        self.dataclose = self.datas[0].close
        self.order = None
        self.sma = bt.indicators.MovingAverageSimple(
            period=self.params.maperiod)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def next(self):
        self.log(f"close {self.dataclose[0]}")

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] > self.sma[0]:
                self.log(f"buy create {self.dataclose[0]}")
                self.order = self.buy()
        else:
            if self.dataclose[0] < self.sma[0]:
                self.log(f"sell create {self.dataclose[0]}")
                self.order = self.sell()

    def notify_trade(self, trade: bt.Trade):
        if not trade.isclosed:
            return
        self.log(f"operation profit, gross {trade.pnl} net {trade.pnlcomm}")

    def notify_order(self, order: bt.Order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"buy executed price:{order.executed.price}, value:{order.executed.value}, comm:{order.executed.comm}")
            elif order.issell():
                self.log(
                    f"sell executed price:{order.executed.price}, value:{order.executed.value}, comm:{order.executed.comm}")
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f"order canceled/margin/rejected")
        self.order = None


cerebro = bt.Cerebro()
cerebro.addstrategy(TestStrategy, maperiod=5)
datapath = os.path.join(os.getcwd(), "orcl-1995-2014.txt")
data = bt.feeds.GenericCSVData(
    dataname=datapath,
    fromdate=datetime.datetime(2000, 1, 1),
    todate=datetime.datetime(2000, 3, 31),
    dtformat=('%Y-%m-%d'),
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=6,
    openinterest=5,
    reverse=False)
cerebro.adddata(data)
cerebro.addsizer(bt.sizers.FixedSize, stake=10)
cerebro.broker.setcommission(commission=0.001)
cerebro.broker.set_cash(100000.0)
result = cerebro.run()
# print(result)
# cerebro.plot()
