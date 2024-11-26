# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module contains jsonschema files for all of Spack's YAML formats."""
import typing
import warnings

import llnl.util.lang

from spack.error import SpecSyntaxError


class DeprecationMessage(typing.NamedTuple):
    message: str
    error: bool


# jsonschema is imported lazily as it is heavy to import
# and increases the start-up time
def _make_validator():
    import jsonschema

    def _validate_spec(validator, is_spec, instance, schema):
        """Check if the attributes on instance are valid specs."""
        import jsonschema

        import spack.parser

        if not validator.is_type(instance, "object"):
            return

        for spec_str in instance:
            try:
                spack.parser.parse(spec_str)
            except SpecSyntaxError as e:
                yield jsonschema.ValidationError(str(e))

    def _deprecated_properties(validator, deprecated, instance, schema):
        if not (validator.is_type(instance, "object") or validator.is_type(instance, "array")):
            return

        if not deprecated:
            return

        deprecations = {
            name: DeprecationMessage(message=x["message"], error=x["error"])
            for x in deprecated
            for name in x["names"]
        }

        # Get a list of the deprecated properties, return if there is none
        issues = [entry for entry in instance if entry in deprecations]
        if not issues:
            return

        # Process issues
        errors = []
        for name in issues:
            msg = deprecations[name].message.format(name=name)
            if deprecations[name].error:
                errors.append(msg)
            else:
                warnings.warn(msg)

        if errors:
            yield jsonschema.ValidationError("\n".join(errors))

    return jsonschema.validators.extend(
        jsonschema.Draft4Validator,
        {"validate_spec": _validate_spec, "deprecatedProperties": _deprecated_properties},
    )


Validator = llnl.util.lang.Singleton(_make_validator)
