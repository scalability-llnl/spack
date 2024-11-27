# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os.path

import jsonschema
import pytest

import spack.paths
import spack.schema


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
    with open(meta_schema_file) as f:
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
    with pytest.raises(jsonschema.ValidationError, match="unexpected tokens"):
        v.validate(data)


@pytest.mark.regression("9857")
def test_module_suffixes(module_suffixes_schema):
    v = spack.schema.Validator(module_suffixes_schema)
    data = {"tcl": {"all": {"suffixes": {"^python@2.7@": "py2.7"}}}}

    with pytest.raises(jsonschema.ValidationError, match="unexpected tokens"):
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
