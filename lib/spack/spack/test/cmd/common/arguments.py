# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.environment as ev
import spack.main


@pytest.fixture()
def job_parser():
    # --jobs needs to write to a command_line config scope, so this is the only
    # scope we create.
    p = argparse.ArgumentParser()
    arguments.add_common_arguments(p, ["jobs"])
    scopes = [spack.config.InternalConfigScope("command_line", {"config": {}})]

    with spack.config.use_configuration(*scopes):
        yield p


def test_setting_jobs_flag(job_parser):
    namespace = job_parser.parse_args(["-j", "24"])
    assert namespace.jobs == 24
    assert spack.config.get("config:build_jobs", scope="command_line") == 24


def test_omitted_job_flag(job_parser):
    namespace = job_parser.parse_args([])
    assert namespace.jobs is None
    assert spack.config.get("config:build_jobs") is None


def test_negative_integers_not_allowed_for_parallel_jobs(job_parser):
    with pytest.raises(ValueError) as exc_info:
        job_parser.parse_args(["-j", "-2"])

    assert "expected a positive integer" in str(exc_info.value)


@pytest.mark.parametrize(
    "specs,cflags,propagation,negated_variants",
    [
        (['coreutils cflags="-O3 -g"'], ["-O3", "-g"], [False, False], []),
        (['coreutils cflags=="-O3 -g"'], ["-O3", "-g"], [True, True], []),
        (["coreutils", "cflags=-O3 -g"], ["-O3", "-g"], [False, False], []),
        (["coreutils", "cflags==-O3 -g"], ["-O3", "-g"], [True, True], []),
        (["coreutils", "cflags=-O3", "-g"], ["-O3"], [False], ["g"]),
    ],
)
@pytest.mark.regression("12951")
def test_parse_spec_flags_with_spaces(specs, cflags, propagation, negated_variants):
    spec_list = spack.cmd.parse_specs(specs)
    assert len(spec_list) == 1

    s = spec_list.pop()

    compiler_flags = [flag for flag in s.compiler_flags["cflags"]]
    flag_propagation = [flag.propagate for flag in s.compiler_flags["cflags"]]

    assert compiler_flags == cflags
    assert flag_propagation == propagation
    assert list(s.variants.keys()) == negated_variants
    for v in negated_variants:
        assert "~{0}".format(v) in s


def test_match_spec_env(mock_packages, mutable_mock_env_path):
    """
    Concretize a spec with non-default options in an environment. Make
    sure that when we ask for a matching spec when the environment is
    active that we get the instance concretized in the environment.
    """
    # Initial sanity check: we are planning on choosing a non-default
    # value, so make sure that is in fact not the default.
    check_defaults = spack.cmd.parse_specs(["pkg-a"], concretize=True)[0]
    assert not check_defaults.satisfies("foobar=baz")

    e = ev.create("test")
    e.add("pkg-a foobar=baz")
    e.concretize()
    with e:
        env_spec = spack.cmd.matching_spec_from_env(spack.cmd.parse_specs(["pkg-a"])[0])
        assert env_spec.satisfies("foobar=baz")
        assert env_spec.concrete


def test_multiple_env_match_raises_error(mock_packages, mutable_mock_env_path):
    e = ev.create("test")
    e.add("pkg-a foobar=baz")
    e.add("pkg-a foobar=fee")
    e.concretize()
    with e:
        with pytest.raises(ev.SpackEnvironmentError) as exc_info:
            spack.cmd.matching_spec_from_env(spack.cmd.parse_specs(["pkg-a"])[0])

    assert "matches multiple specs" in exc_info.value.message


def test_root_and_dep_match_returns_root(mock_packages, mutable_mock_env_path):
    e = ev.create("test")
    e.add("pkg-b@0.9")
    e.add("pkg-a foobar=bar")  # Depends on b, should choose b@1.0
    e.concretize()
    with e:
        # This query matches the root b and b as a dependency of a. In that
        # case the root instance should be preferred.
        env_spec1 = spack.cmd.matching_spec_from_env(spack.cmd.parse_specs(["pkg-b"])[0])
        assert env_spec1.satisfies("@0.9")

        env_spec2 = spack.cmd.matching_spec_from_env(spack.cmd.parse_specs(["pkg-b@1.0"])[0])
        assert env_spec2


@pytest.mark.parametrize(
    "arg,conf",
    [
        ("--reuse", True),
        ("--fresh", False),
        ("--reuse-deps", "dependencies"),
        ("--fresh-roots", "dependencies"),
    ],
)
def test_concretizer_arguments(mutable_config, mock_packages, arg, conf):
    """Ensure that ConfigSetAction is doing the right thing."""
    spec = spack.main.SpackCommand("spec")

    assert spack.config.get("concretizer:reuse", None, scope="command_line") is None

    spec(arg, "zlib")

    assert spack.config.get("concretizer:reuse", None) == conf
    assert spack.config.get("concretizer:reuse", None, scope="command_line") == conf


def test_use_buildcache_type():
    assert arguments.use_buildcache("only") == ("only", "only")
    assert arguments.use_buildcache("never") == ("never", "never")
    assert arguments.use_buildcache("auto") == ("auto", "auto")
    assert arguments.use_buildcache("package:never,dependencies:only") == ("never", "only")
    assert arguments.use_buildcache("only,package:never") == ("never", "only")
    assert arguments.use_buildcache("package:only,package:never") == ("never", "auto")
    assert arguments.use_buildcache("auto , package: only") == ("only", "auto")

    with pytest.raises(argparse.ArgumentTypeError):
        assert arguments.use_buildcache("pkg:only,deps:never")

    with pytest.raises(argparse.ArgumentTypeError):
        assert arguments.use_buildcache("sometimes")
