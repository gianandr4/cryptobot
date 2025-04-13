
class RiskManager:
    def __init__(self):
        self.max_drawdown = 0.1  # 10%
        self.balance = 1000  # Example initial balance
    
    def check_stop_loss(self):
        # Check if balance drops more than max_drawdown percentage
        current_balance = self.get_balance()
        if (self.balance - current_balance) / self.balance > self.max_drawdown:
            print("Stop-loss triggered!")
            return True
        return False

    def get_balance(self):
        # Placeholder for getting current balance from Pionex API
        return self.balance  # This should be fetched from the exchange via the API
