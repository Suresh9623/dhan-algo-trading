from datetime import datetime, time
import json

class RiskManager:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.daily_pnl = 0
        self.trade_count = 0
        self.max_trades = 10
        self.max_daily_loss = initial_capital * 0.20
        
        # Trading hours
        self.start_time = time(9, 25, 0)
        self.end_time = time(15, 0, 0)
        
        # State tracking
        self.trading_enabled = True
        self.blocked = False
        
    def can_trade(self):
        """Check all trading rules"""
        if self.blocked:
            return False, "Trading blocked due to rule violation"
        
        # Rule 1: Time check
        if not self.is_trading_hours():
            return False, "Outside trading hours"
        
        # Rule 2: Loss check
        if self.daily_pnl <= -self.max_daily_loss:
            self.blocked = True
            return False, "Daily loss limit reached"
        
        # Rule 3: Trade count check
        if self.trade_count >= self.max_trades:
            self.blocked = True
            return False, "Max trades reached"
        
        return True, "OK"
    
    def is_trading_hours(self):
        """Check if current time is within trading hours"""
        current_time = datetime.now().time()
        return self.start_time <= current_time <= self.end_time
    
    def update_pnl(self, pnl):
        """Update P&L and check loss limit"""
        self.daily_pnl += pnl
        self.current_capital += pnl
        
        # Auto block if loss limit reached
        if self.daily_pnl <= -self.max_daily_loss:
            self.blocked = True
            return "STOP_TRADING"
        
        return "CONTINUE"
    
    def increment_trade_count(self):
        """Increment trade count"""
        self.trade_count += 1
        if self.trade_count >= self.max_trades:
            self.blocked = True
    
    def reset_daily(self):
        """Reset daily counters (call this at market close)"""
        self.daily_pnl = 0
        self.trade_count = 0
        self.blocked = False
        # Carry forward capital
        self.initial_capital = self.current_capital
        self.max_daily_loss = self.initial_capital * 0.20
    
    def get_status(self):
        """Get current risk status"""
        return {
            "current_capital": self.current_capital,
            "daily_pnl": self.daily_pnl,
            "trade_count": self.trade_count,
            "max_trades": self.max_trades,
            "max_daily_loss": self.max_daily_loss,
            "trading_enabled": self.trading_enabled and not self.blocked,
            "blocked": self.blocked,
            "loss_percentage": (abs(self.daily_pnl) / self.initial_capital * 100) if self.daily_pnl < 0 else 0
        }