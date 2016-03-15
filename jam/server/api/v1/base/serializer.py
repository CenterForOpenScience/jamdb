import datetime


class Serializer:
    view = None
    relations = {}

    @classmethod
    def serialize(cls, request, inst, *parents):
        return {
            # TODO MAKE CONSTANT
            'id': '.'.join([p.ref or p.ref for p in parents] + [inst.ref]),
            'type': cls.type,
            'meta': cls.meta(inst),
            # 'links': cls.links(request, inst, *parents),
            'attributes': cls.attributes(inst),
            'relationships': cls.relationships(request, inst, *parents)
        }

    @classmethod
    def relationships(cls, request, inst, *parents):
        return {
            name: relation.serialize(request, inst, *parents)
            for name, relation in cls.relations.items()
            if relation.included
        }

    @classmethod
    def meta(cls, inst):
        return {
            'created-by': inst.created_by,
            'modified-by': inst.modified_by,
            'created-on': datetime.datetime.fromtimestamp(inst.created_on).isoformat(),
            'modified-on': datetime.datetime.fromtimestamp(inst.modified_on).isoformat()
        }
