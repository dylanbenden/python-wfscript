from . import ConstantNamespace


class PayloadKey(ConstantNamespace):
    REQUEST = 'request'
    RESPONSE = 'response'

    INPUT = 'input'
    RESULT = 'result'

    METHOD = 'method'
    STEP = 'step'
    STATE = 'state'
    RUN_ID = 'run_id'

    RESUME = 'resume'

    TIMESTAMP = 'timestamp'
    COMPLETED = 'completed'
    DUPLICATE = 'duplicate'
