import logging
import boto3
import botocore
import json
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
    preference_data,
    numeric_cols,
    LAMBDA_FUNCTION
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
        await update.callback_query.answer()
    if query == 'No':
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Ending current operation...'
        )
        return ConversationHandler.END
    if preference_key_count > 0:
        if last_key in numeric_cols:
            new_preference[last_key] = int(query)
        elif last_key == 'district':
            new_preference[last_key] = query.split(' ')[0]
        else:
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
                text += 'Type /continue to run your scraper'
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text
            )
            return ConversationHandler.END
    category = list(preference_options.keys())[preference_key_count]
    preference_key_count += 1
    text = 'Choose - ' + ' '.join(category.split('_')).lower() + '\n'
    if category == 'property_type_code':
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
            text += f'{i + 1}. {option}\n'
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


async def schedule_scraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # get frequency from db
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Scraper scheduled'
    )
    context.job_queue.run_once(
        callback=invoke_scraper,
        when=0,
        # interval=3600*new_preference['job_frequency_hours'],
        data=json.dumps(new_preference),
        chat_id=update.effective_message.chat_id,
        # first=0
    )


async def invoke_scraper(context: CallbackContext):
    config = botocore.config.Config(
        read_timeout=900,
        connect_timeout=900,
        retries={"max_attempts": 0}
    )
    session = boto3.Session()
    lambda_client = session.client(
        service_name='lambda',
        region_name='ap-southeast-1',
        config=config
    )
    invoke_response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION,
        InvocationType='RequestResponse',
        Payload=context.job.data
    )
    response = json.loads(invoke_response['Payload'].read())
    print(response)
    if response['statusCode'] == 500:
        text = json.loads(response['body'])
    else:
        links = json.loads(response['body'])
        if not links:
            text = 'No new listings found\n'
        else:
            text = 'New listings found!\n'
            for link in links:
                text += f'\n{link[0]}\n{link[1]}\n'
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=text
    )


async def create_new_preference():
    return True


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global new_preference, preference_key_count
    new_preference = preference_data.copy()
    preference_key_count = 0
    await update.message.reply_text('Operation cancelled...')
    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[list(handlers.keys())],
        one_time_keyboard=True
    )
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    scraper_handler = CommandHandler('continue', schedule_scraper)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
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
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(scraper_handler)
    application.add_handler(conv_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
