# Modify this file if you want a different startup sequence, for example using
# a Webhook
from credentials import TOKEN

BASE_URL = '' 
HOST = ''
PORT = 0


def start_bot(updater):
    updater.start_polling()
    # updater.bot.setWebhook(webhook_url='https://%s/%s' % (BASE_URL, TOKEN))
    # updater.start_webhook(HOST, PORT, url_path=TOKEN)
