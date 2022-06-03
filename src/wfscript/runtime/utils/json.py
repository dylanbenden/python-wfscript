import decimal

from ...runtime.materials import WorkflowMaterial


def preserialize(data):
    if isinstance(data, dict):
        return {k: preserialize(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [preserialize(v) for v in data]
    elif isinstance(data, WorkflowMaterial):
        return data.identity
    else:
        if isinstance(data, decimal.Decimal):
            return float(data)
    return data


def unfloat(data):
    if isinstance(data, dict):
        return {k: unfloat(v) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return [unfloat(v) for v in data]
    else:
        if isinstance(data, float):
            return decimal.Decimal(str(data))
    return data
