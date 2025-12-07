import requests
import json
from .config import Config

class DhanAPI:
    def __init__(self):
        self.base_url = Config.DHAN_API_URL
        self.headers = {
            'access-token': Config.DHAN_ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }
    
    def get_margin(self):
        """Get available margin"""
        url = f"{self.base_url}/margins"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def place_order(self, order_data):
        """Place new order"""
        url = f"{self.base_url}/orders"
        response = requests.post(url, headers=self.headers, json=order_data)
        return response.json()
    
    def get_positions(self):
        """Get current positions"""
        url = f"{self.base_url}/positions"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def cancel_order(self, order_id):
        """Cancel order"""
        url = f"{self.base_url}/orders/{order_id}"
        response = requests.delete(url, headers=self.headers)
        return response.json()
    
    def exit_position(self, symbol, exchange):
        """Exit position"""
        url = f"{self.base_url}/positions"
        data = {
            "symbol": symbol,
            "exchange": exchange,
            "transaction_type": "SELL"  # or "BUY" for short positions
        }
        response = requests.delete(url, headers=self.headers, json=data)
        return response.json()