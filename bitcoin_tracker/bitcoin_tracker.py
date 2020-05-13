import os
import sys
import logging.config
import yaml
import requests
import time
from datetime import datetime

#--------------------importing process configs and setting logger---------------------
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import properties.config as config

with open(config.log_config, 'r') as stream:
    log_config = yaml.load(stream, Loader=yaml.FullLoader)

logging.config.dictConfig(log_config)
logger = logging.getLogger('BitcoinTrackerTask')
#-------------------------------------------------------------------------------


def get_latest_bitcoin_price():
    
    response = requests.get(config.BITCOIN_API_URL)
    import  pprint as pp
    pp.pprint(response.text)
    response_json = response.json()
    # Convert the price to a floating point number
    print(response_json)
    return float(response_json[0]['price_usd'])


def post_ifttt_webhook(event, value):
    
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desired event
    ifttt_event_url = config.IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)

def main():

    logger.info("Starting main task")
    
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < config.BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', 
                               format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        # Sleep for 5 minutes 
        # (For testing purposes you can set it to a lower number)
        time.sleep(config.app_sleep)
    
    logger.info("Finished main task")

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


if __name__ == '__main__':
    main()
