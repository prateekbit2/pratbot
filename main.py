from telegram.ext import Updater, InlineQueryHandler,  CommandHandler, MessageHandler, Filters
from nsetools import Nse
import logging
import os
import sys

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        updater.start_polling()
        updater.idle()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

def quote(update, context):
    text_caps = ' '.join(context.args).upper()
    nse = Nse()
    quote = nse.get_quote(text_caps)
    text = ""
    text = text + "Symbol - " + quote["symbol"] + "\n"
    text = text + "Open - " + str(quote["open"]) + "\n"
    text = text + "High - " + str(quote["dayHigh"]) + "\n"
    text = text + "Low - " + str(quote["dayLow"]) + "\n"
    text = text + "Prev. Close - " + str(quote["previousClose"]) + "\n"
    text = text + "AveragePrice - " + str(quote["averagePrice"]) + "\n"
    text = text + "Change - " + str(quote["change"]) + "\n"
    text = text + "Change% - " + str(quote["pChange"]) + "\n"
    text = text + "YearHigh - " + str(quote["high52"]) + "\n"
    text = text + "YearLow - " + str(quote["low52"]) + "\n"
    text = text + "TotalTradedVolume - " + str(quote["totalTradedVolume"]) + "\n"
    text = text + "LastPrice - " + str(quote["lastPrice"]) + "\n"
    text = text + "ClosePrice - " + str(quote["closePrice"]) + "\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    # quote_handler = CommandHandler('quote', quote)
    # dispatcher.add_handler(quote_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    run(updater)