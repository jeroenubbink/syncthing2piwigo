from typing import cast, Any, List


class NotRegisteredException(Exception):
    def __str__(self):
        return "Class was not found in registry"


class EventDataRegistry(type):
    registered = {}
    def __new__(cls: Any, name: Any, bases: Any, attrs: Any):
        _name: str = cast(name, str)
        type_name = _name.replace("EventData")
        newtype = super(EventDataRegistry, cls).__new__(cls, name, bases, attrs)
        cls.registered[type_name] = newtype

    @classmethod
    def class_by_name(cls, name: str):
        # get a class from the registerd classes
        try:
            return cls.registered[name]
        except KeyError:
            print(cls.__dict__)
            print(name)
            raise NotRegisteredException()
