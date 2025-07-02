import yfinance as yf
import backtrader as bt
import pandas as pd

# 1. 获取并转换数据
raw_data = yf.download("601127.SS", period="1d", interval="5m")
data = raw_data.copy()
data.columns = [col.lower() for col in data.columns]  # 取第一级列名并小写
data = data.drop('adj close', axis=1, errors='ignore')  # 删除无效列

# 2. 创建策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=5)
        self.sma_slow = bt.indicators.SMA(period=20)
    
    def next(self):
        if self.sma_fast > self.sma_slow and not self.position:
            self.buy(size=100)
        elif self.sma_fast < self.sma_slow and self.position:
            self.sell(size=100)

# 3. 配置引擎
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata(bt.feeds.PandasData(
    dataname=data,
    open='open',
    high='high',
    low='low',
    close='close',
    volume='volume'
))
cerebro.broker.set_cash(100000)
cerebro.run()
cerebro.plot()
