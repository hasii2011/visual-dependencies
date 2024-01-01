
# TODO:  Use a copy of this until code-ally-basic is updated

def singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


class SingletonV2:
    """
    Base class for singleton classes.

    Any class derived from this one is a singleton. You can call its
    constructor multiple times, you'll get only one instance.

    """
    def __new__(cls, *args, **kwargs):
        """
        New operator of a singleton class.
        Will return the only instance, or create it if needed.

        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonV2, cls).__new__(cls)
        # noinspection PyUnresolvedReferences
        return cls.instance
