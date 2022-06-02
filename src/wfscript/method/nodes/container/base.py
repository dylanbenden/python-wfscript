from ..base import WorkflowNode, ExecutionPhase


class ContainerNode(WorkflowNode, ExecutionPhase):
    permitted_contents = None
