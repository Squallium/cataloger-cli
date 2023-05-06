class BaseService(type):
    """ Singleton metaclass for services"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(BaseService, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
