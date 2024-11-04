# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

import spack.environment as ev
import spack.error
import spack.spec
import spack.store
from spack.main import SpackCommand, SpackCommandError

pytestmark = pytest.mark.usefixtures("mutable_config", "mutable_mock_repo")

spec = SpackCommand("spec")


def test_spec():
    output = spec("mpileaks")

    assert "mpileaks@2.3" in output
    assert "callpath@1.0" in output
    assert "dyninst@8.2" in output
    assert "libdwarf@20130729" in output
    assert "libelf@0.8.1" in output
    assert "mpich@3.0.4" in output


def test_spec_concretizer_args(mutable_database, do_not_check_runtimes_on_reuse):
    """End-to-end test of CLI concretizer prefs.

    It's here to make sure that everything works from CLI
    options to `solver.py`, and that config options are not
    lost along the way.
    """
    # remove two non-preferred mpileaks installations
    # so that reuse will pick up the zmpi one
    uninstall = SpackCommand("uninstall")
    uninstall("-y", "mpileaks^mpich")
    uninstall("-y", "mpileaks^mpich2")

    # get the hash of mpileaks^zmpi
    mpileaks_zmpi = spack.store.STORE.db.query_one("mpileaks^zmpi")
    h = mpileaks_zmpi.dag_hash()[:7]

    output = spec("--fresh", "-l", "mpileaks")
    assert h not in output

    output = spec("--reuse", "-l", "mpileaks")
    assert h in output


def test_spec_parse_dependency_variant_value():
    """Verify that we can provide multiple key=value variants to multiple separate
    packages within a spec string."""
    output = spec("multivalue-variant fee=barbaz ^ pkg-a foobar=baz")

    assert "fee=barbaz" in output
    assert "foobar=baz" in output


def test_spec_parse_cflags_quoting():
    """Verify that compiler flags can be provided to a spec from the command line."""
    output = spec("--yaml", 'gcc cflags="-Os -pipe" cxxflags="-flto -Os"')
    gh_flagged = spack.spec.Spec.from_yaml(output)

    assert ["-Os", "-pipe"] == gh_flagged.compiler_flags["cflags"]
    assert ["-flto", "-Os"] == gh_flagged.compiler_flags["cxxflags"]


def test_spec_yaml():
    output = spec("--yaml", "mpileaks")

    mpileaks = spack.spec.Spec.from_yaml(output)
    assert "mpileaks" in mpileaks
    assert "callpath" in mpileaks
    assert "dyninst" in mpileaks
    assert "libdwarf" in mpileaks
    assert "libelf" in mpileaks
    assert "mpich" in mpileaks


def test_spec_json():
    output = spec("--json", "mpileaks")

    mpileaks = spack.spec.Spec.from_json(output)
    assert "mpileaks" in mpileaks
    assert "callpath" in mpileaks
    assert "dyninst" in mpileaks
    assert "libdwarf" in mpileaks
    assert "libelf" in mpileaks
    assert "mpich" in mpileaks


def test_spec_format(mutable_database):
    output = spec("--format", "{name}-{^mpi.name}", "mpileaks^mpich")
    assert output.rstrip("\n") == "mpileaks-mpich"


def _parse_types(string):
    """Parse deptypes for specs from `spack spec -t` output."""
    lines = string.strip().split("\n")

    result = {}
    for line in lines:
        match = re.match(r"\[([^]]*)\]\s*\^?([^@]*)@", line)
        if match:
            types, name = match.groups()
            result.setdefault(name, []).append(types)
            result[name] = sorted(result[name])
    return result


def test_spec_deptypes_nodes():
    output = spec("--types", "--cover", "nodes", "--no-install-status", "dt-diamond")
    types = _parse_types(output)

    assert types["dt-diamond"] == ["    "]
    assert types["dt-diamond-left"] == ["bl  "]
    assert types["dt-diamond-right"] == ["bl  "]
    assert types["dt-diamond-bottom"] == ["blr "]


def test_spec_deptypes_edges():
    output = spec("--types", "--cover", "edges", "--no-install-status", "dt-diamond")
    types = _parse_types(output)

    assert types["dt-diamond"] == ["    "]
    assert types["dt-diamond-left"] == ["bl  "]
    assert types["dt-diamond-right"] == ["bl  "]
    assert types["dt-diamond-bottom"] == ["b   ", "blr "]


def test_spec_returncode():
    with pytest.raises(SpackCommandError):
        spec()
    assert spec.returncode == 1


def test_spec_parse_error():
    with pytest.raises(spack.error.SpecSyntaxError) as e:
        spec("1.15:")

    # make sure the error is formatted properly
    error_msg = "unexpected tokens in the spec string\n1.15:\n    ^"
    assert error_msg in str(e.value)


def test_env_aware_spec(mutable_mock_env_path):
    env = ev.create("test")
    env.add("mpileaks")

    with env:
        output = spec()
        assert "mpileaks@2.3" in output
        assert "callpath@1.0" in output
        assert "dyninst@8.2" in output
        assert "libdwarf@20130729" in output
        assert "libelf@0.8.1" in output
        assert "mpich@3.0.4" in output


@pytest.mark.parametrize(
    "name, version, error",
    [
        ("develop-branch-version", "f3c7206350ac8ee364af687deaae5c574dcfca2c=develop", None),
        ("develop-branch-version", "git." + "a" * 40 + "=develop", None),
        ("callpath", "f3c7206350ac8ee364af687deaae5c574dcfca2c=1.0", spack.error.FetchError),
        ("develop-branch-version", "git.foo=0.2.15", None),
    ],
)
def test_spec_version_assigned_git_ref_as_version(name, version, error):
    if error:
        with pytest.raises(error):
            output = spec(name + "@" + version)
    else:
        output = spec(name + "@" + version)
        assert version in output
