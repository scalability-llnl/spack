# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Test YAML and JSON serialization for specs.

The YAML and JSON formats preserve DAG information in the spec.

"""
import ast
import collections
import collections.abc
import gzip
import inspect
import io
import json
import os

import pytest
import ruamel.yaml

import spack.hash_types as ht
import spack.paths
import spack.repo
import spack.spec
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.version
from spack.spec import Spec, save_dependency_specfiles
from spack.util.spack_yaml import SpackYAMLError, syaml_dict


def check_yaml_round_trip(spec):
    yaml_text = spec.to_yaml()
    spec_from_yaml = Spec.from_yaml(yaml_text)
    assert spec.eq_dag(spec_from_yaml)


def check_json_round_trip(spec):
    json_text = spec.to_json()
    spec_from_json = Spec.from_json(json_text)
    assert spec.eq_dag(spec_from_json)


def test_read_spec_from_signed_json():
    spec_dir = os.path.join(spack.paths.test_path, "data", "mirrors", "signed_json")
    file_name = (
        "linux-ubuntu18.04-haswell-gcc-8.4.0-"
        "zlib-1.2.12-g7otk5dra3hifqxej36m5qzm7uyghqgb.spec.json.sig"
    )
    spec_path = os.path.join(spec_dir, file_name)

    def check_spec(spec_to_check):
        assert spec_to_check.name == "zlib"
        assert spec_to_check._hash == "g7otk5dra3hifqxej36m5qzm7uyghqgb"

    with open(spec_path) as fd:
        s = Spec.from_signed_json(fd)
        check_spec(s)

    with open(spec_path) as fd:
        s = Spec.from_signed_json(fd.read())
        check_spec(s)


@pytest.mark.parametrize(
    "invalid_yaml", ["playing_playlist: {{ action }} playlist {{ playlist_name }}"]
)
def test_invalid_yaml_spec(invalid_yaml):
    with pytest.raises(SpackYAMLError, match="error parsing YAML") as e:
        Spec.from_yaml(invalid_yaml)
    assert invalid_yaml in str(e)


@pytest.mark.parametrize("invalid_json, error_message", [("{13:", "Expecting property name")])
def test_invalid_json_spec(invalid_json, error_message):
    with pytest.raises(sjson.SpackJSONError) as e:
        Spec.from_json(invalid_json)
    exc_msg = str(e.value)
    assert exc_msg.startswith("error parsing JSON spec:")
    assert error_message in exc_msg


@pytest.mark.parametrize(
    "abstract_spec",
    [
        # Externals
        "externaltool",
        "externaltest",
        # Ambiguous version spec
        "mpileaks@1.0:5.0,6.1,7.3+debug~opt",
        # Variants
        "mpileaks+debug~opt",
        'multivalue-variant foo="bar,baz"',
        # Virtuals on edges
        "callpath",
        "mpileaks",
    ],
)
def test_roundtrip_concrete_specs(abstract_spec, default_mock_concretization):
    check_yaml_round_trip(Spec(abstract_spec))
    check_json_round_trip(Spec(abstract_spec))
    concrete_spec = default_mock_concretization(abstract_spec)
    check_yaml_round_trip(concrete_spec)
    check_json_round_trip(concrete_spec)


def test_yaml_subdag(config, mock_packages):
    spec = Spec("mpileaks^mpich+debug")
    spec.concretize()
    yaml_spec = Spec.from_yaml(spec.to_yaml())
    json_spec = Spec.from_json(spec.to_json())

    for dep in ("callpath", "mpich", "dyninst", "libdwarf", "libelf"):
        assert spec[dep].eq_dag(yaml_spec[dep])
        assert spec[dep].eq_dag(json_spec[dep])


@pytest.mark.parametrize("spec_str", ["mpileaks ^zmpi", "dttop", "dtuse"])
def test_using_ordered_dict(default_mock_concretization, spec_str):
    """Checks that we use syaml_dicts for spec serialization.

    Necessary to make sure that dag_hash is stable across python
    versions and processes.
    """

    def descend_and_check(iterable, level=0):
        if isinstance(iterable, collections.abc.Mapping):
            assert isinstance(iterable, syaml_dict)
            return descend_and_check(iterable.values(), level=level + 1)
        max_level = level
        for value in iterable:
            if isinstance(value, collections.abc.Iterable) and not isinstance(value, str):
                nlevel = descend_and_check(value, level=level + 1)
                if nlevel > max_level:
                    max_level = nlevel
        return max_level

    s = default_mock_concretization(spec_str)
    level = descend_and_check(s.to_node_dict())
    # level just makes sure we are doing something here
    assert level >= 5


def test_ordered_read_not_required_for_consistent_dag_hash(config, mock_packages):
    """Make sure ordered serialization isn't required to preserve hashes.

    For consistent hashes, we require that YAML and json documents
    have their keys serialized in a deterministic order. However, we
    don't want to require them to be serialized in order. This
    ensures that is not required.
    """
    specs = ["mpileaks ^zmpi", "dttop", "dtuse"]
    for spec in specs:
        spec = Spec(spec)
        spec.concretize()

        #
        # Dict & corresponding YAML & JSON from the original spec.
        #
        spec_dict = spec.to_dict()
        spec_yaml = spec.to_yaml()
        spec_json = spec.to_json()

        #
        # Make a spec with reversed OrderedDicts for every
        # OrderedDict in the original.
        #
        reversed_spec_dict = reverse_all_dicts(spec.to_dict())

        #
        # Dump to YAML and JSON
        #
        yaml_string = syaml.dump(spec_dict, default_flow_style=False)
        reversed_yaml_string = syaml.dump(reversed_spec_dict, default_flow_style=False)
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
        round_trip_reversed_yaml_spec = Spec.from_yaml(reversed_yaml_string)
        round_trip_reversed_json_spec = Spec.from_yaml(reversed_json_string)

        # Strip spec if we stripped the yaml
        spec = spec.copy(deps=ht.dag_hash.depflag)

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

        # dag_hash is equal after round-trip by dag_hash
        spec.concretize()
        round_trip_yaml_spec.concretize()
        round_trip_json_spec.concretize()
        round_trip_reversed_yaml_spec.concretize()
        round_trip_reversed_json_spec.concretize()
        assert spec.dag_hash() == round_trip_yaml_spec.dag_hash()
        assert spec.dag_hash() == round_trip_json_spec.dag_hash()
        assert spec.dag_hash() == round_trip_reversed_yaml_spec.dag_hash()
        assert spec.dag_hash() == round_trip_reversed_json_spec.dag_hash()


@pytest.mark.parametrize("module", [spack.spec, spack.version])
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

        def visit_FunctionDef(self, node):
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

        def visit_Dict(self, node):
            self.add_error(node)

        def visit_Call(self, node):
            name = None
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr

            if name == "dict":
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
        return syaml_dict(
            reversed([(reverse_all_dicts(k), reverse_all_dicts(v)) for k, v in data.items()])
        )
    elif isinstance(data, (list, tuple)):
        return type(data)(reverse_all_dicts(elt) for elt in data)
    else:
        return data


def check_specs_equal(original_spec, spec_yaml_path):
    with open(spec_yaml_path, "r") as fd:
        spec_yaml = fd.read()
        spec_from_yaml = Spec.from_yaml(spec_yaml)
        return original_spec.eq_dag(spec_from_yaml)


def test_save_dependency_spec_jsons_subset(tmpdir, config):
    output_path = str(tmpdir.mkdir("spec_jsons"))

    builder = spack.repo.MockRepositoryBuilder(tmpdir.mkdir("mock-repo"))
    builder.add_package("pkg-g")
    builder.add_package("pkg-f")
    builder.add_package("pkg-e")
    builder.add_package("pkg-d", dependencies=[("pkg-f", None, None), ("pkg-g", None, None)])
    builder.add_package("pkg-c")
    builder.add_package("pkg-b", dependencies=[("pkg-d", None, None), ("pkg-e", None, None)])
    builder.add_package("pkg-a", dependencies=[("pkg-b", None, None), ("pkg-c", None, None)])

    with spack.repo.use_repositories(builder.root):
        spec_a = Spec("pkg-a").concretized()
        b_spec = spec_a["pkg-b"]
        c_spec = spec_a["pkg-c"]

        save_dependency_specfiles(spec_a, output_path, [Spec("pkg-b"), Spec("pkg-c")])

        assert check_specs_equal(b_spec, os.path.join(output_path, "pkg-b.json"))
        assert check_specs_equal(c_spec, os.path.join(output_path, "pkg-c.json"))


def test_legacy_yaml(tmpdir, install_mockery, mock_packages):
    """Tests a simple legacy YAML with a dependency and ensures spec survives
    concretization."""
    yaml = """
