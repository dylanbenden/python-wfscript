from .tags.choice import ChoiceTag
from .tags.container import StepTag, BodySectionTag, ForEachTag
from .tags.data_source import InputTag, StateTag, OutputTag
from .tags.executors import ActionTag, MethodTag, TicketTag
from .tags.identity import IdentitySectionTag
from .tags.input import InputSectionTag
from .tags.labels import NamespaceTag, NameTag, VersionTag, StatusTag
from .tags.output import OutputSectionTag

constructor_for_tag = {
    tag.tag_name: tag
    for tag in [
        IdentitySectionTag, InputSectionTag, BodySectionTag, OutputSectionTag,
        NamespaceTag, NameTag, VersionTag, StatusTag,
        ActionTag, MethodTag, StepTag, TicketTag,
        InputTag, OutputTag, StateTag,
        ChoiceTag, ForEachTag,
    ]
}
