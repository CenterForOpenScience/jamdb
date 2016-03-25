class Plugin:

    @classmethod
    def serialize(cls, request, inst, *parents):
        return {
            'links': {
                'self': cls.self_link(request, inst, *parents),
                'related': cls.related_link(request, inst, *parents),
            }
        }

    @classmethod
    def view(inst, *parents):
        raise NotImplementedError()

    @classmethod
    def serializer(cls):
        raise NotImplementedError()

    @classmethod
    def self_link(request, inst, *parents):
        raise NotImplementedError()

    @classmethod
    def related_link(request, inst, *parents):
        raise NotImplementedError()

    @classmethod
    def prerequisite_check(request, inst, *parents):
        raise NotImplementedError()
