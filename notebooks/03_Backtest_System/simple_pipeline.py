def run_backtest(prices, signal, initial_capital=100000, cost_bps=0.001):
    # 1. 對齊與填充
    signal = signal.reindex(prices.index).fillna(0)
    
    # 2. 計算資產本身的回報
    asset_returns = prices.pct_change().fillna(0)
    
    # 3. 策略毛報酬 (Gross Returns)
    # 昨天的訊號決定今天的曝險
    strategy_returns_gross = signal.shift(1) * asset_returns
    
    # === 4. 核心修改：計算交易成本 ===
    # 邏輯：計算 signal 的變化量 (Turnover)
    # 買入 (0->1): diff=1, 賣出 (1->0): diff=-1, 反手 (1->-1): diff=-2
    # 我們只在乎變動的幅度 (絕對值)
    trades_turnover = signal.diff().abs()  # 填空: 計算差分
    
    # 成本拖累 (Cost Drag)
    # 這裡簡化假設：成本是扣在報酬率上的 (近似解)
    cost_drag = trades_turnover * cost_bps / 10000 # 填空: 填入費率參數
    
    # 5. 策略淨報酬 (Net Returns)
    strategy_returns_net = strategy_returns_gross - cost_drag
    
    # 6. 計算淨值 (Equity Curve)
    # 填空: 從本金開始，累積乘上 (1 + net_returns)
    equity_curve = initial_capital * (1 + strategy_returns_net).cumprod() # 填空: 累積連乘
    
    # 7. 績效結算
    total_return = (equity_curve.iloc[-1] / initial_capital) - 1
    peak = equity_curve.cummax()
    drawdown = (equity_curve - peak) / peak
    max_drawdown = drawdown.min()
    
    return {
        'equity_curve': equity_curve,
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'total_costs': cost_drag.sum() # 讓我們看看總共付了多少手續費
    }