import os

from ..content_root.loading import content_root_path, content_root_module, loading_namespace_root
from ...utils.names import path_to_identity, find_yaml_files

root_path = content_root_path
contained_path = os.path.sep.join([root_path, 'versioned_method'])


def test_path_to_identity():
    expected = 'wfscript.tests.content_root.loading.versioned_method'
    assert path_to_identity(contained_path, root_path, content_root_module) == expected


def test_find_yaml_files():
    expected = [
        f'{contained_path}{os.path.sep}{method_version}'
        for method_version in ['1_0.yaml', '1_1.yaml', '1_2.yaml']
    ]
    assert find_yaml_files(loading_namespace_root) == expected
