class Event:
    def __init__(self, action: str, actor: str, object_of_action: str, time: str, place: str):
        self.action = action
        self.actor = actor
        self.object_of_action = object_of_action
        self.time = time
        self.place = place
