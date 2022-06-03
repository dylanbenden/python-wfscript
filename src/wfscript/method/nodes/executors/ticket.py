from .base import ExecutorNode
from ....constants.method import TagName
from ....runtime.utils.render import execute_render


class TicketNode(ExecutorNode):
    tag_name = TagName.Ticket

    def execute_render_from_list(self, context):
        return context.namespace_root.domain.add_ticket(
            identity=self.node_for_tag[TagName.IDENTITY].constructed,
            input_data=execute_render(self.node_for_tag[TagName.INPUT].value, context)
        )