spec:
- a:
    version: '2.0'
    arch:
      platform: linux
      platform_os: rhel7
      target: x86_64
    compiler:
      name: gcc
      version: 8.3.0
    namespace: builtin.mock
    parameters:
      bvv: true
      foo:
      - bar
      foobar: bar
      cflags: []
      cppflags: []
      cxxflags: []
      fflags: []
      ldflags: []
      ldlibs: []
    dependencies:
      b:
        hash: iaapywazxgetn6gfv2cfba353qzzqvhn
        type:
        - build
        - link
    hash: obokmcsn3hljztrmctbscmqjs3xclazz
    full_hash: avrk2tqsnzxeabmxa6r776uq7qbpeufv
    build_hash: obokmcsn3hljztrmctbscmqjs3xclazy
- b:
    version: '1.0'
    arch:
      platform: linux
      platform_os: rhel7
      target: x86_64
    compiler:
      name: gcc
      version: 8.3.0
    namespace: builtin.mock
    parameters:
      cflags: []
      cppflags: []
      cxxflags: []
      fflags: []
      ldflags: []
      ldlibs: []
    hash: iaapywazxgetn6gfv2cfba353qzzqvhn
    full_hash: qvsxvlmjaothtpjluqijv7qfnni3kyyg
    build_hash: iaapywazxgetn6gfv2cfba353qzzqvhy
