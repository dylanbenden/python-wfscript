class ConstantNamespace(object):
    @classmethod
    def as_dict(cls):
        return {
            k: v
            for (k, v) in cls.__dict__.items()
            if not k.startswith('_')
        }

    @classmethod
    def keys(cls):
        # sorted, for deterministic goodness
        return sorted(cls.as_dict().keys())

    @classmethod
    def values(cls):
        return sorted(cls.as_dict().values())

    @classmethod
    def items(cls):
        return sorted(cls.as_dict().items())

    @classmethod
    def choices(cls):
        # provides ordering that Django CharField(choices=...) expects
        return sorted([(v, k) for k, v in cls.items()])

    @classmethod
    def document(cls):
        return {cls.__name__: cls.as_dict()}
