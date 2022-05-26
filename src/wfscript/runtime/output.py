from datetime import timezone, datetime

from ..constants.payload import PayloadKey


class ExecutorReturn(object):
    def __init__(self, result, context):
        self._result = result
        resume_info = context.state.resume_info
        if resume_info.get(PayloadKey.METHOD) and resume_info.get(PayloadKey.STEP):
            self._resume = resume_info
        else:
            self._resume = dict()

    @property
    def result(self):
        return self._result

    @property
    def resume(self):
        return self._resume

    def render(self):
        return {
            PayloadKey.RESULT: self.result,
            PayloadKey.RESUME: self.resume,
            PayloadKey.TIMESTAMP: datetime.now(tz=timezone.utc).isoformat(),
        }


class MethodReturn(ExecutorReturn):
    pass


class ActionReturn(ExecutorReturn):
    pass


class StepReturn(ExecutorReturn):
    pass