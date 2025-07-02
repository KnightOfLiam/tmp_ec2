import backtrader as bt

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.sma_fast = bt.indicators.SMA(period=5)
        self.sma_slow = bt.indicators.SMA(period=20)
    
    def next(self):
        # 双均线策略逻辑
        if self.sma_fast > self.sma_slow and not self.position:
            self.buy(size=100)  # 模拟买入
        elif self.sma_fast < self.sma_slow and self.position:
            self.sell(size=100)  # 模拟卖出

# 回测引擎配置
cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
cerebro.adddata(bt.feeds.PandasData(dataname=data))  # 加载yfinance数据
cerebro.broker.set_cash(100000)  # 初始资金10万
cerebro.run()  
cerebro.plot()  # 可视化结果
