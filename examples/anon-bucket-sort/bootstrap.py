import os
import json

from iodm import Namespace
from iodm import exceptions
from iodm.auth import Permissions


cards_loc = os.path.join(os.path.split(__file__)[0], 'cards.json')


def main():
    ns = Namespace('card-app')

    try:
        ns.create_collection('cards', {
            'logs': ['mongo', 'cardapp', 'card-logs'],
            'state': ['mongo', 'cardapp', 'card-state'],
            'storage': ['mongo', 'cardapp', 'card-storage'],
        }, '', permissions={'*': Permissions.READ})
    except Exception:
        pass

    try:
        ns.create_collection('placements', {
            'logs': ['mongo', 'cardapp', 'placement-logs'],
            'state': ['mongo', 'cardapp', 'placement-state'],
            'storage': ['mongo', 'cardapp', 'placement-storage'],
        }, '', permissions={'anon-*': Permissions.CREATE})
    except Exception:
        pass

    collection = ns.get_collection('cards')

    with open(cards_loc) as cards:
        for card in json.load(cards)['cards']:
            try:
                entry = collection.read(card['id'])
                assert entry.data['content'] == card['content']
            except AssertionError:
                collection.update(card['id'], {'content': card['content']}, '')
            except exceptions.NotFound:
                collection.create(card['id'], {'content': card['content']}, '')


if __name__ == '__main__':
    main()
