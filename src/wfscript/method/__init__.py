from .tags import container
from .tags import data_source
from .tags import executors
from .tags import interface
from .tags import labels
from .tags import selection

constructor_for_tag = {
    tag.tag_name: tag
    for tag in [
        interface.IdentitySectionTag,
        interface.InputSectionTag,
        interface.OutputSectionTag,

        labels.NamespaceTag,
        labels.NameTag,
        labels.VersionTag,
        labels.StatusTag,

        container.BodySectionTag,
        container.ChoicesSectionTag,
        container.StepsSectionTag,
        container.RepeatSectionTag,
        container.ChoiceTag,

        executors.ActionTag,
        executors.MethodTag,
        executors.TicketTag,
        executors.StepTag,

        data_source.StateTag,
        data_source.InputTag,
        data_source.OutputTag,
        data_source.ItemTag,
        data_source.CollectionTag,
        data_source.MaterialTag,
        data_source.MaterialsTag,
        data_source.AssetTag,
        data_source.AssetsTag,

        selection.SelectionSourceTag,
        selection.SelectionValueTag,
    ]
}
