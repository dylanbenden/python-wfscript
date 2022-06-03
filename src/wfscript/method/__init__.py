from .nodes import container
from .nodes import data_source
from .nodes import executors
from .nodes import interface
from .nodes import labels
from .nodes import selection

node_for_tag = {
    node_klass.tag_name: node_klass
    for node_klass in [
        interface.IdentityBindingNode,
        interface.InputBindingNode,
        interface.OutputBindingNode,

        labels.NamespaceTag,
        labels.NameTag,
        labels.VersionTag,
        labels.StatusTag,

        container.BodyContainerNode,
        container.ChoicesContainerNode,
        container.StepsContainerNode,
        container.RepeatContainerNode,
        container.ChoiceNode,

        executors.ActionNode,
        executors.MethodNode,
        executors.TicketNode,
        executors.StepNode,
        executors.VerifyNode,

        data_source.StateNode,
        data_source.InputNode,
        data_source.OutputNode,
        data_source.ItemNode,
        data_source.CollectionNode,
        data_source.MaterialTag,
        data_source.MaterialsTag,

        selection.SelectionSourceTag,
        selection.SelectionValueTag,
    ]
}
