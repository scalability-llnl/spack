# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test Spack's custom YAML format."""
import io

import pytest

import spack.util.spack_yaml as syaml


@pytest.fixture()
def data():
    """Returns the data loaded from a test file"""
    test_file = """\
config_file:
  x86_64:
    foo: /path/to/foo
    bar: /path/to/bar
    baz: /path/to/baz
  some_list:
    - item 1
    - item 2
    - item 3
  another_list:
    [ 1, 2, 3 ]
  some_key: some_string
"""
    return syaml.load_config(test_file)


def test_parse(data):
    expected = {
        "config_file": syaml.syaml_dict(
            [
                (
                    "x86_64",
                    syaml.syaml_dict(
                        [("foo", "/path/to/foo"), ("bar", "/path/to/bar"), ("baz", "/path/to/baz")]
                    ),
                ),
                ("some_list", ["item 1", "item 2", "item 3"]),
                ("another_list", [1, 2, 3]),
                ("some_key", "some_string"),
            ]
        )
    }

    assert data == expected


def test_dict_order(data):
    expected_order = ["x86_64", "some_list", "another_list", "some_key"]
    assert list(data["config_file"].keys()) == expected_order

    expected_order = ["foo", "bar", "baz"]
    assert list(data["config_file"]["x86_64"].keys()) == expected_order


def test_line_numbers(data):
    def check(obj, start_line, end_line):
        assert obj._start_mark.line == start_line
        assert obj._end_mark.line == end_line

    check(data, 0, 12)
    check(data["config_file"], 1, 12)
    check(data["config_file"]["x86_64"], 2, 5)
    check(data["config_file"]["x86_64"]["foo"], 2, 2)
    check(data["config_file"]["x86_64"]["bar"], 3, 3)
    check(data["config_file"]["x86_64"]["baz"], 4, 4)
    check(data["config_file"]["some_list"], 6, 9)
    check(data["config_file"]["some_list"][0], 6, 6)
    check(data["config_file"]["some_list"][1], 7, 7)
    check(data["config_file"]["some_list"][2], 8, 8)
    check(data["config_file"]["another_list"], 10, 10)
    check(data["config_file"]["some_key"], 11, 11)


def test_yaml_aliases():
    aliased_list_1 = ["foo"]
    aliased_list_2 = []
    dict_with_aliases = {
        "a": aliased_list_1,
        "b": aliased_list_1,
        "c": aliased_list_1,
        "d": aliased_list_2,
        "e": aliased_list_2,
        "f": aliased_list_2,
    }
    stringio = io.StringIO()
    syaml.dump(dict_with_aliases, stream=stringio)

    # ensure no YAML aliases appear in syaml dumps.
    assert "*id" not in stringio.getvalue()


@pytest.mark.parametrize(
    "initial_content,expected_final_content",
    [
        # List are dumped indented as the outer attribute
        (
            """spack:
  #foo
  specs:
  # bar
  - zlib
""",
            None,
        ),
        (
            """spack:
  #foo
  specs:
    # bar
    - zlib
""",
            """spack:
  #foo
  specs:
    # bar
  - zlib
""",
        ),
    ],
)
@pytest.mark.not_on_windows(reason="fails on Windows")
def test_round_trip_configuration(initial_content, expected_final_content, tmp_path):
    """Test that configuration can be loaded and dumped without too many changes"""
    file = tmp_path / "test.yaml"
    file.write_text(initial_content)
    final_content = io.StringIO()

    data = syaml.load_config(file)
    syaml.dump_config(data, stream=final_content)

    if expected_final_content is None:
        expected_final_content = initial_content

    assert final_content.getvalue() == expected_final_content
