import spacy

nlp = spacy.load("en_core_web_sm")

text = "John ate an apple in the park yesterday."

doc = nlp(text)

events = []

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

        event = {"action": action,
                 "actor": actor,
                 "object_of_action": object_of_action,
                 "time": time,
                 "place": place}
        events.append(event)

for event in events:
    print(event)
