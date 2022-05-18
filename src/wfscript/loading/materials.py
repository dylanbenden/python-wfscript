from ..constants.loading import TagName
from ..loading.base import YAMLConfiguredObject


class ObjectManagingTag(YAMLConfiguredObject):
    tag_name = None
    is_read_only = None
    is_plural = None

    def get_material_or_materials(self, name_key, context):
        if name_key in context.state.value:
            obj_or_id = context.state[name_key]
        elif name_key in context.output.value:
            obj_or_id = context.output[name_key]
        elif name_key in context.input.value:
            obj_or_id = context.input[name_key]
        else:
            raise RuntimeError('asdf')
        if isinstance(obj_or_id, str):
            if self.is_plural:
                raise('expecting array of ids, got single string')
            else:
                return context.namespace_root.domain.load_material(obj_or_id)
        elif isinstance(obj_or_id, list):
            if all([isinstance(i, str) for i in obj_or_id]):
                if self.is_plural:
                    return context.namespace_root.domain.load_materials(obj_or_id)
                else:
                    raise RuntimeError('expecting single id, got array of strings')
            else:
                if self.is_plural:
                    return obj_or_id
                else:
                    raise RuntimeError('expecting single object, got array')
        return obj_or_id

    def render_payload(self, context):
        name_key = self.value
        attribute = None
        if '.' in name_key:
            name_key, attribute = name_key.split('.')
        mat_or_mats = self.get_material_or_materials(name_key, context)
        if attribute:
            if self.is_plural:
                return [getattr(mat, attribute, None) for mat in mat_or_mats]
            else:
                return getattr(mat_or_mats, attribute, None)
        return mat_or_mats



class MaterialTag(ObjectManagingTag):
    tag_name = TagName.Material
    is_read_only = False
    is_plural = False


class MaterialsTag(ObjectManagingTag):
    tag_name = TagName.Materials
    is_read_only = False
    is_plural = True


class AssetTag(ObjectManagingTag):
    tag_name = TagName.Asset
    is_read_only = True
    is_plural = False


class AssetsTag(ObjectManagingTag):
    tag_name = TagName.Assets
    is_read_only = True
    is_plural = True
