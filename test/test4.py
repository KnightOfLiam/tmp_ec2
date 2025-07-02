while True:
    latest_data = yf.download("601127.SS", period="1d", interval="5m", prepost=True)  # 获取最新5分钟K线
    current_price = latest_data['Close'][-1]  # 最新价格（延迟）
    
    # 根据策略生成信号（示例）
    if generate_signal(latest_data) == "BUY":
        print(f"[模拟下单] 买入601127.SS @ {current_price}")
    elif generate_signal(latest_data) == "SELL":
        print(f"[模拟下单] 卖出601127.SS @ {current_price}")
    
    time.sleep(300)  # 每5分钟检查一次（与K线周期同步）
