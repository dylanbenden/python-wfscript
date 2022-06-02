from .base import DataSourceNode
from ....constants.identity import IdentityDelimeter
from ....constants.method import TagName
from ....runtime.materials import WorkflowMaterial


class ObjectManagingNode(DataSourceNode):
    tag_name = None
    is_read_only = None
    is_plural = None

    def data_source(self, context):
        name_key = self.value
        if '.' in name_key:
            name_key = name_key.split('.')[0]
        if name_key in context.state.value:
            return context.state
        elif name_key in context.output.value:
            return context.output
        elif name_key in context.input.value:
            return context.input
        raise RuntimeError(f'Unable to find key {name_key} in state, output, or input')

    def execute_render_from_scalar(self, context):
        # result might be a single identity/object or a collection of identities/objects
        result = self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))
        if isinstance(result, list):
            if all([isinstance(i, str) for i in result]):
                if self.is_plural:
                    return context.namespace_root.domain.load_materials(result)
                else:
                    raise RuntimeError(f'{self.tag_name} expects single id, got array of strings: {result}')
            else:
                if not self.is_plural:
                    raise RuntimeError(f'{self.tag_name} expects single object, got array: {result}')
        else:
            if self.is_plural:
                raise RuntimeError(f'{self.tag_name} expects an array of ids or objects, got: {result}')
            else:
                if isinstance(result, str):
                    return context.namespace_root.domain.load_material(result)
        if isinstance(result, WorkflowMaterial):
            return result.identity
        return result

    # def output_render_from_scalar(self, context):
    #     if self.is_plural:
    #         rendered_items = output_render(self.value, context)
    #     else:
    #         rendered_items = [output_render(self.value, context)]
    #     if all(hasattr(item, 'identity') for item in rendered_items):
    #         identified_items = [getattr(item, 'identity') for item in rendered_items]
    #     else:
    #         identified_items = rendered_items
    #     if self.is_plural:
    #         return identified_items
    #     return identified_items[0]


    # def get_material_or_materials(self, name_key, context):
        # if name_key in context.state.value:
        #     obj_or_id = context.state[name_key]
        # elif name_key in context.output.value:
        #     obj_or_id = context.output[name_key]
        # elif name_key in context.input.value:
        #     obj_or_id = context.input[name_key]
        # else:
        #     raise RuntimeError('asdf')
    # def sanity_check(self, result):
    #     if isinstance(result, str):
    #         if self.is_plural:
    #             raise('expecting array of ids, got single string')
    #         else:
    #             return context.namespace_root.domain.load_material(obj_or_id)
    #     elif isinstance(obj_or_id, list):
    #         if all([isinstance(i, str) for i in obj_or_id]):
    #             if self.is_plural:
    #                 return context.namespace_root.domain.load_materials(obj_or_id)
    #             else:
    #                 raise RuntimeError('expecting single id, got array of strings')
    #         else:
    #             if self.is_plural:
    #                 return obj_or_id
    #             else:
    #                 raise RuntimeError('expecting single object, got array')
    #     return obj_or_id
    #
    # def render_payload(self, context):
    #     name_key = self.value
    #     attribute = None
    #     if '.' in name_key:
    #         name_key, attribute = name_key.split('.')
    #     mat_or_mats = self.get_material_or_materials(name_key, context)
    #     if attribute:
    #         if self.is_plural:
    #             return [getattr(mat, attribute, None) for mat in mat_or_mats]
    #         else:
    #             return getattr(mat_or_mats, attribute, None)
    #     return mat_or_mats



class MaterialTag(ObjectManagingNode):
    tag_name = TagName.Material

    def execute_render_from_scalar(self, context):
        result = self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))
        if isinstance(result, str) and IdentityDelimeter.NAMESPACE in result:
            return context.namespace_root.domain.load_material(result)
        return result

    def output_render_from_scalar(self, context):
        result = self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))
        if isinstance(result, WorkflowMaterial):
            return result.identity
        return result


class MaterialsTag(ObjectManagingNode):
    tag_name = TagName.Materials

    def execute_render_from_scalar(self, context):
        result = self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))
        if isinstance(result, list):
            if all(isinstance(item, str) and IdentityDelimeter.NAMESPACE in item for item in result):
                return context.namespace_root.domain.load_materials(result)
        return result


    def output_render_from_scalar(self, context):
        result = self.traverse_name_key(name_key=self.value, data_source=self.data_source(context))
        if isinstance(result, list):
            return [
                item.identity if isinstance(item, WorkflowMaterial) else item
                for item in result
            ]
        return result

