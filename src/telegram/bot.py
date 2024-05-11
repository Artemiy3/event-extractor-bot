import telebot
from config import config
from extractor.event_extractor import EventExtractor
from model.event import Event


def convert_events(events: list[Event]) -> str:
    result = ""
    for i, event in enumerate(events):
        result += f"\nEvent {i + 1}:\n" + str(event)

    return result


bot = telebot.TeleBot(config.get("TG_TOKEN"))
event_extractor = EventExtractor()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Enter a text to extract events from")
    else:
        bot.send_message(message.from_user.id, convert_events(event_extractor.extract_events(message.text)))


bot.polling(none_stop=True, interval=0)
