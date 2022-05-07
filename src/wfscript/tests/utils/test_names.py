import os

from ..content_root import content_root_path, content_root_module, testing_namespace_root
from ...utils.names import path_to_identity, find_yaml_files

root_path = content_root_path
_relative_path = os.path.sep.join(['loading', 'versioned_method'])
contained_path = os.path.sep.join([root_path, _relative_path])


def test_path_to_identity():
    expected = 'wfscript.tests.content_root.loading.versioned_method'
    assert path_to_identity(contained_path, root_path, content_root_module) == expected


def test_find_yaml_files():
    expected = [
        f'{contained_path}{os.path.sep}{method_version}'
        for method_version in ['1_0.yaml', '1_1.yaml', '1_2.yaml']
    ]
    assert find_yaml_files(testing_namespace_root) == expected
