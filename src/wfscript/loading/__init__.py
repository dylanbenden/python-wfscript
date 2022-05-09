from .data import DataTag, StateTag
from .executors import ActionTag
from ..constants.loading import TagName

constructor_for_tag = {
    TagName.Action: ActionTag,
    TagName.Data: DataTag,
    TagName.State: StateTag
}