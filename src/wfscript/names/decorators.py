from .store import NameStore


def action_identity(identity):
    def registration_wrapper(fx):
        NameStore.register_action(identity, fx)
        return fx
    return registration_wrapper
