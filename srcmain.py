from flask import Flask, jsonify, request
import schedule
import time
import threading
from datetime import datetime
from .risk_manager import RiskManager
from .dhan_api import DhanAPI
from .config import Config

app = Flask(__name__)
risk_manager = RiskManager(initial_capital=100000)  # Starting capital
dhan_api = DhanAPI()

# Global state
trading_active = False

@app.route('/')
def home():
    return jsonify({
        "status": "Dhan Algo Trading System",
        "version": "1.0.0",
        "rules": {
            "max_daily_loss": "20%",
            "trading_hours": "9:25 AM - 3:00 PM",
            "max_trades_per_day": 10
        }
    })

@app.route('/status', methods=['GET'])
def get_status():
    status = risk_manager.get_status()
    status["current_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status["trading_active"] = trading_active
    return jsonify(status)

@app.route('/place_order', methods=['POST'])
def place_order():
    if not trading_active:
        return jsonify({"error": "Trading not active"}), 400
    
    # Check risk rules
    can_trade, message = risk_manager.can_trade()
    if not can_trade:
        return jsonify({"error": message}), 400
    
    order_data = request.json
    
    # Place order through Dhan API
    try:
        result = dhan_api.place_order(order_data)
        
        # Update risk manager
        risk_manager.increment_trade_count()
        
        return jsonify({
            "success": True,
            "order_id": result.get("orderId"),
            "message": "Order placed successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/exit_all', methods=['POST'])
def exit_all_positions():
    """Exit all positions (for 3PM or loss limit)"""
    try:
        positions = dhan_api.get_positions()
        
        for position in positions:
            dhan_api.exit_position(
                symbol=position['symbol'],
                exchange=position['exchange']
            )
        
        return jsonify({"success": True, "message": "All positions exited"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def schedule_checks():
    """Scheduled tasks"""
    # 3:00 PM - Auto exit all positions
    schedule.every().day.at("15:00").do(auto_exit_at_3pm)
    
    # 9:25 AM - Enable trading
    schedule.every().day.at("09:25").do(enable_trading)
    
    # 9:15 AM - Pre-market checks
    schedule.every().day.at("09:15").do(pre_market_checks)
    
    # 3:30 PM - Reset for next day
    schedule.every().day.at("15:30").do(reset_daily)

def auto_exit_at_3pm():
    """Auto exit all positions at 3:00 PM"""
    global trading_active
    trading_active = False
    
    # Exit all positions
    exit_all_positions()
    
    print(f"[{datetime.now()}] 3:00 PM - All positions exited")

def enable_trading():
    """Enable trading at 9:25 AM"""
    global trading_active
    trading_active = True
    print(f"[{datetime.now()}] 9:25 AM - Trading enabled")

def pre_market_checks():
    """Pre-market checks at 9:15 AM"""
    # Reset risk manager
    risk_manager.reset_daily()
    print(f"[{datetime.now()}] 9:15 AM - Daily reset completed")

def reset_daily():
    """Reset at 3:30 PM for next day"""
    global trading_active
    trading_active = False
    print(f"[{datetime.now()}] 3:30 PM - System reset for next day")

def run_scheduler():
    """Run scheduler in background thread"""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start scheduler thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("Dhan Algo Trading System Started")
    print(f"Server running on port {Config.PORT}")
    
    app.run(host='0.0.0.0', port=Config.PORT, debug=False)