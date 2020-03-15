from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler


from secrets import TELEGRAM_API_TOKEN
from minfin_scrapper import CurrencyScrapper
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)


def start_handler(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please choose currency:", reply_markup=reply_markup)


def button_click_handler(update: Update, context: CallbackContext):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))


def callback_minute(context: CallbackContext):
    context.bot.send_message(
        chat_id=context.job.context["chat_id"], text="One message every minute"
    )


def init_job_hanlder(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id, text="Setting a timer for 1 minute!"
    )

    context.job_queue.run_repeating(
        callback_minute,
        interval=60,
        first=0,
        context={"chat_id": update.message.chat_id},
    )


timer_handler = CommandHandler("timer", init_job_hanlder)
updater.dispatcher.add_handler(timer_handler)


start_handler = CommandHandler("start", start_handler)
updater.dispatcher.add_handler(start_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button_click_handler))


if __name__ == "__main__":
    # updater.start_polling()

    # updater.idle()

    scrapper = CurrencyScrapper()
    print(scrapper.get_usd_currency())

