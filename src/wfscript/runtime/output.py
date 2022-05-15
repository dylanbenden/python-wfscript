from datetime import timezone, datetime

from ..constants.payload import PayloadKey


class MethodReturn(object):
    def __init__(self, result, context):
        self._result = result
        self._run_id = context.run_id
        resume_info = context.state.resume_info
        if resume_info.get(PayloadKey.METHOD) and resume_info.get(PayloadKey.STEP):
            self._resume = resume_info
        else:
            self._resume = dict()

    @property
    def result(self):
        return self._result

    @property
    def run_id(self):
        return self._run_id

    @property
    def resume(self):
        return self._resume

    def render(self):
        return {
            PayloadKey.RESULT: self.result,
            PayloadKey.RUN_ID: self.run_id,
            PayloadKey.TIMESTAMP: datetime.now(tz=timezone.utc).isoformat(),
            PayloadKey.RESUME: self.resume,
        }


class ActionReturn(MethodReturn):
    pass


class StepReturn(MethodReturn):
    pass