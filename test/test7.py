import yfinance as yf
import backtrader as bt
import pandas as pd

# 1. 获取数据（忽略FutureWarning）
raw_data = yf.download("601127.SS", period="1d", interval="5m", ignore_tz=True)

# 2. 正确转换列名（处理MultiIndex元组）
# 关键修正：使用col获取元组的第一个元素（如'Open'），然后转换为小写
data = raw_data.copy()
data.columns = [col.lower() for col in data.columns]  # 修正点：使用col

# 3. 删除不需要的列
data = data.drop('adj close', axis=1, errors='ignore')

# 4. 验证列名格式
print("处理后的列名:", data.columns.tolist())
# 应输出: ['open', 'high', 'low', 'close', 'volume']

# 5. 创建策略
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=5)
        self.sma_slow = bt.indicators.SMA(period=20)
    
    def next(self):
        if self.sma_fast > self.sma_slow and not self.position:
            self.buy(size=100)
        elif self.sma_fast < self.sma_slow and self.position:
            self.sell(size=100)

# 6. 配置引擎
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
