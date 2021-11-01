from marshmallow import Schema, fields, ValidationError, EXCLUDE

from syncthing2piwigo.syncthing.registry import EventDataRegistry, NotRegisteredException



class EventDataField(fields.Field):

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            schema_cls = EventDataRegistry.class_by_name(data.get("type"))
            event_data = schema_cls()
            return event_data.load(value)
        except NotRegisteredException as error:
            raise ValidationError("Could not find schema class in registry.") from error


class EventDataSchema(Schema):
    item: fields.Str()
    folder: fields.Str()
    error: fields.Str()
    type: fields.Str()
    action: fields.Str()


class EventSchema(Schema):
    id: fields.Int()
    globalID: fields.Int()
    type: fields.Str()
    time: fields.DateTime()
    data: fields.Nested(EventDataSchema(partial=True, unknown=EXCLUDE))
