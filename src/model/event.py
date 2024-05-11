class Event:
    def __init__(self, actor: str, action: str, time: str, place: str):
        self.actor = actor
        self.action = action
        self.time = time
        self.place = place

    def __str__(self):
        return (f"Actor:{self.actor}\n"
                f"Action:{self.action}\n"
                f"Time:{self.time}\n"
                f"Place:{self.place}\n")
