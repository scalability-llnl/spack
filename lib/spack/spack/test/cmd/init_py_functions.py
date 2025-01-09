# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

import spack.config
import spack.environment as ev
import spack.error
import spack.solver.asp as asp
import spack.store
from spack.cmd import (
    CommandNameError,
    PythonNameError,
    cmd_name,
    matching_specs_from_env,
    parse_specs,
    python_name,
    require_cmd_name,
    require_python_name,
)


def test_require_python_name():
    """Python module names should not contain dashes---ensure that
    require_python_name() raises the appropriate exception if one is
    detected.
    """
    require_python_name("okey_dokey")
    with pytest.raises(PythonNameError):
        require_python_name("okey-dokey")
    require_python_name(python_name("okey-dokey"))


def test_require_cmd_name():
    """By convention, Spack command names should contain dashes rather than
    underscores---ensure that require_cmd_name() raises the appropriate
    exception if underscores are detected.
    """
    require_cmd_name("okey-dokey")
    with pytest.raises(CommandNameError):
        require_cmd_name("okey_dokey")
    require_cmd_name(cmd_name("okey_dokey"))


@pytest.mark.parametrize(
    "unify,spec_strs,error",
    [
        # single spec
        (True, ["zmpi"], None),
        (False, ["mpileaks"], None),
        # multiple specs, some from hash some from file
        (True, ["zmpi", "mpileaks^zmpi", "libelf"], None),
        (True, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], spack.error.SpecError),
        (False, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], None),
    ],
)
def test_special_cases_concretization_parse_specs(
    unify, spec_strs, error, monkeypatch, mutable_config, mutable_database, tmpdir
):
    """Test that special cases in parse_specs(concretize=True) bypass solver"""

    # monkeypatch to ensure we do not call the actual concretizer
    def _fail(*args, **kwargs):
        assert False

    monkeypatch.setattr(asp.SpackSolverSetup, "setup", _fail)

    spack.config.set("concretizer:unify", unify)

    args = [f"/{spack.store.STORE.db.query(s)[0].dag_hash()}" for s in spec_strs]
    if len(args) > 1:
        # We convert the last one to a specfile input
        filename = tmpdir.join("spec.json")
        spec = parse_specs(args[-1], concretize=True)[0]
        with open(filename, "w", encoding="utf-8") as f:
            spec.to_json(f)
        args[-1] = str(filename)

    if error:
        with pytest.raises(error):
            parse_specs(args, concretize=True)
    else:
        # assertion error from monkeypatch above if test fails
        parse_specs(args, concretize=True)


@pytest.mark.parametrize(
    "unify,spec_strs,error",
    [
        # single spec
        (True, ["zmpi"], None),
        (False, ["mpileaks"], None),
        # multiple specs, some from hash some from file
        (True, ["zmpi", "mpileaks^zmpi", "libelf"], None),
        (True, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], spack.error.SpecError),
        (False, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], None),
    ],
)
def test_special_cases_concretization_matching_specs_from_env(
    unify,
    spec_strs,
    error,
    monkeypatch,
    mutable_config,
    mutable_database,
    tmpdir,
    mutable_mock_env_path,
):
    """Test that special cases in parse_specs(concretize=True) bypass solver"""

    # monkeypatch to ensure we do not call the actual concretizer
    def _fail(*args, **kwargs):
        assert False

    monkeypatch.setattr(asp.SpackSolverSetup, "setup", _fail)

    spack.config.set("concretizer:unify", unify)

    ev.create("test")
    env = ev.read("test")

    args = [f"/{spack.store.STORE.db.query(s)[0].dag_hash()}" for s in spec_strs]
    if len(args) > 1:
        # We convert the last one to a specfile input
        filename = tmpdir.join("spec.json")
        spec = parse_specs(args[-1], concretize=True)[0]
        with open(filename, "w", encoding="utf-8") as f:
            spec.to_json(f)
        args[-1] = str(filename)

    with env:
        specs = parse_specs(args, concretize=False)
        if error:
            with pytest.raises(error):
                matching_specs_from_env(specs)
        else:
            # assertion error from monkeypatch above if test fails
            matching_specs_from_env(specs)
