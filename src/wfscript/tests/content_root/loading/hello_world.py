from ....names.decorators import action_identity


@action_identity('content_root/loading::hello_world==1.0')
def hello_world_1_0():
    return f'Hello there, you beautiful person!'


# changing the signature of the function is considered a major version bump
@action_identity('content_root/loading::hello_world==2.0')
@action_identity('content_root/loading::hello_world==production')
@action_identity('content_root/loading::hello_world')
def hello_world_2_0(name=None):
    if name is None:
        name = 'you beautiful person'
    return f'Hello there, {name}!'


@action_identity('content_root/loading::hello_world==2.1')
@action_identity('content_root/loading::hello_world==testing')
def hello_world_2_1(name=None):
    return f'{hello_world_2_0(name)} Shall we play a game?'
