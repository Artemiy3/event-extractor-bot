import spacy
from model.Event import Event


class EventExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_events(self, text: str) -> list[Event]:
        # text = "John ate an apple in the park yesterday and I decided to go home."

        doc = self.nlp(text)

        events = []

        # for sent in doc.sents:
        #     sent

        for token in doc:
            if token.pos_ == "VERB":
                action = token.lemma_

                actor = None
                for child in token.children:
                    if "subj" in child.dep_:
                        actor = child.text
                        break

                object_of_action = None
                for child in token.children:
                    if "obj" in child.dep_:
                        object_of_action = child.text
                        break

                time = None
                for ent in doc.ents:
                    if ent.label_ == "DATE":
                        time = ent.text
                        break

                place = None
                for ent in doc.ents:
                    if ent.label_ == "LOC":
                        place = ent.text
                        break

                event = Event(action, actor, object_of_action, time, place)

                events.append(event)
        return events
