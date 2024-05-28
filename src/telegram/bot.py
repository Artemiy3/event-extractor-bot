import telebot
from config import config
import logging as log
# from extractor.event_extractor import EventExtractor
from model.event import Event, to_str
from extractor.stanford_extractor import extract_events
from telegram.messages import HELP_MESSAGE, START_MESSAGE, PROCESSING_MESSAGE


def convert_events(events: list[Event]) -> str:
    result = ""
    for i, event in enumerate(events):
        result += f"\n*Event {i + 1}\\:*\n" + to_str(event)

    return result


bot = telebot.TeleBot(config.get("TG_TOKEN"))
markup = telebot.types.InlineKeyboardMarkup()
# event_extractor = EventExtractor()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, START_MESSAGE)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, HELP_MESSAGE, reply_markup=markup, parse_mode='MarkdownV2')
    else:
        bot.send_message(message.from_user.id, PROCESSING_MESSAGE)
        try:
            response = convert_events(extract_events(message.text))
            if response:
                bot.send_message(message.from_user.id,  "*Here\\'s the list of events*\\! ⬇️\n\n" + response, reply_markup=markup, parse_mode='MarkdownV2')
            else:
                bot.send_message(message.from_user.id, "No events found in text.")
        except RuntimeError as error:
            log.error(error)
            bot.send_message(message.from_user.id, 'An error occurred, please try another text.')


bot.polling(none_stop=True, interval=0)
