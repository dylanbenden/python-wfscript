from .base import ExecutorTag
from ....constants.method import TagName


class StepTag(ExecutorTag):
    tag_name = TagName.Step
    permitted_contents = [TagName.Method, TagName.Step, TagName.Action, TagName.State]