"""
    spec = Spec.from_yaml(yaml)
    concrete_spec = spec.concretized()
    assert concrete_spec.eq_dag(spec)


#: A well ordered Spec dictionary, using ``OrderdDict``.
#: Any operation that transforms Spec dictionaries should
#: preserve this order.
ordered_spec = collections.OrderedDict(
    [
        (
            "arch",
            collections.OrderedDict(
                [
                    ("platform", "darwin"),
                    ("platform_os", "bigsur"),
                    (
                        "target",
                        collections.OrderedDict(
                            [
                                (
                                    "features",
                                    [
                                        "adx",
                                        "aes",
                                        "avx",
                                        "avx2",
                                        "bmi1",
                                        "bmi2",
                                        "clflushopt",
                                        "f16c",
                                        "fma",
                                        "mmx",
                                        "movbe",
                                        "pclmulqdq",
                                        "popcnt",
                                        "rdrand",
                                        "rdseed",
                                        "sse",
                                        "sse2",
                                        "sse4_1",
                                        "sse4_2",
                                        "ssse3",
                                        "xsavec",
                                        "xsaveopt",
                                    ],
                                ),
                                ("generation", 0),
                                ("name", "skylake"),
                                ("parents", ["broadwell"]),
                                ("vendor", "GenuineIntel"),
                            ]
                        ),
                    ),
                ]
            ),
        ),
        ("compiler", collections.OrderedDict([("name", "apple-clang"), ("version", "13.0.0")])),
        ("name", "zlib"),
        ("namespace", "builtin"),
        (
            "parameters",
            collections.OrderedDict(
                [
                    ("cflags", []),
                    ("cppflags", []),
                    ("cxxflags", []),
                    ("fflags", []),
                    ("ldflags", []),
                    ("ldlibs", []),
                    ("optimize", True),
                    ("pic", True),
                    ("shared", True),
                ]
            ),
        ),
        ("version", "1.2.11"),
    ]
)


@pytest.mark.parametrize(
    "specfile,expected_hash,reader_cls",
    [
        # First version supporting JSON format for specs
        ("specfiles/hdf5.v013.json.gz", "vglgw4reavn65vx5d4dlqn6rjywnq76d", spack.spec.SpecfileV1),
        # Introduces full hash in the format, still has 3 hashes
        ("specfiles/hdf5.v016.json.gz", "stp45yvzte43xdauknaj3auxlxb4xvzs", spack.spec.SpecfileV1),
        # Introduces "build_specs", see https://github.com/spack/spack/pull/22845
        ("specfiles/hdf5.v017.json.gz", "xqh5iyjjtrp2jw632cchacn3l7vqzf3m", spack.spec.SpecfileV2),
        # Use "full hash" everywhere, see https://github.com/spack/spack/pull/28504
        ("specfiles/hdf5.v019.json.gz", "iulacrbz7o5v5sbj7njbkyank3juh6d3", spack.spec.SpecfileV3),
        # Add properties on edges, see https://github.com/spack/spack/pull/34821
        ("specfiles/hdf5.v020.json.gz", "vlirlcgazhvsvtundz4kug75xkkqqgou", spack.spec.SpecfileV4),
    ],
)
def test_load_json_specfiles(specfile, expected_hash, reader_cls):
    fullpath = os.path.join(spack.paths.test_path, "data", specfile)
    with gzip.open(fullpath, "rt", encoding="utf-8") as f:
        data = json.load(f)

    s1 = Spec.from_dict(data)
    s2 = reader_cls.load(data)

    assert s2.dag_hash() == expected_hash
    assert s1.dag_hash() == s2.dag_hash()
    assert s1 == s2
    assert Spec.from_json(s2.to_json()).dag_hash() == s2.dag_hash()

    openmpi_edges = s2.edges_to_dependencies(name="openmpi")
    assert len(openmpi_edges) == 1

    # The virtuals attribute must be a tuple, when read from a
    # JSON or YAML file, not a list
    for edge in s2.traverse_edges():
        assert isinstance(edge.virtuals, tuple), edge


def test_anchorify_1():
    """Test that anchorify replaces duplicate values with references to a single instance, and
    that that results in anchors in the output YAML."""
    before = {"a": [1, 2, 3], "b": [1, 2, 3]}
    after = {"a": [1, 2, 3], "b": [1, 2, 3]}
    syaml.anchorify(after)
    assert before == after
    assert after["a"] is after["b"]

    # Check if anchors are used
    out = io.StringIO()
    ruamel.yaml.YAML().dump(after, out)
    assert (
        out.getvalue()
        == """\
a: &id001
- 1
- 2
- 3
b: *id001
"""
    )


def test_anchorify_2():
    before = {"a": {"b": {"c": True}}, "d": {"b": {"c": True}}, "e": {"c": True}}
    after = {"a": {"b": {"c": True}}, "d": {"b": {"c": True}}, "e": {"c": True}}
    syaml.anchorify(after)
    assert before == after
    assert after["a"] is after["d"]
    assert after["a"]["b"] is after["e"]

    # Check if anchors are used
    out = io.StringIO()
    ruamel.yaml.YAML().dump(after, out)
    assert (
        out.getvalue()
        == """\
a: &id001
  b: &id002
    c: true
d: *id001
e: *id002
"""
    )
