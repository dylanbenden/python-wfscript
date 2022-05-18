from ..constants.identity import IdentityDelimeter


class WorkflowMaterial(object):
    model_identity = None
    identity_field = None

    @property
    def identity(self):
        return f'{self.model_identity}{IdentityDelimeter.MATERIAL}{getattr(self, self.identity_field)}'