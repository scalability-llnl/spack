# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test YAML serialization for specs.

YAML format preserves DAG information in the spec.

"""
import ast
import inspect
import os
import sys

import pytest

import spack.architecture
import spack.hash_types as ht
import spack.spec
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.version

from spack import repo
from spack.spec import Spec, save_dependency_spec_yamls
from spack.util.spack_yaml import syaml_dict
from spack.util.mock_package import MockPackageMultiRepo


if sys.version_info >= (3, 3):
    from collections.abc import Iterable, Mapping  # novm
else:
    from collections import Iterable, Mapping


def check_yaml_round_trip(spec):
    yaml_text = spec.to_yaml()
    spec_from_yaml = Spec.from_yaml(yaml_text)
    assert spec.eq_dag(spec_from_yaml)


def test_simple_spec():
    spec = Spec('mpileaks')
    check_yaml_round_trip(spec)


def test_normal_spec(mock_packages):
    spec = Spec('mpileaks+debug~opt')
    spec.normalize()
    check_yaml_round_trip(spec)


def test_external_spec(config, mock_packages):
    spec = Spec('externaltool')
    spec.concretize()
    check_yaml_round_trip(spec)

    spec = Spec('externaltest')
    spec.concretize()
    check_yaml_round_trip(spec)


def test_ambiguous_version_spec(mock_packages):
    spec = Spec('mpileaks@1.0:5.0,6.1,7.3+debug~opt')
    spec.normalize()
    check_yaml_round_trip(spec)


def test_concrete_spec(config, mock_packages):
    spec = Spec('mpileaks+debug~opt')
    spec.concretize()
    check_yaml_round_trip(spec)


def test_yaml_multivalue(config, mock_packages):
    spec = Spec('multivalue-variant foo="bar,baz"')
    spec.concretize()
    check_yaml_round_trip(spec)


def test_yaml_subdag(config, mock_packages):
    spec = Spec('mpileaks^mpich+debug')
    spec.concretize()
    yaml_spec = Spec.from_yaml(spec.to_yaml())

    for dep in ('callpath', 'mpich', 'dyninst', 'libdwarf', 'libelf'):
        assert spec[dep].eq_dag(yaml_spec[dep])


def test_using_ordered_dict(mock_packages):
    """ Checks that dicts are ordered

    Necessary to make sure that dag_hash is stable across python
    versions and processes.
    """
    def descend_and_check(iterable, level=0):
        if isinstance(iterable, Mapping):
            assert isinstance(iterable, syaml_dict)
            return descend_and_check(iterable.values(), level=level + 1)
        max_level = level
        for value in iterable:
            if isinstance(value, Iterable) and not isinstance(value, str):
                nlevel = descend_and_check(value, level=level + 1)
                if nlevel > max_level:
                    max_level = nlevel
        return max_level

    specs = ['mpileaks ^zmpi', 'dttop', 'dtuse']
    for spec in specs:
        dag = Spec(spec)
        dag.normalize()
        level = descend_and_check(dag.to_node_dict())

        # level just makes sure we are doing something here
        assert level >= 5


def test_to_record_dict(mock_packages, config):
    specs = ['mpileaks', 'zmpi', 'dttop']
    for name in specs:
        spec = Spec(name).concretized()
        record = spec.to_record_dict()
        assert record["name"] == name
        assert "hash" in record

        node = spec.to_node_dict()
        for key, value in node[name].items():
            assert key in record
            assert record[key] == value


@pytest.mark.parametrize("hash_type", [
    ht.dag_hash,
    ht.build_hash,
    ht.full_hash
])
def test_ordered_read_not_required_for_consistent_dag_hash(
        hash_type, config, mock_packages
):
    """Make sure ordered serialization isn't required to preserve hashes.

    For consistent hashes, we require that YAML and json documents
    have their keys serialized in a deterministic order. However, we
    don't want to require them to be serialized in order. This
    ensures that is not required.
    """
    specs = ['mpileaks ^zmpi', 'dttop', 'dtuse']
    for spec in specs:
        spec = Spec(spec)
        spec.concretize()

        #
        # Dict & corresponding YAML & JSON from the original spec.
        #
        spec_dict = spec.to_dict(hash=hash_type)
        spec_yaml = spec.to_yaml(hash=hash_type)
        spec_json = spec.to_json(hash=hash_type)

        #
        # Make a spec with reversed OrderedDicts for every
        # OrderedDict in the original.
        #
        reversed_spec_dict = reverse_all_dicts(spec.to_dict(hash=hash_type))

        #
        # Dump to YAML and JSON
        #
        yaml_string = syaml.dump(spec_dict, default_flow_style=False)
        reversed_yaml_string = syaml.dump(reversed_spec_dict,
                                          default_flow_style=False)
        json_string = sjson.dump(spec_dict)
        reversed_json_string = sjson.dump(reversed_spec_dict)

        #
        # Do many consistency checks
        #

        # spec yaml is ordered like the spec dict
        assert yaml_string == spec_yaml
        assert json_string == spec_json

        # reversed string is different from the original, so it
        # *would* generate a different hash
        assert yaml_string != reversed_yaml_string
        assert json_string != reversed_json_string

        # build specs from the "wrongly" ordered data
        round_trip_yaml_spec = Spec.from_yaml(yaml_string)
        round_trip_json_spec = Spec.from_json(json_string)
        round_trip_reversed_yaml_spec = Spec.from_yaml(
            reversed_yaml_string
        )
        round_trip_reversed_json_spec = Spec.from_yaml(
            reversed_json_string
        )

        # Strip spec if we stripped the yaml
        spec = spec.copy(deps=hash_type.deptype)

        # specs are equal to the original
        assert spec == round_trip_yaml_spec
        assert spec == round_trip_json_spec

        assert spec == round_trip_reversed_yaml_spec
        assert spec == round_trip_reversed_json_spec
        assert round_trip_yaml_spec == round_trip_reversed_yaml_spec
        assert round_trip_json_spec == round_trip_reversed_json_spec
        # dag_hashes are equal
        assert spec.dag_hash() == round_trip_yaml_spec.dag_hash()
        assert spec.dag_hash() == round_trip_json_spec.dag_hash()
        assert spec.dag_hash() == round_trip_reversed_yaml_spec.dag_hash()
        assert spec.dag_hash() == round_trip_reversed_json_spec.dag_hash()

        # full_hashes are equal if we round-tripped by build_hash or full_hash
        if hash_type in (ht.build_hash, ht.full_hash):
            spec.concretize()
            round_trip_yaml_spec.concretize()
            round_trip_json_spec.concretize()
            round_trip_reversed_yaml_spec.concretize()
            round_trip_reversed_json_spec.concretize()
            assert spec.full_hash() == round_trip_yaml_spec.full_hash()
            assert spec.full_hash() == round_trip_json_spec.full_hash()
            assert spec.full_hash() == round_trip_reversed_yaml_spec.full_hash()
            assert spec.full_hash() == round_trip_reversed_json_spec.full_hash()


@pytest.mark.parametrize("module", [
    spack.spec,
    spack.architecture,
    spack.version,
])
def test_hashes_use_no_python_dicts(module):
    """Coarse check to make sure we don't use dicts in Spec.to_node_dict().

    Python dicts are not guaranteed to iterate in a deterministic order
    (at least not in all python versions) so we need to use lists and
    syaml_dicts.  syaml_dicts are ordered and ensure that hashes in Spack
    are deterministic.

    This test is intended to handle cases that are not covered by the
    consistency checks above, or that would be missed by a dynamic check.
    This test traverses the ASTs of functions that are used in our hash
    algorithms, finds instances of dictionaries being constructed, and
    prints out the line numbers where they occur.

    """
    class FindFunctions(ast.NodeVisitor):
        """Find a function definition called to_node_dict."""
        def __init__(self):
            self.nodes = []

        def visit_FunctionDef(self, node):  # noqa
            if node.name in ("to_node_dict", "to_dict", "to_dict_or_value"):
                self.nodes.append(node)

    class FindDicts(ast.NodeVisitor):
        """Find source locations of dicts in an AST."""
        def __init__(self, filename):
            self.nodes = []
            self.filename = filename

        def add_error(self, node):
            self.nodes.append(
                "Use syaml_dict instead of dict at %s:%s:%s"
                % (self.filename, node.lineno, node.col_offset)
            )

        def visit_Dict(self, node):  # noqa
            self.add_error(node)

        def visit_Call(self, node):  # noqa
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr

            if name == 'dict':
                self.add_error(node)

    find_functions = FindFunctions()
    module_ast = ast.parse(inspect.getsource(module))
    find_functions.visit(module_ast)

    find_dicts = FindDicts(module.__file__)
    for node in find_functions.nodes:
        find_dicts.visit(node)

    # fail with offending lines if we found some dicts.
    assert [] == find_dicts.nodes


def reverse_all_dicts(data):
    """Descend into data and reverse all the dictionaries"""
    if isinstance(data, dict):
        return syaml_dict(reversed(
            [(reverse_all_dicts(k), reverse_all_dicts(v))
             for k, v in data.items()]))
    elif isinstance(data, (list, tuple)):
        return type(data)(reverse_all_dicts(elt) for elt in data)
    else:
        return data


def check_specs_equal(original_spec, spec_yaml_path):
    with open(spec_yaml_path, 'r') as fd:
        spec_yaml = fd.read()
        spec_from_yaml = Spec.from_yaml(spec_yaml)
        return original_spec.eq_dag(spec_from_yaml)


def test_save_dependency_spec_yamls_subset(tmpdir, config):
    output_path = str(tmpdir.mkdir('spec_yamls'))

    default = ('build', 'link')

    mock_repo = MockPackageMultiRepo()
    g = mock_repo.add_package('g', [], [])
    f = mock_repo.add_package('f', [], [])
    e = mock_repo.add_package('e', [], [])
    d = mock_repo.add_package('d', [f, g], [default, default])
    c = mock_repo.add_package('c', [], [])
    b = mock_repo.add_package('b', [d, e], [default, default])
    mock_repo.add_package('a', [b, c], [default, default])

    with repo.use_repositories(mock_repo):
        spec_a = Spec('a')
        spec_a.concretize()
        b_spec = spec_a['b']
        c_spec = spec_a['c']
        spec_a_yaml = spec_a.to_yaml(hash=ht.build_hash)

        save_dependency_spec_yamls(spec_a_yaml, output_path, ['b', 'c'])

        assert check_specs_equal(b_spec, os.path.join(output_path, 'b.yaml'))
        assert check_specs_equal(c_spec, os.path.join(output_path, 'c.yaml'))
