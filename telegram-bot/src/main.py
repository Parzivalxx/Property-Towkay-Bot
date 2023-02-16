import logging
from credentials import BOT_TOKEN
from project_config import handlers
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f'Hello {update.message.chat.first_name}, Property Towkay is here to help you find your next dream home\n\n'
    text += 'Here are the commands that you can run:\n'
    for handle, description in handlers.items():
        text += f'{handle}: {description}\n'
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   parse_mode='MarkdownV2',
                                   reply_markup=reply_markup)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = '*Here are the commands that you can run:*\n'
    for handle, description in handlers.items():
        text += f'{handle}: {description}\n'
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=text,
                                   parse_mode='MarkdownV2',
                                   reply_markup=reply_markup)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Sorry, I didn't understand that command.",
                                   reply_markup=reply_markup)

async def new(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # check for existing preference
    preference = get_existing_preference()
    if preference:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Existing preference exists, please delete it first',
                                       reply_markup=reply_markup)
    preference = get_new_preference()
    # user inputs a new preference
    if not preference:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='No new preference added',
                                       reply_markup=reply_markup)



def get_existing_preference():
    return

def get_new_preference():
    return

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    keyboard = [list(handlers.keys())]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
