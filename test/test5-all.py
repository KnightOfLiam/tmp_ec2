import yfinance as yf
import time

# 获取A股数据（通过港股通代码，例：赛力斯）
data = yf.download("601127.SS", period="1d", interval="5m")  # 5分钟K线（延迟15分钟）
print(data.tail())  # 查看最新数据（非实时）


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



# while True:
#     latest_data = yf.download("601127.SS", period="1d", interval="5m", prepost=True)  # 获取最新5分钟K线
#     current_price = latest_data['Close'][-1]  # 最新价格（延迟）
    
#     # 根据策略生成信号（示例）
#     if generate_signal(latest_data) == "BUY":
#         print(f"[模拟下单] 买入601127.SS @ {current_price}")
#     elif generate_signal(latest_data) == "SELL":
#         print(f"[模拟下单] 卖出601127.SS @ {current_price}")
    
#     time.sleep(300)  # 每5分钟检查一次（与K线周期同步）
