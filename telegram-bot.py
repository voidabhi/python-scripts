from flask import Flask, request

import telegram

# CONFIG
TOKEN    = ''
HOST     = '' # Same FQDN used when generating SSL Cert
PORT     = 8443
CERT     = 'path/to/ssl/server.crt'
CERT_KEY = 'path/to/ssl/server.key'

bot = telegram.Bot(TOKEN)
app = Flask(__name__)
context = (CERT, CERT_KEY)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True))
    bot.sendMessage(chat_id=update.message.chat_id, text='Hello, there')

    return 'OK'


def setWebhook():
    bot.setWebhook(webhook_url='https://%s:%s/%s' % (HOST, PORT, TOKEN),
                   certificate=open(CERT, 'rb'))

if __name__ == '__main__':
    setWebhook()

    app.run(host='0.0.0.0',
            port=PORT,
            ssl_context=context,
            debug=True)
