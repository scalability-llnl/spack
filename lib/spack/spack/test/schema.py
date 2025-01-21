# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os.path

import jsonschema
import pytest

import spack.paths
import spack.schema
import spack.util.spack_yaml as syaml


@pytest.fixture()
def validate_spec_schema():
    return {
        "type": "object",
        "validate_spec": True,
        "patternProperties": {r"\w[\w-]*": {"type": "string"}},
    }


@pytest.fixture()
def module_suffixes_schema():
    return {
        "type": "object",
        "properties": {
            "tcl": {
                "type": "object",
                "patternProperties": {
                    r"\w[\w-]*": {
                        "type": "object",
                        "properties": {
                            "suffixes": {
                                "validate_spec": True,
                                "patternProperties": {r"\w[\w-]*": {"type": "string"}},
                            }
                        },
                    }
                },
            }
        },
    }


@pytest.fixture(scope="module")
def meta_schema():
    """Meta schema for JSON schema validation (Draft 4)"""
    meta_schema_file = os.path.join(spack.paths.test_path, "data", "jsonschema_meta.json")
    with open(meta_schema_file, encoding="utf-8") as f:
        ms = json.load(f)
    return ms


@pytest.mark.regression("9857")
def test_validate_spec(validate_spec_schema):
    v = spack.schema.Validator(validate_spec_schema)
    data = {"foo@3.7": "bar"}

    # Validate good data (the key is a spec)
    v.validate(data)

    # Check that invalid data throws
    data["^python@3.7@"] = "baz"
    with pytest.raises(jsonschema.ValidationError, match="is not a valid spec"):
        v.validate(data)


@pytest.mark.regression("9857")
def test_module_suffixes(module_suffixes_schema):
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python@2.7@": "py2.7"}}}}

    with pytest.raises(jsonschema.ValidationError, match="is not a valid spec"):
        v.validate(data)


@pytest.mark.regression("10246")
@pytest.mark.parametrize(
    "config_name",
    [
        "compilers",
        "config",
        "definitions",
        "env",
        "merged",
        "mirrors",
        "modules",
        "packages",
        "repos",
    ],
)
def test_schema_validation(meta_schema, config_name):
    import importlib

    module_name = "spack.schema.{0}".format(config_name)
    module = importlib.import_module(module_name)
    schema = getattr(module, "schema")

    # If this validation throws the test won't pass
    jsonschema.validate(schema, meta_schema)


def test_deprecated_properties(module_suffixes_schema):
    # Test that an error is reported when 'error: True'
    msg_fmt = r"{name} is deprecated"
    module_suffixes_schema["deprecatedProperties"] = [
        {"names": ["tcl"], "message": msg_fmt, "error": True}
    ]
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python": "py"}}}}

    expected_match = "tcl is deprecated"
    with pytest.raises(jsonschema.ValidationError, match=expected_match):
        v.validate(data)

    # Test that just a warning is reported when 'error: False'
    module_suffixes_schema["deprecatedProperties"] = [
        {"names": ["tcl"], "message": msg_fmt, "error": False}
    ]
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python": "py"}}}}
    # The next validation doesn't raise anymore
    v.validate(data)


def test_ordereddict_merge_order():
    """ "Test that source keys come before dest keys in merge_yaml results."""
    source = syaml.syaml_dict([("k1", "v1"), ("k2", "v2"), ("k3", "v3")])

    dest = syaml.syaml_dict([("k4", "v4"), ("k3", "WRONG"), ("k5", "v5")])

    result = spack.schema.merge_yaml(dest, source)
    assert "WRONG" not in result.values()

    expected_keys = ["k1", "k2", "k3", "k4", "k5"]
    expected_items = [("k1", "v1"), ("k2", "v2"), ("k3", "v3"), ("k4", "v4"), ("k5", "v5")]
    assert expected_keys == list(result.keys())
    assert expected_items == list(result.items())


def test_list_merge_order():
    """ "Test that source lists are prepended to dest."""
    source = ["a", "b", "c"]
    dest = ["d", "e", "f"]

    result = spack.schema.merge_yaml(dest, source)

    assert ["a", "b", "c", "d", "e", "f"] == result
