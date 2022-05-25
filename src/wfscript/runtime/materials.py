from ..constants.identity import IdentityDelimeter


class WorkflowMaterial(object):
    model_identity = 'please/set/model_identity'
    identity_field = 'pk'

    @property
    def identity(self):
        return f'{self.model_identity}{IdentityDelimeter.MATERIAL}{getattr(self, self.identity_field)}'
