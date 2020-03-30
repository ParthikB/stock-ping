from twilio.rest import Client as twilio_client
from binance.client import Client as binance_client
import yfinance as yf

from datetime import datetime
import time, os

def get_crypto_price():
	API = os.environ.get('BINANCE_API')
	KEY = os.environ.get('BINANCE_SECRET_KEY')
	
	client = binance_client(API, KEY)

	# Getting the average price of the COIN in $
	btc_price  = client.get_avg_price(symbol=f'BTCUSDT')
	btc_price  = round(float(btc_price['price']), 2)

	xrp_price  = client.get_avg_price(symbol='XRPBTC')
# 	xrp_price  = round(float(xrp_price['price'])*74, 2)
	xrp_price  = float(xrp_price['price'])


	return btc_price, xrp_price


def get_stock_price():
	stock 	   = yf.Ticker('YESBANK.NS')
	return stock.history('max')["Close"][-1]



def notify_me(action, msg=None):
	
	API = os.environ.get('TWILIO_API')
	KEY = os.environ.get('TWILIO_KEY')
	
	client = twilio_client(API, KEY)

	if action.lower() == 'call':
		action = client.calls.create(
						url='http://demo.twilio.com/docs/voice.xml',
						from_='+15592065130',
						to='+917428432678',
					 )
	elif action.lower() == 'msg':
		
		for number in ['+917428432678']: # parthik

			action = client.messages \
		    .create(
		         body=f'''Price Updates from Parthik Papa..!
-------------------------------------
{msg}''',
		         from_='+15592065130',
		         to=number,
		     )

	action.sid


def cur_time():
	return datetime.now().strftime('%H:%M:%S')

def convert_to_time(t):
	sec = t % 60
	t -= sec
	min = t // 60
	return f'{min}:{sec}'
########################################################################


while True:

	print('Fetching Details..')
	btc, xrp = get_crypto_price()
	stock = get_stock_price()
	info = f'''Current BTC Price   : {btc} $
Current XRP Price   : {'{0:.10f}'.format(xrp)} BTC
Current Stock Price : Rs. {stock}
-------------------------------------
Last Updated        : {cur_time()}'''
	
	print(info, '\n')

	if btc<5800 or xrp>13 or xrp<12 or stock<25 or stock>30:
		print('Pinging you, time to make some money! Hell yeah!')
		notify_me(action='msg', msg=info)
		print(f'Notified! ({cur_time()})', '\n')
		for t in range(1800)[::-1]: # 30 minutes break
			time.sleep(1)
			print(f'Re-initializing server in {convert_to_time(t)} m ...')

	time.sleep(20)
