import telebot
from config import config
from extractor.event_extractor import EventExtractor
from model.Event import Event

event_extractor = EventExtractor()
bot = telebot.TeleBot(config.get("TG_TOKEN"))


def convert_events(events: list[Event]) -> str:
    result = ""
    for i, event in enumerate(events):
        result += (
            f"\nEvent {i}:\n"
            f"action: {event.action}\n"
            f"actor: {event.actor}\n"
            f"object_of_action: {event.object_of_action}\n"
            f"time: {event.time}\n"
            f"place: {event.place}\n"
        )

    return result


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Enter a text to extract events from")
    else:
        bot.send_message(message.from_user.id, convert_events(event_extractor.extract_events(message.text)))


bot.polling(none_stop=True, interval=0)
