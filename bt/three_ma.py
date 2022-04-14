import backtrader as bt
import akshare as ak
import datetime


class ThreeMa(bt.Strategy):
    '''三均线策略
        1. 价格在safe上才买入，safe下卖出
        2. fast上穿slow买入
        3. fast下穿slow卖出
    '''

    params = (
        ("fast", 10),
        ("slow", 20),
        ("safe", 30)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def __init__(self) -> None:
        self.dataclose = self.data.close
        self.ma_fast = bt.indicators.SMA(
            self.dataclose, period=self.params.fast)
        self.ma_slow = bt.indicators.SMA(
            self.dataclose, period=self.params.slow)
        self.ma_safe = bt.indicators.SMA(
            self.dataclose, period=self.params.safe)
        co = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)
        self.buy_sig = bt.indicators.And(
            self.dataclose > self.ma_safe, co == 1)
        self.sell_sig = bt.indicators.Or(
            self.dataclose < self.ma_safe, co == -1)
        self.order = None

    def next(self):
        dataclose = self.dataclose[0]
        buy_sig = self.buy_sig[0]
        sell_sig = self.sell_sig[0]
        # self.log(f"close {dataclose}, buy_sig {buy_sig}, sell_sig {sell_sig}")
        if self.order:
            return

        if buy_sig and not self.position:
            self.log(f"create buy {dataclose}")
            self.order = self.order_target_percent(target=1)
        elif sell_sig and self.position:
            self.log(f"create sell {dataclose}")
            self.order = self.sell()
        if self.position:
            self.log(
                f"持仓 {self.position.size}, 成本价: {self.position.price}, 当前价: {self.position.adjbase}, 盈亏: {self.position.size}")
        else:
            self.log("未持仓")

    def notify_order(self, order: bt.Order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"buy price {order.executed.price}, value {order.executed.value}")
            elif order.issell():
                self.log(
                    f"sell price {order.executed.price}, value {order.executed.value}")
        self.order = None


def start():
    data = bt.feeds.GenericCSVData(
        dataname="/Users/zhupeng/Code/git/quant/bt/pa.csv",
        fromdate=datetime.datetime(2010, 1, 1),
        todate=datetime.datetime(2021, 12, 31),
        dtformat=('%Y-%m-%d'),
        datetime=1,
        open=2,
        high=4,
        low=5,
        close=3,
        volume=6,
        openinterest=11,
        reverse=False)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(ThreeMa)
    cerebro.adddata(data=data)
    cerebro.broker.set_cash(100000.0)
    cerebro.broker.setcommission(0.01)
    cerebro.addsizer(bt.sizers.FixedSize, stake=50)
    print(f"start {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"end {cerebro.broker.getvalue()}")

    cerebro.plot()


start()
