import logging
from credentials import BOT_TOKEN

# from Preference import Preference
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ForceReply
)
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)
from project_config import (
    handlers,
    preference_options,
    preference_data
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

preference_key_count = 0
new_preference = None
GET_NEW_PREFERENCE, GET_NUMERIC_INPUT = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f'Hello {update.message.chat.first_name}' + \
        'Property Towkay is here to help you find your next dream home\n\n'
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
    preference = await get_existing_preference()
    if preference:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Existing preference exists, please delete it first',
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    # user inputs a new preference
    buttons = [
        [
            InlineKeyboardButton('Yes', callback_data='Yes'),
            InlineKeyboardButton('No', callback_data='No')
        ]
    ]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='No existing preference, would you like to create a new preference?',
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    global new_preference
    new_preference = preference_data.copy()
    new_preference['user_id'] = update.message.from_user.id
    return GET_NEW_PREFERENCE


async def get_existing_preference():
    return


async def get_new_preference(update: Update, context: CallbackContext):
    global preference_key_count, new_preference
    last_key = list(preference_options.keys())[preference_key_count - 1]
    if not preference_options[last_key]:
        query = update.message.text
    else:
        query = update.callback_query.data
        update.callback_query.answer()
    if query == 'No':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Ending current operation...'
        )
        return ConversationHandler.END
    if preference_key_count > 0:
        new_preference[last_key] = query
        if preference_key_count == len(preference_options.keys()):
            preference_key_count = 0
            create_success = await create_new_preference()
            if not create_success:
                text = 'Error saving preference...'
            else:
                text = 'Successfully created preference!\n'
                for category, val in new_preference.items():
                    text += f'{category}: {val}\n'
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )
            return ConversationHandler.END
    category = list(preference_options.keys())[preference_key_count]
    preference_key_count += 1
    text = 'Choose - ' + ' '.join(category.split('_')).lower() + '\n'
    if category == 'property_code':
        options = preference_options[category][new_preference.get('property_type')]
    else:
        options = preference_options[category]
    if not options:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=ForceReply(True)
        )
        return GET_NUMERIC_INPUT
    else:
        buttons = []
        for i, option in enumerate(options):
            text += f'{i + 1}: {option}\n'
            buttons.append([
                InlineKeyboardButton(
                    text=option,
                    callback_data=option
                )
            ])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    return GET_NEW_PREFERENCE


async def get_numeric_input(update: Update, context):
    reply = update.message.text
    await update.message.reply_text(
        text=reply
    )
    return GET_NEW_PREFERENCE


async def create_new_preference():
    return True


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Operation cancelled...')
    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    keyboard = [list(handlers.keys())]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new', new)],
        states={
            GET_NEW_PREFERENCE: [
                CommandHandler('cancel', cancel),
                CallbackQueryHandler(callback=get_new_preference)
            ],
            GET_NUMERIC_INPUT: [
                CommandHandler('cancel', cancel),
                MessageHandler(
                    filters=(filters.TEXT & ~filters.COMMAND),
                    callback=get_new_preference
                )
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
