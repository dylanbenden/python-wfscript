from .base import ExecutorTag
from ....constants.method import TagName


class TicketTag(ExecutorTag):
    tag_name = TagName.Ticket
    construct_value_as_mapping = True