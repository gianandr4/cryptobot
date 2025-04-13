import numpy as np
from utils.logger import get_logger
from dataclasses import dataclass
from typing import Tuple

logger = get_logger(__name__)

@dataclass
class RiskParameters:
    max_drawdown: float = 0.10  # 10%
    stop_loss: float = 0.05      # 5%
    take_profit: float = 0.15    # 15%

class RiskManager:
    def __init__(self, config: dict):
        self.params = RiskParameters(
            max_drawdown=config['risk']['max_drawdown_pct'] / 100,
            stop_loss=config['risk']['stop_loss_pct'] / 100,
            take_profit=config['risk']['take_profit_pct'] / 100
        )
        self.peak_balance = 0
        self.current_balance = 0
        
    def update_balance(self, new_balance: float) -> Tuple[bool, float]:
        """Returns (is_risk_triggered, drawdown_pct)"""
        self.current_balance = new_balance
        self.peak_balance = max(self.peak_balance, new_balance)
        
        drawdown = (self.peak_balance - new_balance) / self.peak_balance
        risk_triggered = drawdown >= self.params.max_drawdown
        
        if risk_triggered:
            logger.warning(f"Risk threshold breached! Drawdown: {drawdown*100:.2f}%")
            
        return risk_triggered, drawdown
    
    def calculate_position_size(self, volatility: float) -> float:
        """Dynamic position sizing based on volatility"""
        base_size = 0.01  # 1% of capital
        adj_size = base_size * (1 - np.tanh(volatility * 10))
        return max(adj_size, 0.001)  # Never less than 0.1%