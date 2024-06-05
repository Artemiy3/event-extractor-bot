# from extractor.event_extractor import EventExtractor
from bert_score import score

from extractor.stanford_extractor import extract_events
from model.event import Event


def convert_event(event: Event) -> str:
    return f"{event.actor}, {event.action}, {event.time}, {event.place}"


def measure():
    # event_extractor = EventExtractor()
    with open("event_extraction_dataset.txt", "r") as f:
        lines = f.readlines()
        index = lines.index("__stop__\n")
        lines = lines[0:index]
        print(lines)

        sentences = []
        expected_events = []

        for line in lines:
            line = line.strip()
            dot_index = line.index(".")

            sent = line[0:dot_index + 1]
            sentences.append(sent)

            event_str = line[dot_index + 3:len(line) - 1]
            actor, action, time, place = event_str.split(", ")
            event = Event(actor, action, time, place)

            # raw_events = events_str.split(';')
            #
            # sent_events = []
            #
            # for raw_event in raw_events:
            #     event_str = raw_event[1:len(raw_event) - 1]
            #     actor, action, time, place = event_str.split(", ")
            #     event = Event(actor, action, time, place)
            #     sent_events.append(event)

            expected_events.append(event)

        predicted_events = []

        for i, sent in enumerate(sentences):
            print(i)
            try:
                predicted_event_list = extract_events(sent)
                # sent_predicted_events = []
                if not predicted_event_list:
                    predicted_events.append(Event("", "", "", ""))
                    # for _ in expected_events[i]:
                    #     sent_predicted_events.append(Event("", "", "", ""))
                else:
                    predicted_events.append(predicted_event_list[0])
                    # sent_predicted_events.extend(predicted_event_list)
                    # while len(sent_predicted_events) < len(expected_events[i]):
                    #     sent_predicted_events.append(Event("", "", "", ""))
                    # while len(sent_predicted_events) > len(expected_events[i]):
                    #     expected_events[i].append(Event("", "", "", ""))
                    # predicted_events.append(sent_predicted_events)

            except IndexError:
                print("ERROR: " + sent)

        # flattened_expected_events = []
        # for event_list in expected_events:
        #     for event in event_list:
        #         flattened_expected_events.append(event)
        #
        # flattened_predicted_events = []
        # for event_list in predicted_events:
        #     for event in event_list:
        #         flattened_predicted_events.append(event)

        # with open("extracted_events.txt", "w") as fw:
        #     lines_to_write = []
        #     for event in predicted_events:
        #         actor_str = event.actor if event.actor is not None else ""
        #         action_str = event.action if event.action is not None else ""
        #         time_str = event.time if event.time is not None else ""
        #         place_str = event.place if event.place is not None else ""
        #         lines_to_write.append(f"{{{actor_str}, {action_str}, {time_str}, {place_str}}}\n")
        #     fw.writelines(lines_to_write)

        predicted_actors = list(map(lambda e: e.actor if e.actor is not None else "", predicted_events))
        predicted_actions = list(map(lambda e: e.action if e.action is not None else "", predicted_events))
        predicted_times = list(map(lambda e: e.time if e.time is not None else "", predicted_events))
        predicted_places = list(map(lambda e: e.place if e.place is not None else "", predicted_events))

        expected_actors = list(map(lambda e: e.actor, expected_events))
        expected_actions = list(map(lambda e: e.action, expected_events))
        expected_times = list(map(lambda e: e.time, expected_events))
        expected_places = list(map(lambda e: e.place, expected_events))

        actor_precision, actor_recall, actor_f1_score = score(predicted_actors, expected_actors, lang="en", verbose=True)
        action_precision, action_recall, action_f1_score = score(predicted_actions, expected_actions, lang="en", verbose=True)
        time_precision, time_recall, time_f1_score = score(predicted_times, expected_times, lang="en", verbose=True)
        place_precision, place_recall, place_f1_score = score(predicted_places, expected_places, lang="en", verbose=True)

        print("Actor:")
        print("Precision: " + str(round(actor_precision.mean().item(), 3)))
        print("Recall: " + str(round(actor_recall.mean().item(), 3)))
        print("F1-score: " + str(round(actor_f1_score.mean().item(), 3)))

        print("Action:")
        print("Precision: " + str(round(action_precision.mean().item(), 3)))
        print("Recall: " + str(round(action_recall.mean().item(), 3)))
        print("F1-score: " + str(round(action_f1_score.mean().item(), 3)))

        print("Time:")
        print("Precision: " + str(round(time_precision.mean().item(), 3)))
        print("Recall: " + str(round(time_recall.mean().item(), 3)))
        print("F1-score: " + str(round(time_f1_score.mean().item(), 3)))

        print("Place:")
        print("Precision: " + str(round(place_precision.mean().item(), 3)))
        print("Recall: " + str(round(place_recall.mean().item(), 3)))
        print("F1-score: " + str(round(place_f1_score.mean().item(), 3)))


measure()
