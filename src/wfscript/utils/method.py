from .json import unfloat
from ..constants.loading import TagName
from ..loading.base import YAMLConfiguredObject
from ..runtime.output import StepReturn


def handle_method_or_step_body(body, context):
    for item in body:
        result = handle_item(item, context)
        if isinstance(result, StepReturn):
            return result


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


handler_for_tag = {
    TagName.Action: handle_action,
    # TagName.Method: handle_method,
    # TagName.Step: handle_step,
    # TagName.State: handle_state
}
render_for_tag = {
    # TagName.Material: render_material,
    # TagName.Asset: render_asset,
    # TagName.Materials: render_materials,
    # TagName.Assets: render_assets
}
