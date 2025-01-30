# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import re
import sys

import pytest

import spack.paths
from spack.compiler import _parse_non_system_link_dirs

drive = ""
if sys.platform == "win32":
    match = re.search(r"[A-Za-z]:", spack.paths.test_path)
    if match:
        drive = match.group()
root = drive + os.sep

#: directory with sample compiler data
datadir = os.path.join(spack.paths.test_path, "data", "compiler_verbose_output")


@pytest.fixture(autouse=True)
def allow_nonexistent_paths(monkeypatch):
    # Allow nonexistent paths to be detected as part of the output
    # for testing purposes.
    monkeypatch.setattr(os.path, "isdir", lambda x: True)


def check_link_paths(filename, paths):
    with open(os.path.join(datadir, filename), encoding="utf-8") as file:
        output = file.read()
    detected_paths = _parse_non_system_link_dirs(output)

    actual = detected_paths
    expected = paths

    missing_paths = list(x for x in expected if x not in actual)
    assert not missing_paths

    extra_paths = list(x for x in actual if x not in expected)
    assert not extra_paths

    assert actual == expected


def test_icc16_link_paths():
    prefix = os.path.join(root, "usr", "tce", "packages")
    check_link_paths(
        "icc-16.0.3.txt",
        [
            os.path.join(
                prefix,
                "intel",
                "intel-16.0.3",
                "compilers_and_libraries_2016.3.210",
                "linux",
                "compiler",
                "lib",
                "intel64_lin",
            ),
            os.path.join(
                prefix, "gcc", "gcc-4.9.3", "lib64", "gcc", "x86_64-unknown-linux-gnu", "4.9.3"
            ),
            os.path.join(prefix, "gcc", "gcc-4.9.3", "lib64"),
        ],
    )


def test_gcc7_link_paths():
    check_link_paths("gcc-7.3.1.txt", [])


def test_clang4_link_paths():
    check_link_paths("clang-4.0.1.txt", [])


def test_xl_link_paths():
    check_link_paths(
        "xl-13.1.5.txt",
        [
            os.path.join(root, "opt", "ibm", "xlsmp", "4.1.5", "lib"),
            os.path.join(root, "opt", "ibm", "xlmass", "8.1.5", "lib"),
            os.path.join(root, "opt", "ibm", "xlC", "13.1.5", "lib"),
        ],
    )


def test_cce_link_paths():
    gcc = os.path.join(root, "opt", "gcc")
    cray = os.path.join(root, "opt", "cray")
    check_link_paths(
        "cce-8.6.5.txt",
        [
            os.path.join(gcc, "6.1.0", "snos", "lib64"),
            os.path.join(cray, "dmapp", "default", "lib64"),
            os.path.join(cray, "pe", "mpt", "7.7.0", "gni", "mpich-cray", "8.6", "lib"),
            os.path.join(cray, "pe", "libsci", "17.12.1", "CRAY", "8.6", "x86_64", "lib"),
            os.path.join(cray, "rca", "2.2.16-6.0.5.0_15.34__g5e09e6d.ari", "lib64"),
            os.path.join(cray, "pe", "pmi", "5.0.13", "lib64"),
            os.path.join(cray, "xpmem", "2.2.4-6.0.5.0_4.8__g35d5e73.ari", "lib64"),
            os.path.join(cray, "dmapp", "7.1.1-6.0.5.0_49.8__g1125556.ari", "lib64"),
            os.path.join(cray, "ugni", "6.0.14-6.0.5.0_16.9__g19583bb.ari", "lib64"),
            os.path.join(cray, "udreg", "2.3.2-6.0.5.0_13.12__ga14955a.ari", "lib64"),
            os.path.join(cray, "alps", "6.5.28-6.0.5.0_18.6__g13a91b6.ari", "lib64"),
            os.path.join(cray, "pe", "atp", "2.1.1", "libApp"),
            os.path.join(cray, "pe", "cce", "8.6.5", "cce", "x86_64", "lib"),
            os.path.join(cray, "wlm_detect", "1.3.2-6.0.5.0_3.1__g388ccd5.ari", "lib64"),
            os.path.join(gcc, "6.1.0", "snos", "lib", "gcc", "x86_64-suse-linux", "6.1.0"),
            os.path.join(
                cray, "pe", "cce", "8.6.5", "binutils", "x86_64", "x86_64-unknown-linux-gnu", "lib"
            ),
        ],
    )


def test_clang_apple_ld_link_paths():
    check_link_paths(
        "clang-9.0.0-apple-ld.txt",
        [
            os.path.join(
                root,
                "Applications",
                "Xcode.app",
                "Contents",
                "Developer",
                "Platforms",
                "MacOSX.platform",
                "Developer",
                "SDKs",
                "MacOSX10.13.sdk",
                "usr",
                "lib",
            )
        ],
    )


def test_nag_mixed_gcc_gnu_ld_link_paths():
    # This is a test of a mixed NAG/GCC toolchain, i.e. 'cxx' is set to g++ and
    # is used for the rpath detection. The reference compiler output is a
    # result of
    # '/path/to/gcc/bin/g++ -Wl,-v ./main.c'.
    prefix = os.path.join(
        root,
        "scratch",
        "local1",
        "spack",
        "opt",
        "spack",
        "gcc-6.3.0-haswell",
        "gcc-6.5.0-4sdjgrs",
    )

    check_link_paths(
        "collect2-6.3.0-gnu-ld.txt",
        [
            os.path.join(prefix, "lib", "gcc", "x86_64-pc-linux-gnu", "6.5.0"),
            os.path.join(prefix, "lib64"),
            os.path.join(prefix, "lib"),
        ],
    )


def test_nag_link_paths():
    # This is a test of a NAG-only toolchain, i.e. 'cc' and 'cxx' are empty,
    # and therefore 'fc' is used for the rpath detection). The reference
    # compiler output is a result of
    # 'nagfor -Wc=/path/to/gcc/bin/gcc -Wl,-v ./main.c'.
    prefix = os.path.join(
        root,
        "scratch",
        "local1",
        "spack",
        "opt",
        "spack",
        "gcc-6.3.0-haswell",
        "gcc-6.5.0-4sdjgrs",
    )

    check_link_paths(
        "nag-6.2-gcc-6.5.0.txt",
        [
            os.path.join(prefix, "lib", "gcc", "x86_64-pc-linux-gnu", "6.5.0"),
            os.path.join(prefix, "lib64"),
            os.path.join(prefix, "lib"),
        ],
    )


def test_obscure_parsing_rules():
    paths = [
        os.path.join(root, "first", "path"),
        os.path.join(root, "second", "path"),
        os.path.join(root, "third", "path"),
    ]

    # TODO: add a comment explaining why this happens
    if sys.platform == "win32":
        paths.remove(os.path.join(root, "second", "path"))

    check_link_paths("obscure-parsing-rules.txt", paths)
