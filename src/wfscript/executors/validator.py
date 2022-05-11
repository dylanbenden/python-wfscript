from .base import DocumentExecutor
from ..utils.validation import validate_input


class ValidatorExecutor(DocumentExecutor):
    def validate(self, data_node):
        return validate_input(self.document, data_node, self.namespace_root)
