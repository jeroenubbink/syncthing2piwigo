from typing import cast

from marshmallow import Schema, fields, EXCLUDE


class EventBaseSchema(Schema):
    ...


# FIXME: unsure how this works, should probably do something with timezone
#        accept we have a dict for the nested schema right now.

class EventDateTimeField(fields.DateTime):

    def _to_iso_format(self, syncthing_event_time: str) -> str:
        # look at the crap we have to deal with...
        # "2014-07-13T21:22:03.414609034+02:00"
        # first transform nano_seconds into micro_seconds
        _nano_seconds = syncthing_event_time.split(".")[1][:-6]
        _micro_seconds = _nano_seconds[:6]
        # correct tz
        _syncthing_tz = syncthing_event_time[-6:]
        _iso_format_tz = _syncthing_tz.replace(":", "")

        _fixed_nano_seconds = syncthing_event_time.replace(_nano_seconds, _micro_seconds)
        iso_format_string = _fixed_nano_seconds.replace(_syncthing_tz, _iso_format_tz)

        return iso_format_string

    def _to_syncthing_format(self, iso_format_time: str) -> str:
        # let's add the crap and forget about the lost nano seconds
        _micro_seconds = iso_format_time.split(".")[1][:-5]
        _nano_seconds = f"{_micro_seconds}000"

        _iso_format_tz = iso_format_time[-5:]
        _syncthing_tz = f"{_iso_format_tz[:-2]}:{_iso_format_tz[-2:]}"

        _fixed_micro_seconds = iso_format_time.replace(_micro_seconds, _nano_seconds)
        syncthing_format_string = _fixed_micro_seconds.replace(_iso_format_tz, _syncthing_tz)

        return syncthing_format_string

    def _deserialize(self, value, attr, data, **kwargs):
        print(f"deserialize value: {value}")
        event_time: str = cast(str, value)
        value_iso_format = self._to_iso_format(syncthing_event_time=event_time)
        super()._deserialize(value_iso_format, attr, data, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        print(f"serialize value: {value}")
        iso_time: str = super()._serialize(value, attr, obj, **kwargs)
        value_syncthing_format = self._to_syncthing_format(iso_format_time=iso_time)
        return value_syncthing_format


class EventDataSchema(EventBaseSchema):
    item = fields.Str()
    folder = fields.Str()
    error = fields.Str(required=False, allow_none=True)
    type = fields.Str()
    action = fields.Str()

    class Meta(EventBaseSchema.Meta):
        unknown = EXCLUDE


class EventSchema(EventBaseSchema):
    id = fields.Int()
    globalID = fields.Int()
    type = fields.Str()
    time = EventDateTimeField()
    data = fields.Nested(EventDataSchema(partial=True))
