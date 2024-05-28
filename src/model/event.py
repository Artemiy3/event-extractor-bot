import telebot


class Event:
    def __init__(self, actor: str, action: str, time: str, place: str):
        self.actor = actor
        self.action = action
        self.time = time
        self.place = place

    def __str__(self):
        return to_str(self)


def to_str(event: Event):
    return (f"*Who\\:* {telebot.formatting.escape_markdown(event.actor)}\n"
            f"*Action\\:* {telebot.formatting.escape_markdown(event.action)}\n"
            f"*When\\:* {telebot.formatting.escape_markdown(event.time)}\n"
            f"*Where\\:* {telebot.formatting.escape_markdown(event.place)}\n")
