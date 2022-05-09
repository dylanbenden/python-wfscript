from .base import YAMLConfiguredObject
from ..constants.loading import TagName


class StateTag(YAMLConfiguredObject):
    tag_name = TagName.State


class DataTag(YAMLConfiguredObject):
    tag_name = TagName.Data
