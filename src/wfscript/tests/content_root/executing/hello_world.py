from ....runtime.decorators import action_identity


@action_identity('content_root/executing::hello_world==production')
def hello_world_2_0(name=None):
    if name is None:
        name = 'you beautiful person'
    return f'Hello there, {name}!'
