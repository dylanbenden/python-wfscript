from .json import unfloat
from ..constants.loading import TagName, MethodKeyword
from ..loading.base import YAMLConfiguredObject
from ..runtime.output import StepReturn


def handle_method_or_step_body(body, context):
    for item in body:
        result = handle_item(item, context)
        if isinstance(result, StepReturn):
            return result


def items_after_step(body, step_name):
    for idx, item in enumerate(body):
        if item.tag == TagName.Step and item.value['name'] == step_name:
            return body[idx + 1:]
    raise RuntimeError(f'Step {step_name} not found')


def handle_item(item, context):
    return handler_for_tag[item.tag](item, context)


def handle_action(action, context):
    return run_executor(
        executor=context.namespace_root.get_action(action.identity),
        action_or_method_tag=action,
        context=context
    )


def render_tag_dict(data, context):
    output = dict()
    for key, value in data.items():
        if isinstance(value, YAMLConfiguredObject):
            output[key] = value.render_payload(context)
        else:
            output[key] = value
    return output

def run_executor(executor, action_or_method_tag, context):
    exec_kwargs = action_or_method_tag.render_payload(context)
    if action_or_method_tag.tag == TagName.Action:
        result = executor(**exec_kwargs)
    else:
        result = executor.run(context)
    if result is not None:
        if action_or_method_tag.output_target:
            target_key = action_or_method_tag.output_target.value
            action_or_method_tag.output_target.update({target_key: unfloat(result)}, context)
        return result


def handle_method(method, context):
    return run_executor(
        executor=context.namespace_root.get_method(method.identity),
        action_or_method_tag=method,
        context=context
    )


def handle_step(step, context):
    if 'name' not in step.value:
        raise RuntimeError(f'Step requires a name; Provided: {step.value}')
    results = handle_method_or_step_body(step.value[MethodKeyword.BODY], context)
    if isinstance(results, StepReturn):
        return results
    if MethodKeyword.RETURN in step.value:
        context.state.set_resume_state(method=context.method, step=step.value['name'])
        return StepReturn(
            result=render_tag_dict(step.value[MethodKeyword.RETURN], context),
            context=context
        )


def handle_state(state_tag, context):
    data_updates = dict()
    for key, value in state_tag.value.items():
        if isinstance(value, YAMLConfiguredObject):
            data_updates[key] = value.render_payload(context)
        else:
            data_updates[key] = value
    context.state.update(data_updates)


handler_for_tag = {
    TagName.Action: handle_action,
    TagName.Method: handle_method,
    TagName.Step: handle_step,
    TagName.State: handle_state
}
render_for_tag = {
    # TagName.Material: render_material,
    # TagName.Asset: render_asset,
    # TagName.Materials: render_materials,
    # TagName.Assets: render_assets
}
