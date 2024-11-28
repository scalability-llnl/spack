# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse

import pytest

import spack.cmd.info
from spack.main import SpackCommand

info = SpackCommand("info")


@pytest.fixture(scope="module")
def parser():
    """Returns the parser for the module command"""
    prs = argparse.ArgumentParser()
    spack.cmd.info.setup_parser(prs)
    return prs


@pytest.fixture()
def print_buffer(monkeypatch):
    buffer = []

    def _print(*args, **kwargs):
        buffer.extend(args)

    monkeypatch.setattr(spack.cmd.info.color, "cprint", _print, raising=False)
    return buffer


@pytest.mark.parametrize(
    "pkg", ["openmpi", "trilinos", "boost", "python", "dealii", "xsdk", "gasnet", "warpx"]
)
@pytest.mark.parametrize("extra_args", [[], ["--variants-by-name"]])
def test_it_just_runs(pkg, extra_args):
    info(pkg, *extra_args)


def test_info_noversion(mock_packages, print_buffer):
    """Check that a mock package with no versions outputs None."""
    info("noversion")

    line_iter = iter(print_buffer)
    for line in line_iter:
        if "version" in line:
            has = [desc in line for desc in ["Preferred", "Safe", "Deprecated"]]
            if not any(has):
                continue
        else:
            continue

        assert "None" in next(line_iter).strip()


@pytest.mark.parametrize(
    "pkg_query,expected", [("zlib", "False"), ("find-externals1", "True (version)")]
)
def test_is_externally_detectable(mock_packages, pkg_query, expected, parser, print_buffer):
    args = parser.parse_args(["--detectable", pkg_query])
    spack.cmd.info.info(parser, args)

    line_iter = iter(print_buffer)
    for line in line_iter:
        if "Externally Detectable" in line:
            is_externally_detectable = next(line_iter).strip()
            assert is_externally_detectable == expected


@pytest.mark.parametrize(
    "pkg_query",
    [
        "hdf5",
        "cloverleaf3d",
        "trilinos",
        "gcc",  # This should ensure --test's c_names processing loop covered
    ],
)
@pytest.mark.parametrize("extra_args", [[], ["--variants-by-name"]])
def test_info_fields(pkg_query, extra_args, parser, print_buffer):
    expected_fields = (
        "Description:",
        "Homepage:",
        "Externally Detectable:",
        "Safe versions:",
        "Variants:",
        "Installation Phases:",
        "Virtual Packages:",
        "Tags:",
        "Licenses:",
    )

    args = parser.parse_args(["--all", pkg_query] + extra_args)
    spack.cmd.info.info(parser, args)

    for text in expected_fields:
        assert any(x for x in print_buffer if text in x)
