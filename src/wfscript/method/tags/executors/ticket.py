from .base import ExecutorTag
from ....constants.method import TagName
from ....runtime.utils.identity import construct_identity


class TicketTag(ExecutorTag):
    tag_name = TagName.Ticket
    use_child_tags_as_labels = True

    def render_from_dict(self, context, **_):
        return context.namespace_root.domain.add_ticket(
            identity=construct_identity(self.value[TagName.IDENTITY]),
            input_data=self.value[TagName.INPUT]
        )
