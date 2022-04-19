import backtrader as bt
import akshare as ak
import pandas as pd


class ThreeMa(bt.Strategy):
    params = (("fast", 10), ("slow", 30), ("safe", 60))

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f"{dt.isoformat()}, {txt}")

    def __init__(self) -> None:
        self.dataclose = self.data.close
        self.ma_fast = bt.indicators.SMA(self.dataclose,
                                         period=self.params.fast)
        self.ma_slow = bt.indicators.SMA(self.dataclose,
                                         period=self.params.slow)
        self.ma_safe = bt.indicators.SMA(self.dataclose,
                                         period=self.params.safe)
        co = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)
        self.buy_sig = bt.indicators.And(self.dataclose > self.ma_safe,
                                         co == 1)
        self.sell_sig = bt.indicators.Or(self.dataclose < self.ma_safe,
                                         co == -1)
        self.order = None

    def next(self):
        if self.order:
            return

        dataclose = self.dataclose[0]
        buy_sig = self.buy_sig[0]
        sell_sig = self.sell_sig[0]

        if buy_sig and not self.position:
            self.log(f"创建买单 {dataclose}")
            self.order = self.buy()
        elif sell_sig and self.position:
            self.log(f"创建卖单 {dataclose}")
            self.order = self.sell()

    def notify_order(self, order: bt.Order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"买入价格 {order.executed.price}, 买入 {order.executed.value} 共 {order.executed.size} 手"
                )
            elif order.issell():
                self.log(
                    f"卖出价格 {order.executed.price}, 卖出 {order.executed.value} 共 {order.executed.size} 手"
                )
            if self.position:
                self.log(
                    f"持仓 {self.position.size}, 成本价: {self.position.price}, 当前价: {self.position.adjbase}"
                )
            else:
                self.log("未持仓")
        self.order = None


def start():
    raw_data = ak.stock_zh_a_hist(symbol="000001",
                                  period="daily",
                                  start_date="20100101",
                                  end_date='20211231',
                                  adjust="hfq")
    raw_data = raw_data.set_index("日期", drop=False)
    raw_data["日期"] = pd.to_datetime(raw_data["日期"])
    stock_data = pd.DataFrame(
        {
            "datetime": raw_data["日期"],
            "open": raw_data["开盘"],
            "high": raw_data["最高"],
            "low": raw_data["最低"],
            "close": raw_data["收盘"],
            "volume": raw_data["成交量"],
            "openinterest": 0
        },
        index=raw_data["日期"])

    data = bt.feeds.PandasData(dataname=stock_data)

    cerebro = bt.Cerebro()

    # 添加策略
    cerebro.addstrategy(ThreeMa)
    # 添加数据
    cerebro.adddata(data=data)
    # 设置初始资金
    cerebro.broker.setcash(1000000.0)
    # 设置佣金
    cerebro.broker.setcommission(commission=0.0003)
    # 设置滑点
    cerebro.broker.set_slippage_perc(perc=0.0001)
    # 设置每笔交易手数
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
    # 回撤曲线
    cerebro.addobserver(bt.observers.DrawDown)
    # 收益曲线
    cerebro.addobserver(bt.observers.TimeReturn)

    start = cerebro.broker.getvalue()
    # 执行回测
    cerebro.run()
    end = cerebro.broker.getvalue()
    print(f"初始资金 {start}, 结束资金 {end}, 收益率 {(end- start) /start }")
    # 绘图
    cerebro.plot()


if __name__ == '__main__':
    start()
