from ..constants import TagName
from ....testing_tools.context import get_empty_context
from ....testing_tools.mocks import ValueAssignableObject
from .....constants import ConstantNamespace
from .....method.document_loader import load_yaml


class TestParam(ConstantNamespace):
    obj_key = 'my_key'
    obj_value = 'some value'
    sub_key = 'data_subkey'

def test_item_tag():
    tag_name = TagName.Item
    context = get_empty_context()

    # with no argument, !Item is a reference to the !Item object
    context.runtime[TagName.Item] = ValueAssignableObject(**{TestParam.obj_key: TestParam.obj_value})
    snippet = f'''
      - {tag_name}
    '''
    node = load_yaml(snippet)[0]
    assert node.tag == tag_name
    assert node.value == ''
    item_obj = node.render(context)
    assert getattr(item_obj, TestParam.obj_key) == TestParam.obj_value

    # argument to !Item is assumed to be a "dotted path" notation for getting attr/index/etc of item
    context.runtime[TagName.Item] = ValueAssignableObject(**{TestParam.sub_key:
                                                             {TestParam.obj_key: TestParam.obj_value}})
    snippet = f'''
      - {tag_name} {TestParam.sub_key}.{TestParam.obj_key}
    '''
    node = load_yaml(snippet)[0]
    assert node.tag == tag_name
    assert node.value == f'{TestParam.sub_key}.{TestParam.obj_key}'
    assert node.render(context) == TestParam.obj_value
