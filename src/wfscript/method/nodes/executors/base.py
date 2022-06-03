from ..base import WorkflowNode, ExecutionPhase
from ....constants.method import TagName


class ExecutorNode(WorkflowNode, ExecutionPhase):
    tag_name = None

    @property
    def identity(self):
        return self.node_for_tag[TagName.IDENTITY].constructed

    @property
    def input(self):
        return self.node_for_tag.get(TagName.INPUT, dict())

    @property
    def output(self):
        return self.node_for_tag.get(TagName.OUTPUT)
