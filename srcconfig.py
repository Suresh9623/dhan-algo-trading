import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # धन API credentials
    DHAN_CLIENT_ID = os.getenv('DHAN_CLIENT_ID')
    DHAN_ACCESS_TOKEN = os.getenv('DHAN_ACCESS_TOKEN')
    
    # Trading rules
    MAX_DAILY_LOSS_PERCENT = 20
    MAX_TRADES_PER_DAY = 10
    TRADING_START_TIME = "09:25:00"
    TRADING_END_TIME = "15:00:00"
    
    # API URLs
    DHAN_API_URL = "https://api.dhan.co"
    DHAN_WS_URL = "wss://api.dhan.co"
    
    # Server settings
    PORT = int(os.getenv('PORT', 10000))