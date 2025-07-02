# fix plot pic
import matplotlib
matplotlib.use('Agg')  # 设置为非交互式后端

import yfinance as yf
import backtrader as bt
import pandas as pd

raw_data = yf.download("601127.SS", period="1d", interval="5m", ignore_tz=True)
data = raw_data.copy()
data.columns = [col[0] for col in data.columns]
data = data.drop('adj close', axis=1, errors='ignore')

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=5)
        self.sma_slow = bt.indicators.SMA(period=20)

    def next(self):
        if self.sma_fast > self.sma_slow and not self.position:
            self.buy(size=100)
        elif self.sma_fast < self.sma_slow and self.position:
            self.sell(size=100)

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

# 保存图像到文件（而非显示）
import matplotlib.pyplot as plt
plt.switch_backend('Agg')  # 再次确认后端
cerebro.plot(iplot=False, filename='backtrader_plot.png')
