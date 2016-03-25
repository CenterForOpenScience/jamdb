from jam.server.api.v1.base.view import View
from jam.server.api.v1.base.plugin import Plugin
from jam.server.api.v1.base.constants import ID_RE
from jam.server.api.v1.base.constants import ENDING
from jam.server.api.v1.base.constants import NAMESPACER
from jam.server.api.v1.base.serializer import Serializer
from jam.server.api.v1.base.handlers import PluginHandler
from jam.server.api.v1.base.handlers import ResourceHandler
from jam.server.api.v1.base.relationship import Relationship
from jam.server.api.v1.base.handlers import RelationshipHandler


def ResourceEndpoint(view, serializer):
    hierachical, ids, kwargs = [], [], {'view': view, 'serializer': serializer}
    selector = r'(?P<{}_id>{})'.format(view.name, ID_RE)

    for v in view.lineage()[:-1]:
        # Just of list of resource id regexes that will be concatenated with NAMESPACER
        ids.append(r'(?P<{}_id>{})'.format(v.name, ID_RE))
        # Builds /resources/regexeforresourceid
        hierachical.extend([v.plural, r'(?P<{}_id>{})'.format(v.name, ID_RE)])

    hierachical.append(view.plural)

    hierachical = '/v1/' + '/'.join(hierachical) + ENDING.format(selector)
    id_ = '/v1/id/' + view.plural + ENDING.format(NAMESPACER.join(ids + [selector]))

    endpoints = [
        (hierachical, ResourceHandler, kwargs),
        (id_, ResourceHandler, kwargs),
    ]

    # If the serializer has relationships add a relationship handler
    if serializer.relations:
        relationships = '/v1/id/{}/{}/(?P<relationship>{})/?'.format(
            view.plural,
            NAMESPACER.join(ids + [selector]),
            '|'.join(serializer.relations.keys())
        )
        endpoints.append((relationships, RelationshipHandler, kwargs))

    if serializer.plugins:
        relationships = '/v1/id/{}/{}/(?P<plugin>{})/?'.format(
            view.plural,
            NAMESPACER.join(ids + [selector]),
            '|'.join(serializer.plugins.keys())
        )
        endpoints.append((relationships, PluginHandler, kwargs))

    return endpoints


__all__ = (
    'View',
    'Plugin',
    'Serializer',
    'Relationship',
    'ResourceEndpoint',
)
