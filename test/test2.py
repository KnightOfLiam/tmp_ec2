import yfinance as yf

# 获取A股数据（通过港股通代码，例：赛力斯）
data = yf.download("601127.SS", period="1d", interval="5m")  # 5分钟K线（延迟15分钟）
print(data.tail())  # 查看最新数据（非实时）
