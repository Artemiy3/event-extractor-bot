import os

import nltk
from nltk import Tree
from nltk.parse.corenlp import CoreNLPServer
import logging as log
from model.event import Event

os.environ['CLASSPATH'] = '/Users/artkochergin/pycharmProjects/thesis/event_extractor/stanford-corenlp-4.5.7'
nltk.download('punkt')


def get_children_with_label(tree: Tree, label: str) -> list[Tree]:
    result = []
    for child in tree:
        if isinstance(child, Tree) and child.label() == label:
            result.append(child)
    return result


def parse_time(tree: Tree) -> str:
    if tree.label().__contains__('TMP'):
        return ' '.join(tree.leaves())

    if tree.label() == 'ADVP':
        rb_children = get_children_with_label(tree, 'RB')
        if rb_children and len(tree) > 1:
            return ' '.join(tree.leaves())

    for child in tree:
        if isinstance(child, Tree):
            time = parse_time(child)
            if time:
                return time

    return ''


def parse_location(tree: Tree) -> str:
    if tree.label() == 'PP':
        if len(tree) == 2:
            if tree[0].label() == 'IN' and tree[1].label() == 'NP':
                potential_location = tree[1]
                pp_children = get_children_with_label(potential_location, 'PP')
                if pp_children:
                    location = parse_location(pp_children[0])
                    if location:
                        return location
                else:
                    location_tokens = []
                    location_tokens.extend(tree[0].leaves())
                    location_tokens.extend(potential_location.leaves())
                    return ' '.join(location_tokens)

    for child in tree:
        if isinstance(child, Tree):
            location = parse_location(child)
            if location:
                return location

    return ''


def parse_action(tree: Tree) -> str:
    if tree.label() != 'VP':
        log.error(f'Expected VP label, got {tree.label()}')

    action_trees = get_children_with_label(tree, 'VP')
    commas = get_children_with_label(tree, ',')
    ccs = get_children_with_label(tree, 'CC')
    if len(action_trees) > 1 and (commas or ccs):
        return parse_multiple_actions(tree)

    children_count = len(tree)
    action_tokens = []

    for i in range(0, children_count):
        child = tree[i]
        if child.label().startswith('VB'):
            if i < children_count - 1:
                next_component = tree[i + 1]
                if next_component.label() == 'PRT':
                    action_tokens.extend(child.leaves())
                    action_tokens.extend(next_component.leaves())
                    return ' '.join(action_tokens)
                if next_component.label() == 'VP':
                    action_tokens.extend(child.leaves())
                    action_tokens.append(parse_action(next_component))
                    return ' '.join(action_tokens)

                s_trees = get_children_with_label(tree, 'S')
                if s_trees:
                    s_tree = s_trees[0]
                    if s_tree[0].label() == 'VP' and len(s_tree[0]) == 2 and s_tree[0][0].label() == 'TO' and s_tree[0][1].label() == 'VP':
                        infinitive = s_tree[0]
                        action_tokens.extend(child.leaves())
                        action_tokens.extend(infinitive[0].leaves())
                        action_tokens.append(parse_action(infinitive[1]))
                        return ' '.join(action_tokens)

            if not child.label() == 'VBP' and not child.label() == 'VBZ':
                action_tokens.append(child[0])
            i += 1
            if i < children_count and tree[i].label() == 'NP':
                np_children = get_children_with_label(tree[i], 'NP')
                pp_children = get_children_with_label(tree[i], 'PP')
                if pp_children:
                    if np_children:
                        action_tokens.extend(np_children[0].leaves())
                else:
                    action_tokens.extend(tree[i].leaves())

    return ' '.join(action_tokens)


def parse_multiple_actions(tree: Tree) -> str:
    met_first_vp = False
    result = []
    for i in range(0, len(tree)):
        child = tree[i]
        if child.label() == 'VP':
            met_first_vp = True
            action_str = parse_action(child)
            if not action_str:
                log.error(f"Got empty action while parsing multiple actions.\nTokens: {tree.leaves()}")
            result.append(action_str)
        elif child.label() == ',' or child.label() == 'CC':
            if met_first_vp:
                result.extend(child.leaves())
            else:
                log.error(f"Got comma or CC label without previous action.\nTokens: {tree.leaves()}")

    return ' '.join(result)


def parse_events(tree: Tree) -> list[Event]:
    events = []

    s_count = 0
    np_count = 0
    vp_count = 0
    for child in tree:
        if child.label() == 'NP':
            np_count += 1
        elif child.label() == 'VP':
            vp_count += 1
        elif child.label() == 'S':
            s_count += 1

    if s_count > 0:
        for child in tree:
            if child.label() == 'S':
                events.extend(parse_events(child))

    if np_count == 1 and vp_count >= 1:
        actor_tree = get_children_with_label(tree, 'NP')[0]
        action_tree = get_children_with_label(tree, 'VP')[0]

        if (isinstance(actor_tree[0], Tree) and
                (actor_tree[0].label() == 'RB' or actor_tree[0].label() == 'EX') and
                vp_count == 1):
            if (action_tree[0].label() == 'VBP' or action_tree[0] == 'VBZ') and action_tree[1].label() == 'NP':
                return parse_events(action_tree[1])
            return []

        actor_tokens = actor_tree.leaves()
        actor_str = ' '.join(actor_tokens)

        action_str = parse_action(action_tree)
        if action_str:
            time = parse_time(tree)
            location = parse_location(tree)
            events.append(Event(actor=actor_str, action=action_str, time=time, place=location))

    return events


# sentence1 = "I have had a good breakfast today, but I'm already hungry. John left a minute ago."
# sentence2 = "There're three cats running after a mouse in the street. This house is nice."
# sentence3 = "A bunny ran past me just now. The wind blew in the forest."
# sentence4 = "A big rabbit crossed the street in Moscow city center yesterday."
# sentence5 = "Yesterday Alexey has done a lot of things in the forest."
# sentence6 = "I've cooked a dinner at home. John has sold a car in New York last Monday."
# sentence7 = "Dad returned from a business trip three days ago. He came running right away."
#
# all_sentences = [sentence1, sentence2, sentence3, sentence4, sentence5, sentence6, sentence7]


def extract_events(text: str) -> list[Event]:
    sentences = nltk.sent_tokenize(text)

    result = []
    with CoreNLPServer() as server:
        parser1 = nltk.CoreNLPParser(url=server.url)

        for sentence in sentences:
            tree_it = list(parser1.raw_parse(sentence))
            for tree in tree_it:
                # tree.pretty_print()
                events = parse_events(tree[0])
                result.extend(events)
                # for event in events:
                #     print(event)

    return result
