# import spacy
# from model.event import Event
# from spacy import displacy
#
#
# class EventExtractor:
#     def __init__(self):
#         self.nlp = spacy.load("en_core_web_sm")
#
#     def extract_events(self, text: str) -> list[Event]:
#         doc = self.nlp(text)
#
#         events = []
#
#         for sent in doc.sents:
#             for token in sent:
#                 if token.pos_ == "VERB" or token.pos_ == "AUX":
#                     if "xcomp" in token.dep_:
#                         continue
#
#                     action = None
#                     actor = None
#                     object_of_action = None
#                     time = None
#                     place = None
#
#                     if token.pos_ == "AUX":
#                         if "aux" in token.dep_:
#                             anc = token.ancestors.__next__()
#                             if anc.pos_ == "NOUN":
#                                 action = token.text + " " + anc.text
#
#                                 for child in token.children:
#                                     if "subj" in child.dep_:
#                                         actor = child.text
#                                         break
#
#                                 token = anc
#                         else:
#                             continue
#                     else:
#                         action = token.lemma_
#
#                     for child in token.children:
#                         if "xcomp" in child.dep_:
#                             sub_child = child.children.__next__()
#                             if "aux" in sub_child.dep_:
#                                 action += " " + sub_child.text
#                             action += " " + child.text
#
#                     for child in token.children:
#                         if "subj" in child.dep_:
#                             actor = child.text
#                             break
#
#                     for child in token.children:
#                         if "obj" in child.dep_:
#                             object_of_action = child.text
#                             for sub_child in child.children:
#                                 if "compound" in sub_child.dep_:
#                                     object_of_action = sub_child.text + " " + object_of_action
#                             break
#
#                     for ent in sent.ents:
#                         if ent.label_ == "DATE":
#                             time = ent.text
#                             break
#
#                     for ent in sent.ents:
#                         if ent.label_ == "LOC":
#                             place = ent.text
#                             break
#
#                     for child in token.children:
#                         if "prep" in child.dep_:
#                             for sub_child in child.children:
#                                 if "pobj" in sub_child.dep_ and "NOUN" or "PROPN" in sub_child.pos_:
#                                     place = sub_child.text
#
#                     if object_of_action:
#                         action += " " + object_of_action
#                     event = Event(actor, action, time, place)
#
#                     events.append(event)
#
#         return events
#
#     def show_deps(self, text):
#         doc = self.nlp(text)
#         displacy.serve(doc, style="tag", port=8080)
#
#
# # event_extractor = EventExtractor()
# # event_extractor.show_deps("Three cats are running after a mouse in the street.")
