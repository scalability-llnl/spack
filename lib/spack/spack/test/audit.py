# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.audit
import spack.config


@pytest.mark.parametrize(
    # PKG-PROPERTIES are ubiquitous in mock packages, since they don't use sha256
    # and they don't change the example.com URL very often.
    "packages,expected_errors",
    [
        # A non existing variant is used in a conflict directive
        (["wrong-variant-in-conflicts"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # The package declares a non-existing dependency
        (["missing-dependency"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # The package use a non existing variant in a depends_on directive
        (["wrong-variant-in-depends-on"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # This package has a GitHub pull request commit patch URL
        (["invalid-github-pull-commits-patch-url"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # This package has a GitHub patch URL without full_index=1
        (["invalid-github-patch-url"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # This package has invalid GitLab patch URLs
        (["invalid-gitlab-patch-url"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # This package has invalid GitLab patch URLs
        (["invalid-selfhosted-gitlab-patch-url"], ["PKG-DIRECTIVES", "PKG-PROPERTIES"]),
        # This package has a stand-alone test method in build-time callbacks
        (["fail-test-audit"], ["PKG-PROPERTIES"]),
        # This package implements and uses several deprecated stand-alone
        # test methods
        (["fail-test-audit-deprecated"], ["PKG-DEPRECATED-ATTRIBUTES"]),
        # This package has stand-alone test methods without non-trivial docstrings
        (["fail-test-audit-docstring"], ["PKG-PROPERTIES"]),
        # This package has a stand-alone test method without an implementation
        (["fail-test-audit-impl"], ["PKG-PROPERTIES"]),
        # This package has no issues
        (["mpileaks"], None),
        # This package has a conflict with a trigger which cannot constrain the constraint
        # Should not raise an error
        (["unconstrainable-conflict"], None),
    ],
)
def test_package_audits(packages, expected_errors, mock_packages):
    reports = spack.audit.run_group("packages", pkgs=packages)

    # Check that errors were reported only for the expected failure
    actual_errors = [check for check, errors in reports if errors]
    msg = "\n".join([str(e) for _, errors in reports for e in errors])
    if expected_errors:
        assert expected_errors == actual_errors, msg
    else:
        assert not actual_errors, msg


# Data used in the test below to audit the double definition of a compiler
_double_compiler_definition = [
    {
        "compiler": {
            "spec": "gcc@9.0.1",
            "paths": {
                "cc": "/usr/bin/gcc-9",
                "cxx": "/usr/bin/g++-9",
                "f77": "/usr/bin/gfortran-9",
                "fc": "/usr/bin/gfortran-9",
            },
            "flags": {},
            "operating_system": "ubuntu18.04",
            "target": "x86_64",
            "modules": [],
            "environment": {},
            "extra_rpaths": [],
        }
    },
    {
        "compiler": {
            "spec": "gcc@9.0.1",
            "paths": {
                "cc": "/usr/bin/gcc-9",
                "cxx": "/usr/bin/g++-9",
                "f77": "/usr/bin/gfortran-9",
                "fc": "/usr/bin/gfortran-9",
            },
            "flags": {"cflags": "-O3"},
            "operating_system": "ubuntu18.04",
            "target": "x86_64",
            "modules": [],
            "environment": {},
            "extra_rpaths": [],
        }
    },
]


@pytest.mark.parametrize(
    "config_section,data,failing_check",
    [
        # Double compiler definitions in compilers.yaml
        ("compilers", _double_compiler_definition, "CFG-COMPILER"),
        # Multiple definitions of the same external spec in packages.yaml
        (
            "packages",
            {
                "mpileaks": {
                    "externals": [
                        {"spec": "mpileaks@1.0.0", "prefix": "/"},
                        {"spec": "mpileaks@1.0.0", "prefix": "/usr"},
                    ]
                }
            },
            "CFG-PACKAGES",
        ),
    ],
)
def test_config_audits(config_section, data, failing_check):
    with spack.config.override(config_section, data):
        reports = spack.audit.run_group("configs")
        assert any((check == failing_check) and errors for check, errors in reports)
