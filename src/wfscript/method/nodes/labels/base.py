from ..base import WorkflowNode, DualPhase, ExecutionPhase


class LabelNode(WorkflowNode, ExecutionPhase):
    def execute_render_from_scalar(self, *_):
        return self.value
