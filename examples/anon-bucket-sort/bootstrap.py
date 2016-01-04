import os
import json

# from jam import Namespace
from jam import NamespaceManager
from jam import exceptions
from jam.auth import Permissions


creator = 'anon--6daf159c9a2d4583aef1a6e366288760'
cards_loc = os.path.join(os.path.split(__file__)[0], 'cards.json')


def main():
    try:
        ns = NamespaceManager().get_namespace('card-app')
    except exceptions.NotFound:
        ns = NamespaceManager().create_namespace('card-app', creator)

    try:
        ns.get_collection('placements')
    except exceptions.NotFound:
        ns.create_collection('placements', creator, permissions={
            'anon-*': Permissions.CREATE
        })

    try:
        collection = ns.get_collection('cards')
    except exceptions.NotFound:
        collection = ns.create_collection('cards', creator, permissions={'*': Permissions.READ})

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
