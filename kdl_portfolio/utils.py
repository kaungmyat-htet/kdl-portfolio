import json
from unittest.mock import MagicMock

from opaque_keys.edx.locator import CourseLocator

SENSITIVE_KEYS = [
    "password",
    "token",
    "client_id",
    "client_secret",
    "Authorization",
    "secret",
]

class PluginJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        if isinstance(obj, MagicMock):
            return ""
        try:
            return json.JSONEncoder.default(self, obj)
        except Exception:  # noqa: B902
            # obj probably is not json serializable.
            return ""

def masked_dict(obj) -> dict:
    """
    To mask sensitive key / value in log entries.
    masks the value of specified key.
    obj: a dict or a string representation of a dict, or None
    """

    def redact(key: str, obj):
        if key in obj:
            obj[key] = "*** -- REDACTED -- ***"
        return obj

    obj = obj or {}
    obj = dict(obj)
    for key in SENSITIVE_KEYS:
        obj = redact(key, obj)
    return obj

def serialize_course_key(inst, field, value):  # pylint: disable=unused-argument
    """
    Serialize instances of CourseLocator.
    When value is anything else returns it without modification.
    """
    if isinstance(value, CourseLocator):
        return str(value)
    return value