from twilio.rest import Client as twilio_client
from binance.client import Client as binance_client
import yfinance as yf

from datetime import datetime
import time

def get_crypto_price():
	api_key    = 'jfdgMTk4LEnYl54Lto18zWAvyYS2GEOfvfwfnifaQawFE9TIMUlZnjCPqubWKWoP'
	secret_key = 'H0UfJS8hCj13a3StI3IgZ46C0AfkaUS6zwf7s0bK8bDv1cqP8x49kHe4M4phVfnI'

	client = binance_client(api_key, secret_key)

	# Getting the average price of the COIN in $
	btc_price  = client.get_avg_price(symbol=f'BTCUSDT')
	btc_price  = round(float(btc_price['price']), 2)

	xrp_price  = client.get_avg_price(symbol='XRPUSDT')
	xrp_price  = round(float(xrp_price['price'])*74, 2)

	return btc_price, xrp_price


def get_stock_price():
	stock 	   = yf.Ticker('YESBANK.NS')
	return stock.history('max')["Close"][-1]



def notify_me(action, msg=None):
	ACC = 'AC243598673f6cf8a6fe4ad5ae15d0271d'
	KEY = 'ef642d4b863ff00b0378c06625364eb2'


	client = twilio_client(ACC, KEY)

	if action.lower() == 'call':
		action = client.calls.create(
						url='http://demo.twilio.com/docs/voice.xml',
						from_='+15592065130',
						to='+917428432678'
					 )
	elif action.lower() == 'msg':
		action = client.messages \
	    .create(
	         body=f'''Price Updates..!
-------------------------------------
{msg}''',
	         from_='+15592065130',
	         to='+917428432678'
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
Current XRP Price   : Rs. {xrp}
Current Stock Price : Rs. {stock}
-------------------------------------
Last Updated        : {cur_time()}'''
	
	print(info, '\n')

	if btc<6100 or xrp>13 or xrp<10 or stock<35 or stock>100:
		print('Pinging you, time to make some money! Hell yeah!')
		notify_me(action='msg', msg=info)
		print(f'Notified! ({cur_time()})', '\n')
		for t in range(600)[::-1]: # 10 minutes break
			time.sleep(1)
			print(f'Re-initializing server in {convert_to_time(t)} m ...')

	time.sleep(20)
