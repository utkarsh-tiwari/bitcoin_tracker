import os

process_folder_name = 'bitcoin_tracker'
properties_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
processing_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), process_folder_name, 'processing')
log_config = os.path.join(properties_folder, 'logging_config.yml')
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/{your-IFTTT-key}'
ifttt_webhook = 'https://maker.ifttt.com/trigger/bitcoin_price/with/key/pNFz70A4WFNFqqIpfYK6jmieiWN3m8VtDEDPioaKaLe'
BITCOIN_PRICE_THRESHOLD = 10000
app_sleep = 3600