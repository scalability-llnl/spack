# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import re
import sys

import pytest

import spack.binary_distribution
import spack.cmd
import spack.parser
import spack.platforms.test
import spack.repo
import spack.spec
from spack.parser import (
    UNIX_FILENAME,
    WINDOWS_FILENAME,
    SpecParser,
    SpecTokenizationError,
    Token,
    TokenType,
)

FAIL_ON_WINDOWS = pytest.mark.xfail(
    sys.platform == "win32",
    raises=(SpecTokenizationError, spack.spec.InvalidHashError),
    reason="Unix style path on Windows",
)

FAIL_ON_UNIX = pytest.mark.xfail(
    sys.platform != "win32", raises=SpecTokenizationError, reason="Windows style path on Unix"
)


def simple_package_name(name):
    """A simple package name in canonical form"""
    return name, [Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value=name)], name


def dependency_with_version(text):
    root, rest = text.split("^")
    dependency, version = rest.split("@")
    return (
        text,
        [
            Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value=root.strip()),
            Token(TokenType.DEPENDENCY, value="^"),
            Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value=dependency.strip()),
            Token(TokenType.VERSION, value=f"@{version}"),
        ],
        text,
    )


def compiler_with_version_range(text):
    return text, [Token(TokenType.COMPILER_AND_VERSION, value=text)], text


@pytest.fixture()
def specfile_for(default_mock_concretization):
    def _specfile_for(spec_str, filename):
        s = default_mock_concretization(spec_str)
        is_json = str(filename).endswith(".json")
        is_yaml = str(filename).endswith(".yaml")
        if not is_json and not is_yaml:
            raise ValueError("wrong extension used for specfile")

        with filename.open("w") as f:
            if is_json:
                f.write(s.to_json())
            else:
                f.write(s.to_yaml())
        return s

    return _specfile_for


@pytest.mark.parametrize(
    "spec_str,tokens,expected_roundtrip",
    [
        # Package names
        simple_package_name("mvapich"),
        simple_package_name("mvapich_foo"),
        simple_package_name("_mvapich_foo"),
        simple_package_name("3dtk"),
        simple_package_name("ns-3-dev"),
        # Single token anonymous specs
        ("%intel", [Token(TokenType.COMPILER, value="%intel")], "%intel"),
        ("@2.7", [Token(TokenType.VERSION, value="@2.7")], "@2.7"),
        ("@2.7:", [Token(TokenType.VERSION, value="@2.7:")], "@2.7:"),
        ("@:2.7", [Token(TokenType.VERSION, value="@:2.7")], "@:2.7"),
        ("+foo", [Token(TokenType.BOOL_VARIANT, value="+foo")], "+foo"),
        ("~foo", [Token(TokenType.BOOL_VARIANT, value="~foo")], "~foo"),
        ("-foo", [Token(TokenType.BOOL_VARIANT, value="-foo")], "~foo"),
        (
            "platform=test",
            [Token(TokenType.KEY_VALUE_PAIR, value="platform=test")],
            "arch=test-None-None",
        ),
        # Multiple tokens anonymous specs
        (
            "languages=go @4.2:",
            [
                Token(TokenType.KEY_VALUE_PAIR, value="languages=go"),
                Token(TokenType.VERSION, value="@4.2:"),
            ],
            "@4.2: languages=go",
        ),
        (
            "@4.2:     languages=go",
            [
                Token(TokenType.VERSION, value="@4.2:"),
                Token(TokenType.KEY_VALUE_PAIR, value="languages=go"),
            ],
            "@4.2: languages=go",
        ),
        (
            "^zlib",
            [
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="zlib"),
            ],
            "^zlib",
        ),
        # Specs with simple dependencies
        (
            "openmpi ^hwloc",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="openmpi"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="hwloc"),
            ],
            "openmpi ^hwloc",
        ),
        (
            "openmpi ^hwloc ^libunwind",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="openmpi"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="hwloc"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="libunwind"),
            ],
            "openmpi ^hwloc ^libunwind",
        ),
        (
            "openmpi      ^hwloc^libunwind",
            [  # White spaces are tested
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="openmpi"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="hwloc"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="libunwind"),
            ],
            "openmpi ^hwloc ^libunwind",
        ),
        # Version after compiler
        (
            "foo %bar@1.0 @2.0",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="foo"),
                Token(TokenType.COMPILER_AND_VERSION, value="%bar@1.0"),
                Token(TokenType.VERSION, value="@2.0"),
            ],
            "foo@2.0%bar@1.0",
        ),
        # Single dependency with version
        dependency_with_version("openmpi ^hwloc@1.2e6"),
        dependency_with_version("openmpi ^hwloc@1.2e6:"),
        dependency_with_version("openmpi ^hwloc@:1.4b7-rc3"),
        dependency_with_version("openmpi ^hwloc@1.2e6:1.4b7-rc3"),
        # Complex specs with multiple constraints
        (
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1+debug~qt_4 ^stackwalker@8.1_1e",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich_foo"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
                Token(TokenType.VERSION, value="@1.2:1.4,1.6"),
                Token(TokenType.COMPILER_AND_VERSION, value="%intel@12.1"),
                Token(TokenType.BOOL_VARIANT, value="+debug"),
                Token(TokenType.BOOL_VARIANT, value="~qt_4"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="stackwalker"),
                Token(TokenType.VERSION, value="@8.1_1e"),
            ],
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1+debug~qt_4 ^stackwalker@8.1_1e",
        ),
        (
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1~qt_4 debug=2 ^stackwalker@8.1_1e",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich_foo"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
                Token(TokenType.VERSION, value="@1.2:1.4,1.6"),
                Token(TokenType.COMPILER_AND_VERSION, value="%intel@12.1"),
                Token(TokenType.BOOL_VARIANT, value="~qt_4"),
                Token(TokenType.KEY_VALUE_PAIR, value="debug=2"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="stackwalker"),
                Token(TokenType.VERSION, value="@8.1_1e"),
            ],
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1~qt_4 debug=2 ^stackwalker@8.1_1e",
        ),
        (
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1 cppflags=-O3 +debug~qt_4 "
            "^stackwalker@8.1_1e",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich_foo"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
                Token(TokenType.VERSION, value="@1.2:1.4,1.6"),
                Token(TokenType.COMPILER_AND_VERSION, value="%intel@12.1"),
                Token(TokenType.KEY_VALUE_PAIR, value="cppflags=-O3"),
                Token(TokenType.BOOL_VARIANT, value="+debug"),
                Token(TokenType.BOOL_VARIANT, value="~qt_4"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="stackwalker"),
                Token(TokenType.VERSION, value="@8.1_1e"),
            ],
            "mvapich_foo ^_openmpi@1.2:1.4,1.6%intel@12.1 cppflags=-O3 +debug~qt_4 "
            "^stackwalker@8.1_1e",
        ),
        # Specs containing YAML or JSON in the package name
        (
            "yaml-cpp@0.1.8%intel@12.1 ^boost@3.1.4",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="yaml-cpp"),
                Token(TokenType.VERSION, value="@0.1.8"),
                Token(TokenType.COMPILER_AND_VERSION, value="%intel@12.1"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="boost"),
                Token(TokenType.VERSION, value="@3.1.4"),
            ],
            "yaml-cpp@0.1.8%intel@12.1 ^boost@3.1.4",
        ),
        (
            r"builtin.yaml-cpp%gcc",
            [
                Token(TokenType.FULLY_QUALIFIED_PACKAGE_NAME, value="builtin.yaml-cpp"),
                Token(TokenType.COMPILER, value="%gcc"),
            ],
            "yaml-cpp%gcc",
        ),
        (
            r"testrepo.yaml-cpp%gcc",
            [
                Token(TokenType.FULLY_QUALIFIED_PACKAGE_NAME, value="testrepo.yaml-cpp"),
                Token(TokenType.COMPILER, value="%gcc"),
            ],
            "yaml-cpp%gcc",
        ),
        (
            r"builtin.yaml-cpp@0.1.8%gcc@7.2.0 ^boost@3.1.4",
            [
                Token(TokenType.FULLY_QUALIFIED_PACKAGE_NAME, value="builtin.yaml-cpp"),
                Token(TokenType.VERSION, value="@0.1.8"),
                Token(TokenType.COMPILER_AND_VERSION, value="%gcc@7.2.0"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="boost"),
                Token(TokenType.VERSION, value="@3.1.4"),
            ],
            "yaml-cpp@0.1.8%gcc@7.2.0 ^boost@3.1.4",
        ),
        (
            r"builtin.yaml-cpp ^testrepo.boost ^zlib",
            [
                Token(TokenType.FULLY_QUALIFIED_PACKAGE_NAME, value="builtin.yaml-cpp"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.FULLY_QUALIFIED_PACKAGE_NAME, value="testrepo.boost"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="zlib"),
            ],
            "yaml-cpp ^boost ^zlib",
        ),
        # Canonicalization of the string representation
        (
            r"mvapich ^stackwalker ^_openmpi",  # Dependencies are reordered
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="stackwalker"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
            ],
            "mvapich ^_openmpi ^stackwalker",
        ),
        (
            r"y~f+e~d+c~b+a",  # Variants are reordered
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.BOOL_VARIANT, value="~f"),
                Token(TokenType.BOOL_VARIANT, value="+e"),
                Token(TokenType.BOOL_VARIANT, value="~d"),
                Token(TokenType.BOOL_VARIANT, value="+c"),
                Token(TokenType.BOOL_VARIANT, value="~b"),
                Token(TokenType.BOOL_VARIANT, value="+a"),
            ],
            "y+a~b+c~d+e~f",
        ),
        ("@:", [Token(TokenType.VERSION, value="@:")], r""),
        ("@1.6,1.2:1.4", [Token(TokenType.VERSION, value="@1.6,1.2:1.4")], r"@1.2:1.4,1.6"),
        (
            r"os=fe",  # Various translations associated with the architecture
            [Token(TokenType.KEY_VALUE_PAIR, value="os=fe")],
            "arch=test-redhat6-None",
        ),
        (
            r"os=default_os",
            [Token(TokenType.KEY_VALUE_PAIR, value="os=default_os")],
            "arch=test-debian6-None",
        ),
        (
            r"target=be",
            [Token(TokenType.KEY_VALUE_PAIR, value="target=be")],
            f"arch=test-None-{spack.platforms.test.Test.default}",
        ),
        (
            r"target=default_target",
            [Token(TokenType.KEY_VALUE_PAIR, value="target=default_target")],
            f"arch=test-None-{spack.platforms.test.Test.default}",
        ),
        (
            r"platform=linux",
            [Token(TokenType.KEY_VALUE_PAIR, value="platform=linux")],
            r"arch=linux-None-None",
        ),
        # Version hash pair
        (
            rf"develop-branch-version@{'abc12'*8}=develop",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="develop-branch-version"),
                Token(TokenType.VERSION_HASH_PAIR, value=f"@{'abc12'*8}=develop"),
            ],
            rf"develop-branch-version@{'abc12'*8}=develop",
        ),
        # Redundant specs
        (
            r"x ^y@foo ^y@foo",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="x"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.VERSION, value="@foo"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.VERSION, value="@foo"),
            ],
            r"x ^y@foo",
        ),
        (
            r"x ^y@foo ^y+bar",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="x"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.VERSION, value="@foo"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.BOOL_VARIANT, value="+bar"),
            ],
            r"x ^y@foo+bar",
        ),
        (
            r"x ^y@foo +bar ^y@foo",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="x"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.VERSION, value="@foo"),
                Token(TokenType.BOOL_VARIANT, value="+bar"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="y"),
                Token(TokenType.VERSION, value="@foo"),
            ],
            r"x ^y@foo+bar",
        ),
        # Ambiguous variant specification
        (
            r"_openmpi +debug-qt_4",  # Parse as a single bool variant
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
                Token(TokenType.BOOL_VARIANT, value="+debug-qt_4"),
            ],
            r"_openmpi+debug-qt_4",
        ),
        (
            r"_openmpi +debug -qt_4",  # Parse as two variants
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
                Token(TokenType.BOOL_VARIANT, value="+debug"),
                Token(TokenType.BOOL_VARIANT, value="-qt_4"),
            ],
            r"_openmpi+debug~qt_4",
        ),
        (
            r"_openmpi +debug~qt_4",  # Parse as two variants
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="_openmpi"),
                Token(TokenType.BOOL_VARIANT, value="+debug"),
                Token(TokenType.BOOL_VARIANT, value="~qt_4"),
            ],
            r"_openmpi+debug~qt_4",
        ),
        # Key value pairs with ":" and "," in the value
        (
            r"target=:broadwell,icelake",
            [Token(TokenType.KEY_VALUE_PAIR, value="target=:broadwell,icelake")],
            r"arch=None-None-:broadwell,icelake",
        ),
        # Hash pair version followed by a variant
        (
            f"develop-branch-version@git.{'a' * 40}=develop+var1+var2",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="develop-branch-version"),
                Token(TokenType.VERSION_HASH_PAIR, value=f"@git.{'a' * 40}=develop"),
                Token(TokenType.BOOL_VARIANT, value="+var1"),
                Token(TokenType.BOOL_VARIANT, value="+var2"),
            ],
            f"develop-branch-version@git.{'a' * 40}=develop+var1+var2",
        ),
        # Compiler with version ranges
        compiler_with_version_range("%gcc@10.2.1:"),
        compiler_with_version_range("%gcc@:10.2.1"),
        compiler_with_version_range("%gcc@10.2.1:12.1.0"),
        compiler_with_version_range("%gcc@10.1.0,12.2.1:"),
        compiler_with_version_range("%gcc@:8.4.3,10.2.1:12.1.0"),
        # Special key value arguments
        ("dev_path=*", [Token(TokenType.KEY_VALUE_PAIR, value="dev_path=*")], "dev_path='*'"),
        (
            "dev_path=none",
            [Token(TokenType.KEY_VALUE_PAIR, value="dev_path=none")],
            "dev_path=none",
        ),
        (
            "dev_path=../relpath/work",
            [Token(TokenType.KEY_VALUE_PAIR, value="dev_path=../relpath/work")],
            "dev_path=../relpath/work",
        ),
        (
            "dev_path=/abspath/work",
            [Token(TokenType.KEY_VALUE_PAIR, value="dev_path=/abspath/work")],
            "dev_path=/abspath/work",
        ),
        # One liner for flags like 'a=b=c' that are injected
        (
            "cflags=a=b=c",
            [Token(TokenType.KEY_VALUE_PAIR, value="cflags=a=b=c")],
            "cflags='a=b=c'",
        ),
        (
            "cflags=a=b=c",
            [Token(TokenType.KEY_VALUE_PAIR, value="cflags=a=b=c")],
            "cflags='a=b=c'",
        ),
        (
            "cflags=a=b=c+~",
            [Token(TokenType.KEY_VALUE_PAIR, value="cflags=a=b=c+~")],
            "cflags='a=b=c+~'",
        ),
        (
            "cflags=-Wl,a,b,c",
            [Token(TokenType.KEY_VALUE_PAIR, value="cflags=-Wl,a,b,c")],
            "cflags=-Wl,a,b,c",
        ),
        # Multi quoted
        (
            'cflags=="-O3 -g"',
            [Token(TokenType.PROPAGATED_KEY_VALUE_PAIR, value='cflags=="-O3 -g"')],
            "cflags=='-O3 -g'",
        ),
        # Whitespace is allowed in version lists
        ("@1.2:1.4 , 1.6 ", [Token(TokenType.VERSION, value="@1.2:1.4 , 1.6")], "@1.2:1.4,1.6"),
        # But not in ranges. `a@1:` and `b` are separate specs, not a single `a@1:b`.
        (
            "a@1: b",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="a"),
                Token(TokenType.VERSION, value="@1:"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="b"),
            ],
            "a@1:",
        ),
        (
            "% intel @ 12.1:12.6 + debug",
            [
                Token(TokenType.COMPILER_AND_VERSION, value="% intel @ 12.1:12.6"),
                Token(TokenType.BOOL_VARIANT, value="+ debug"),
            ],
            "%intel@12.1:12.6+debug",
        ),
        (
            "@ 12.1:12.6 + debug - qt_4",
            [
                Token(TokenType.VERSION, value="@ 12.1:12.6"),
                Token(TokenType.BOOL_VARIANT, value="+ debug"),
                Token(TokenType.BOOL_VARIANT, value="- qt_4"),
            ],
            "@12.1:12.6+debug~qt_4",
        ),
        (
            "@10.4.0:10,11.3.0:target=aarch64:",
            [
                Token(TokenType.VERSION, value="@10.4.0:10,11.3.0:"),
                Token(TokenType.KEY_VALUE_PAIR, value="target=aarch64:"),
            ],
            "@10.4.0:10,11.3.0: arch=None-None-aarch64:",
        ),
        (
            "@:0.4 % nvhpc",
            [Token(TokenType.VERSION, value="@:0.4"), Token(TokenType.COMPILER, value="% nvhpc")],
            "@:0.4%nvhpc",
        ),
        (
            "^[virtuals=mpi] openmpi",
            [
                Token(TokenType.START_EDGE_PROPERTIES, value="^["),
                Token(TokenType.KEY_VALUE_PAIR, value="virtuals=mpi"),
                Token(TokenType.END_EDGE_PROPERTIES, value="]"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="openmpi"),
            ],
            "^[virtuals=mpi] openmpi",
        ),
        # Allow merging attributes, if deptypes match
        (
            "^[virtuals=mpi] openmpi+foo ^[virtuals=lapack] openmpi+bar",
            [
                Token(TokenType.START_EDGE_PROPERTIES, value="^["),
                Token(TokenType.KEY_VALUE_PAIR, value="virtuals=mpi"),
                Token(TokenType.END_EDGE_PROPERTIES, value="]"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="openmpi"),
                Token(TokenType.BOOL_VARIANT, value="+foo"),
                Token(TokenType.START_EDGE_PROPERTIES, value="^["),
                Token(TokenType.KEY_VALUE_PAIR, value="virtuals=lapack"),
                Token(TokenType.END_EDGE_PROPERTIES, value="]"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="openmpi"),
                Token(TokenType.BOOL_VARIANT, value="+bar"),
            ],
            "^[virtuals=lapack,mpi] openmpi+bar+foo",
        ),
        (
            "^[deptypes=link,build] zlib",
            [
                Token(TokenType.START_EDGE_PROPERTIES, value="^["),
                Token(TokenType.KEY_VALUE_PAIR, value="deptypes=link,build"),
                Token(TokenType.END_EDGE_PROPERTIES, value="]"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="zlib"),
            ],
            "^[deptypes=build,link] zlib",
        ),
        (
            "^[deptypes=link] zlib ^[deptypes=build] zlib",
            [
                Token(TokenType.START_EDGE_PROPERTIES, value="^["),
                Token(TokenType.KEY_VALUE_PAIR, value="deptypes=link"),
                Token(TokenType.END_EDGE_PROPERTIES, value="]"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="zlib"),
                Token(TokenType.START_EDGE_PROPERTIES, value="^["),
                Token(TokenType.KEY_VALUE_PAIR, value="deptypes=build"),
                Token(TokenType.END_EDGE_PROPERTIES, value="]"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="zlib"),
            ],
            "^[deptypes=link] zlib ^[deptypes=build] zlib",
        ),
        (
            "git-test@git.foo/bar",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, "git-test"),
                Token(TokenType.GIT_VERSION, "@git.foo/bar"),
            ],
            "git-test@git.foo/bar",
        ),
        # Variant propagation
        (
            "zlib ++foo",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, "zlib"),
                Token(TokenType.PROPAGATED_BOOL_VARIANT, "++foo"),
            ],
            "zlib++foo",
        ),
        (
            "zlib ~~foo",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, "zlib"),
                Token(TokenType.PROPAGATED_BOOL_VARIANT, "~~foo"),
            ],
            "zlib~~foo",
        ),
        (
            "zlib foo==bar",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, "zlib"),
                Token(TokenType.PROPAGATED_KEY_VALUE_PAIR, "foo==bar"),
            ],
            "zlib foo==bar",
        ),
    ],
)
def test_parse_single_spec(spec_str, tokens, expected_roundtrip, mock_git_test_package):
    parser = SpecParser(spec_str)
    assert tokens == parser.tokens()
    assert expected_roundtrip == str(parser.next_spec())


@pytest.mark.parametrize(
    "text,tokens,expected_specs",
    [
        (
            "mvapich emacs",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="emacs"),
            ],
            ["mvapich", "emacs"],
        ),
        (
            "mvapich cppflags='-O3 -fPIC' emacs",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich"),
                Token(TokenType.KEY_VALUE_PAIR, value="cppflags='-O3 -fPIC'"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="emacs"),
            ],
            ["mvapich cppflags='-O3 -fPIC'", "emacs"],
        ),
        (
            "mvapich cppflags=-O3 emacs",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich"),
                Token(TokenType.KEY_VALUE_PAIR, value="cppflags=-O3"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="emacs"),
            ],
            ["mvapich cppflags=-O3", "emacs"],
        ),
        (
            "mvapich emacs @1.1.1 %intel cflags=-O3",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="emacs"),
                Token(TokenType.VERSION, value="@1.1.1"),
                Token(TokenType.COMPILER, value="%intel"),
                Token(TokenType.KEY_VALUE_PAIR, value="cflags=-O3"),
            ],
            ["mvapich", "emacs @1.1.1 %intel cflags=-O3"],
        ),
        (
            'mvapich cflags="-O3 -fPIC" emacs^ncurses%intel',
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="mvapich"),
                Token(TokenType.KEY_VALUE_PAIR, value='cflags="-O3 -fPIC"'),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="emacs"),
                Token(TokenType.DEPENDENCY, value="^"),
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="ncurses"),
                Token(TokenType.COMPILER, value="%intel"),
            ],
            ['mvapich cflags="-O3 -fPIC"', "emacs ^ncurses%intel"],
        ),
    ],
)
def test_parse_multiple_specs(text, tokens, expected_specs):
    total_parser = SpecParser(text)
    assert total_parser.tokens() == tokens

    for single_spec_text in expected_specs:
        single_spec_parser = SpecParser(single_spec_text)
        assert str(total_parser.next_spec()) == str(single_spec_parser.next_spec())


@pytest.mark.parametrize(
    "args,expected",
    [
        # Test that CLI-quoted flags/variant values are preserved
        (["zlib", "cflags=-O3 -g", "+bar", "baz"], "zlib cflags='-O3 -g' +bar baz"),
        # Test that CLI-quoted propagated flags/variant values are preserved
        (["zlib", "cflags==-O3 -g", "+bar", "baz"], "zlib cflags=='-O3 -g' +bar baz"),
        # An entire string passed on the CLI with embedded quotes also works
        (["zlib cflags='-O3 -g' +bar baz"], "zlib cflags='-O3 -g' +bar baz"),
        # Entire string *without* quoted flags splits -O3/-g (-g interpreted as a variant)
        (["zlib cflags=-O3 -g +bar baz"], "zlib cflags=-O3 +bar~g baz"),
        # If the entirety of "-O3 -g +bar baz" is quoted on the CLI, it's all taken as flags
        (["zlib", "cflags=-O3 -g +bar baz"], "zlib cflags='-O3 -g +bar baz'"),
        # If the string doesn't start with key=, it needs internal quotes for flags
        (["zlib", " cflags=-O3 -g +bar baz"], "zlib cflags=-O3 +bar~g baz"),
        # Internal quotes for quoted CLI args are considered part of *one* arg
        (["zlib", 'cflags="-O3 -g" +bar baz'], """zlib cflags='"-O3 -g" +bar baz'"""),
        # Use double quotes if internal single quotes are present
        (["zlib", "cflags='-O3 -g' +bar baz"], '''zlib cflags="'-O3 -g' +bar baz"'''),
        # Use single quotes and escape single quotes with internal single and double quotes
        (["zlib", "cflags='-O3 -g' \"+bar baz\""], 'zlib cflags="\'-O3 -g\' \\"+bar baz\\""'),
        # Ensure that empty strings are handled correctly on CLI
        (["zlib", "ldflags=", "+pic"], "zlib+pic"),
        # These flags are assumed to be quoted by the shell, but the space doesn't matter because
        # flags are space-separated.
        (["zlib", "ldflags= +pic"], "zlib ldflags='+pic'"),
        (["ldflags= +pic"], "ldflags='+pic'"),
        # If the name is not a flag name, the space is preserved verbatim, because variant values
        # are comma-separated.
        (["zlib", "foo= +pic"], "zlib foo=' +pic'"),
        (["foo= +pic"], "foo=' +pic'"),
        # You can ensure no quotes are added parse_specs() by starting your string with space,
        # but you still need to quote empty strings properly.
        ([" ldflags= +pic"], SpecTokenizationError),
        ([" ldflags=", "+pic"], SpecTokenizationError),
        ([" ldflags='' +pic"], "+pic"),
        ([" ldflags=''", "+pic"], "+pic"),
        # Ensure that empty strings are handled properly in quoted strings
        (["zlib ldflags='' +pic"], "zlib+pic"),
        # Ensure that $ORIGIN is handled correctly
        (["zlib", "ldflags=-Wl,-rpath=$ORIGIN/_libs"], "zlib ldflags='-Wl,-rpath=$ORIGIN/_libs'"),
        # Ensure that passing escaped quotes on the CLI raises a tokenization error
        (["zlib", '"-g', '-O2"'], SpecTokenizationError),
    ],
)
def test_cli_spec_roundtrip(args, expected):
    if isinstance(expected, type) and issubclass(expected, BaseException):
        with pytest.raises(expected):
            spack.cmd.parse_specs(args)
        return

    specs = spack.cmd.parse_specs(args)
    output_string = " ".join(str(spec) for spec in specs)
    assert expected == output_string


@pytest.mark.parametrize(
    "text,expected_in_error",
    [
        ("x@@1.2", r"x@@1.2\n ^"),
        ("y ^x@@1.2", r"y ^x@@1.2\n    ^"),
        ("x@1.2::", r"x@1.2::\n      ^"),
        ("x::", r"x::\n ^^"),
        ("cflags=''-Wl,a,b,c''", r"cflags=''-Wl,a,b,c''\n            ^ ^ ^ ^^"),
        ("@1.2:   develop   = foo", r"@1.2:   develop   = foo\n                  ^^"),
        ("@1.2:develop   = foo", r"@1.2:develop   = foo\n               ^^"),
    ],
)
def test_error_reporting(text, expected_in_error):
    parser = SpecParser(text)
    with pytest.raises(SpecTokenizationError) as exc:
        parser.tokens()

    assert expected_in_error in str(exc), parser.tokens()


@pytest.mark.parametrize(
    "text,tokens",
    [
        ("/abcde", [Token(TokenType.DAG_HASH, value="/abcde")]),
        (
            "foo/abcde",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="foo"),
                Token(TokenType.DAG_HASH, value="/abcde"),
            ],
        ),
        (
            "foo@1.2.3 /abcde",
            [
                Token(TokenType.UNQUALIFIED_PACKAGE_NAME, value="foo"),
                Token(TokenType.VERSION, value="@1.2.3"),
                Token(TokenType.DAG_HASH, value="/abcde"),
            ],
        ),
    ],
)
def test_spec_by_hash_tokens(text, tokens):
    parser = SpecParser(text)
    assert parser.tokens() == tokens


@pytest.mark.db
def test_spec_by_hash(database, monkeypatch, config):
    mpileaks = database.query_one("mpileaks ^zmpi")
    b = spack.spec.Spec("pkg-b").concretized()
    monkeypatch.setattr(spack.binary_distribution, "update_cache_and_get_specs", lambda: [b])

    hash_str = f"/{mpileaks.dag_hash()}"
    parsed_spec = SpecParser(hash_str).next_spec()
    parsed_spec.replace_hash()
    assert parsed_spec == mpileaks

    short_hash_str = f"/{mpileaks.dag_hash()[:5]}"
    parsed_spec = SpecParser(short_hash_str).next_spec()
    parsed_spec.replace_hash()
    assert parsed_spec == mpileaks

    name_version_and_hash = f"{mpileaks.name}@{mpileaks.version} /{mpileaks.dag_hash()[:5]}"
    parsed_spec = SpecParser(name_version_and_hash).next_spec()
    parsed_spec.replace_hash()
    assert parsed_spec == mpileaks

    b_hash = f"/{b.dag_hash()}"
    parsed_spec = SpecParser(b_hash).next_spec()
    parsed_spec.replace_hash()
    assert parsed_spec == b


@pytest.mark.db
def test_dep_spec_by_hash(database, config):
    mpileaks_zmpi = database.query_one("mpileaks ^zmpi")
    zmpi = database.query_one("zmpi")
    fake = database.query_one("fake")

    assert "fake" in mpileaks_zmpi
    assert "zmpi" in mpileaks_zmpi

    mpileaks_hash_fake = SpecParser(f"mpileaks ^/{fake.dag_hash()} ^zmpi").next_spec()
    mpileaks_hash_fake.replace_hash()
    assert "fake" in mpileaks_hash_fake
    assert mpileaks_hash_fake["fake"] == fake
    assert "zmpi" in mpileaks_hash_fake
    assert mpileaks_hash_fake["zmpi"] == spack.spec.Spec("zmpi")

    mpileaks_hash_zmpi = SpecParser(
        f"mpileaks %{mpileaks_zmpi.compiler} ^ /{zmpi.dag_hash()}"
    ).next_spec()
    mpileaks_hash_zmpi.replace_hash()
    assert "zmpi" in mpileaks_hash_zmpi
    assert mpileaks_hash_zmpi["zmpi"] == zmpi
    assert mpileaks_zmpi.compiler.satisfies(mpileaks_hash_zmpi.compiler)

    mpileaks_hash_fake_and_zmpi = SpecParser(
        f"mpileaks ^/{fake.dag_hash()[:4]} ^ /{zmpi.dag_hash()[:5]}"
    ).next_spec()
    mpileaks_hash_fake_and_zmpi.replace_hash()
    assert "zmpi" in mpileaks_hash_fake_and_zmpi
    assert mpileaks_hash_fake_and_zmpi["zmpi"] == zmpi

    assert "fake" in mpileaks_hash_fake_and_zmpi
    assert mpileaks_hash_fake_and_zmpi["fake"] == fake


@pytest.mark.db
def test_multiple_specs_with_hash(database, config):
    mpileaks_zmpi = database.query_one("mpileaks ^zmpi")
    callpath_mpich2 = database.query_one("callpath ^mpich2")

    # name + hash + separate hash
    specs = SpecParser(
        f"mpileaks /{mpileaks_zmpi.dag_hash()} /{callpath_mpich2.dag_hash()}"
    ).all_specs()
    assert len(specs) == 2

    # 2 separate hashes
    specs = SpecParser(f"/{mpileaks_zmpi.dag_hash()} /{callpath_mpich2.dag_hash()}").all_specs()
    assert len(specs) == 2

    # 2 separate hashes + name
    specs = SpecParser(
        f"/{mpileaks_zmpi.dag_hash()} /{callpath_mpich2.dag_hash()} callpath"
    ).all_specs()
    assert len(specs) == 3

    # hash + 2 names
    specs = SpecParser(f"/{mpileaks_zmpi.dag_hash()} callpath callpath").all_specs()
    assert len(specs) == 3

    # hash + name + hash
    specs = SpecParser(
        f"/{mpileaks_zmpi.dag_hash()} callpath /{callpath_mpich2.dag_hash()}"
    ).all_specs()
    assert len(specs) == 2


@pytest.mark.db
def test_ambiguous_hash(mutable_database):
    """Test that abstract hash ambiguity is delayed until concretization.
    In the past this ambiguity error would happen during parse time."""

    # This is a very sketchy as manually setting hashes easily breaks invariants
    x1 = spack.spec.Spec("pkg-a").concretized()
    x2 = x1.copy()
    x1._hash = "xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    x1._process_hash = "xyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    x2._hash = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    x2._process_hash = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    assert x1 != x2  # doesn't hold when only the dag hash is modified.

    mutable_database.add(x1)
    mutable_database.add(x2)

    # ambiguity in first hash character
    s1 = SpecParser("/x").next_spec()
    with pytest.raises(spack.spec.AmbiguousHashError):
        s1.lookup_hash()

    # ambiguity in first hash character AND spec name
    s2 = SpecParser("pkg-a/x").next_spec()
    with pytest.raises(spack.spec.AmbiguousHashError):
        s2.lookup_hash()


@pytest.mark.db
def test_invalid_hash(database, config):
    zmpi = database.query_one("zmpi")
    mpich = database.query_one("mpich")

    # name + incompatible hash
    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"zmpi /{mpich.dag_hash()}").next_spec()
        parsed_spec.replace_hash()
    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"mpich /{zmpi.dag_hash()}").next_spec()
        parsed_spec.replace_hash()

    # name + dep + incompatible hash
    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"mpileaks ^zmpi /{mpich.dag_hash()}").next_spec()
        parsed_spec.replace_hash()


def test_invalid_hash_dep(database, config):
    mpich = database.query_one("mpich")
    hash = mpich.dag_hash()
    with pytest.raises(spack.spec.InvalidHashError):
        spack.spec.Spec(f"callpath ^zlib/{hash}").replace_hash()


@pytest.mark.db
def test_nonexistent_hash(database, config):
    """Ensure we get errors for non existent hashes."""
    specs = database.query()

    # This hash shouldn't be in the test DB.  What are the odds :)
    no_such_hash = "aaaaaaaaaaaaaaa"
    hashes = [s._hash for s in specs]
    assert no_such_hash not in [h[: len(no_such_hash)] for h in hashes]

    with pytest.raises(spack.spec.InvalidHashError):
        parsed_spec = SpecParser(f"/{no_such_hash}").next_spec()
        parsed_spec.replace_hash()


@pytest.mark.parametrize(
    "spec1,spec2,constraint",
    [
        ("zlib", "hdf5", None),
        ("zlib+shared", "zlib~shared", "+shared"),
        ("hdf5+mpi^zmpi", "hdf5~mpi", "^zmpi"),
        ("hdf5+mpi^mpich+debug", "hdf5+mpi^mpich~debug", "^mpich+debug"),
    ],
)
def test_disambiguate_hash_by_spec(spec1, spec2, constraint, mock_packages, monkeypatch, config):
    spec1_concrete = spack.spec.Spec(spec1).concretized()
    spec2_concrete = spack.spec.Spec(spec2).concretized()

    spec1_concrete._hash = "spec1"
    spec2_concrete._hash = "spec2"

    monkeypatch.setattr(
        spack.binary_distribution,
        "update_cache_and_get_specs",
        lambda: [spec1_concrete, spec2_concrete],
    )

    # Ordering is tricky -- for constraints we want after, for names we want before
    if not constraint:
        spec = spack.spec.Spec(spec1 + "/spec")
    else:
        spec = spack.spec.Spec("/spec" + constraint)

    assert spec.lookup_hash() == spec1_concrete


@pytest.mark.parametrize(
    "text,match_string",
    [
        # Duplicate variants
        ("x@1.2+debug+debug", "variant"),
        ("x ^y@1.2+debug debug=true", "variant"),
        ("x ^y@1.2 debug=false debug=true", "variant"),
        ("x ^y@1.2 debug=false ~debug", "variant"),
        # Multiple versions
        ("x@1.2@2.3", "version"),
        ("x@1.2:2.3@1.4", "version"),
        ("x@1.2@2.3:2.4", "version"),
        ("x@1.2@2.3,2.4", "version"),
        ("x@1.2 +foo~bar @2.3", "version"),
        ("x@1.2%y@1.2@2.3:2.4", "version"),
        # Duplicate dependency
        ("x ^y@1 ^y@2", "Cannot depend on incompatible specs"),
        # Duplicate compiler
        ("x%intel%intel", "compiler"),
        ("x%intel%gcc", "compiler"),
        ("x%gcc%intel", "compiler"),
        ("x ^y%intel%intel", "compiler"),
        ("x ^y%intel%gcc", "compiler"),
        ("x ^y%gcc%intel", "compiler"),
        # Duplicate Architectures
        ("x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64", "two architectures"),
        ("x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le", "two architectures"),
        ("x arch=linux-rhel7-ppc64le arch=linux-rhel7-x86_64", "two architectures"),
        ("y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-x86_64", "two architectures"),
        ("y ^x arch=linux-rhel7-x86_64 arch=linux-rhel7-ppc64le", "two architectures"),
        ("x os=fe os=fe", "'os'"),
        ("x os=fe os=be", "'os'"),
        ("x target=fe target=fe", "'target'"),
        ("x target=fe target=be", "'target'"),
        ("x platform=test platform=test", "'platform'"),
        # TODO: these two seem wrong: need to change how arch is initialized (should fail on os)
        ("x os=fe platform=test target=fe os=fe", "'platform'"),
        ("x target=be platform=test os=be os=fe", "'platform'"),
        # Dependencies
        ("^[@foo] zlib", "edge attributes"),
        ("x ^[deptypes=link]foo ^[deptypes=run]foo", "conflicting dependency types"),
        ("x ^[deptypes=build,link]foo ^[deptypes=link]foo", "conflicting dependency types"),
        # TODO: Remove this as soon as use variants are added and we can parse custom attributes
        ("^[foo=bar] zlib", "edge attributes"),
        # Propagating reserved names generates a parse error
        ("x namespace==foo.bar.baz", "Propagation"),
        ("x arch==linux-rhel9-x86_64", "Propagation"),
        ("x architecture==linux-rhel9-x86_64", "Propagation"),
        ("x os==rhel9", "Propagation"),
        ("x operating_system==rhel9", "Propagation"),
        ("x target==x86_64", "Propagation"),
        ("x dev_path==/foo/bar/baz", "Propagation"),
        ("x patches==abcde12345,12345abcde", "Propagation"),
    ],
)
def test_error_conditions(text, match_string):
    with pytest.raises(spack.parser.SpecParsingError, match=match_string):
        SpecParser(text).next_spec()


@pytest.mark.parametrize(
    "text,exc_cls",
    [
        # Specfile related errors
        pytest.param(
            "/bogus/path/libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_WINDOWS
        ),
        pytest.param("../../libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_WINDOWS),
        pytest.param("./libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_WINDOWS),
        pytest.param(
            "libfoo ^/bogus/path/libdwarf.yaml",
            spack.spec.NoSuchSpecFileError,
            marks=FAIL_ON_WINDOWS,
        ),
        pytest.param(
            "libfoo ^../../libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_WINDOWS
        ),
        pytest.param(
            "libfoo ^./libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_WINDOWS
        ),
        pytest.param(
            "/bogus/path/libdwarf.yamlfoobar",
            spack.spec.NoSuchSpecFileError,
            marks=FAIL_ON_WINDOWS,
        ),
        pytest.param(
            "libdwarf^/bogus/path/libelf.yamlfoobar ^/path/to/bogus.yaml",
            spack.spec.NoSuchSpecFileError,
            marks=FAIL_ON_WINDOWS,
        ),
        pytest.param(
            "c:\\bogus\\path\\libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_UNIX
        ),
        pytest.param("..\\..\\libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_UNIX),
        pytest.param(".\\libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_UNIX),
        pytest.param(
            "libfoo ^c:\\bogus\\path\\libdwarf.yaml",
            spack.spec.NoSuchSpecFileError,
            marks=FAIL_ON_UNIX,
        ),
        pytest.param(
            "libfoo ^..\\..\\libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_UNIX
        ),
        pytest.param(
            "libfoo ^.\\libdwarf.yaml", spack.spec.NoSuchSpecFileError, marks=FAIL_ON_UNIX
        ),
        pytest.param(
            "c:\\bogus\\path\\libdwarf.yamlfoobar",
            spack.spec.SpecFilenameError,
            marks=FAIL_ON_UNIX,
        ),
        pytest.param(
            "libdwarf^c:\\bogus\\path\\libelf.yamlfoobar ^c:\\path\\to\\bogus.yaml",
            spack.spec.SpecFilenameError,
            marks=FAIL_ON_UNIX,
        ),
    ],
)
def test_specfile_error_conditions_windows(text, exc_cls):
    with pytest.raises(exc_cls):
        SpecParser(text).all_specs()


@pytest.mark.parametrize(
    "filename,regex",
    [
        (r"c:\abs\windows\\path.yaml", WINDOWS_FILENAME),
        (r".\\relative\\dot\\win\\path.yaml", WINDOWS_FILENAME),
        (r"relative\\windows\\path.yaml", WINDOWS_FILENAME),
        ("/absolute/path/to/file.yaml", UNIX_FILENAME),
        ("relative/path/to/file.yaml", UNIX_FILENAME),
        ("./dot/rel/to/file.yaml", UNIX_FILENAME),
    ],
)
def test_specfile_parsing(filename, regex):
    match = re.match(regex, filename)
    assert match
    assert match.end() == len(filename)


def test_parse_specfile_simple(specfile_for, tmpdir):
    specfile = tmpdir.join("libdwarf.json")
    s = specfile_for("libdwarf", specfile)

    spec = SpecParser(specfile.strpath).next_spec()
    assert spec == s

    # Check we can mix literal and spec-file in text
    specs = SpecParser(f"mvapich_foo {specfile.strpath}").all_specs()
    assert len(specs) == 2


@pytest.mark.parametrize("filename", ["libelf.yaml", "libelf.json"])
def test_parse_filename_missing_slash_as_spec(specfile_for, tmpdir, filename):
    """Ensure that libelf(.yaml|.json) parses as a spec, NOT a file."""
    specfile = tmpdir.join(filename)
    specfile_for(filename.split(".")[0], specfile)

    # Move to where the specfile is located so that libelf.yaml is there
    with tmpdir.as_cwd():
        specs = SpecParser("libelf.yaml").all_specs()
    assert len(specs) == 1

    spec = specs[0]
    assert spec.name == "yaml"
    assert spec.namespace == "libelf"
    assert spec.fullname == "libelf.yaml"

    # Check that if we concretize this spec, we get a good error
    # message that mentions we might've meant a file.
    with pytest.raises(spack.repo.UnknownEntityError) as exc_info:
        spec.concretize()
    assert exc_info.value.long_message
    assert (
        "Did you mean to specify a filename with './libelf.yaml'?" in exc_info.value.long_message
    )

    # make sure that only happens when the spec ends in yaml
    with pytest.raises(spack.repo.UnknownPackageError) as exc_info:
        SpecParser("builtin.mock.doesnotexist").next_spec().concretize()
    assert not exc_info.value.long_message or (
        "Did you mean to specify a filename with" not in exc_info.value.long_message
    )


def test_parse_specfile_dependency(default_mock_concretization, tmpdir):
    """Ensure we can use a specfile as a dependency"""
    s = default_mock_concretization("libdwarf")

    specfile = tmpdir.join("libelf.json")
    with specfile.open("w") as f:
        f.write(s["libelf"].to_json())

    # Make sure we can use yaml path as dependency, e.g.:
    #     "spack spec libdwarf ^ /path/to/libelf.json"
    spec = SpecParser(f"libdwarf ^ {specfile.strpath}").next_spec()
    assert spec["libelf"] == s["libelf"]

    with specfile.dirpath().as_cwd():
        # Make sure this also works: "spack spec ./libelf.yaml"
        spec = SpecParser(f"libdwarf^.{os.path.sep}{specfile.basename}").next_spec()
        assert spec["libelf"] == s["libelf"]

        # Should also be accepted: "spack spec ../<cur-dir>/libelf.yaml"
        spec = SpecParser(
            f"libdwarf^..{os.path.sep}{specfile.dirpath().basename}\
{os.path.sep}{specfile.basename}"
        ).next_spec()
        assert spec["libelf"] == s["libelf"]


def test_parse_specfile_relative_paths(specfile_for, tmpdir):
    specfile = tmpdir.join("libdwarf.json")
    s = specfile_for("libdwarf", specfile)

    basename = specfile.basename
    parent_dir = specfile.dirpath()

    with parent_dir.as_cwd():
        # Make sure this also works: "spack spec ./libelf.yaml"
        spec = SpecParser(f".{os.path.sep}{basename}").next_spec()
        assert spec == s

        # Should also be accepted: "spack spec ../<cur-dir>/libelf.yaml"
        spec = SpecParser(
            f"..{os.path.sep}{parent_dir.basename}{os.path.sep}{basename}"
        ).next_spec()
        assert spec == s

        # Should also handle mixed clispecs and relative paths, e.g.:
        #     "spack spec mvapich_foo ../<cur-dir>/libelf.yaml"
        specs = SpecParser(
            f"mvapich_foo ..{os.path.sep}{parent_dir.basename}{os.path.sep}{basename}"
        ).all_specs()
        assert len(specs) == 2
        assert specs[1] == s


def test_parse_specfile_relative_subdir_path(specfile_for, tmpdir):
    specfile = tmpdir.mkdir("subdir").join("libdwarf.json")
    s = specfile_for("libdwarf", specfile)

    with tmpdir.as_cwd():
        spec = SpecParser(f"subdir{os.path.sep}{specfile.basename}").next_spec()
        assert spec == s


@pytest.mark.regression("20310")
def test_compare_abstract_specs():
    """Spec comparisons must be valid for abstract specs.

    Check that the spec cmp_key appropriately handles comparing specs for
    which some attributes are None in exactly one of two specs
    """
    # Add fields in order they appear in `Spec._cmp_node`
    constraints = [
        "foo",
        "foo.foo",
        "foo.foo@foo",
        "foo.foo@foo+foo",
        "foo.foo@foo+foo arch=foo-foo-foo",
        "foo.foo@foo+foo arch=foo-foo-foo %foo",
        "foo.foo@foo+foo arch=foo-foo-foo %foo cflags=foo",
    ]
    specs = [SpecParser(s).next_spec() for s in constraints]

    for a, b in itertools.product(specs, repeat=2):
        # Check that we can compare without raising an error
        assert a <= b or b < a


@pytest.mark.parametrize(
    "lhs_str,rhs_str,expected",
    [
        # Git shasum vs generic develop
        (
            f"develop-branch-version@git.{'a' * 40}=develop",
            "develop-branch-version@develop",
            (True, True, False),
        ),
        # Two different shasums
        (
            f"develop-branch-version@git.{'a' * 40}=develop",
            f"develop-branch-version@git.{'b' * 40}=develop",
            (False, False, False),
        ),
        # Git shasum vs. git tag
        (
            f"develop-branch-version@git.{'a' * 40}=develop",
            "develop-branch-version@git.0.2.15=develop",
            (False, False, False),
        ),
        # Git tag vs. generic develop
        (
            "develop-branch-version@git.0.2.15=develop",
            "develop-branch-version@develop",
            (True, True, False),
        ),
    ],
)
def test_git_ref_spec_equivalences(mock_packages, lhs_str, rhs_str, expected):
    lhs = SpecParser(lhs_str).next_spec()
    rhs = SpecParser(rhs_str).next_spec()
    intersect, lhs_sat_rhs, rhs_sat_lhs = expected

    assert lhs.intersects(rhs) is intersect
    assert rhs.intersects(lhs) is intersect
    assert lhs.satisfies(rhs) is lhs_sat_rhs
    assert rhs.satisfies(lhs) is rhs_sat_lhs


@pytest.mark.regression("32471")
@pytest.mark.parametrize("spec_str", ["target=x86_64", "os=redhat6", "target=x86_64:"])
def test_platform_is_none_if_not_present(spec_str):
    s = SpecParser(spec_str).next_spec()
    assert s.architecture.platform is None, s
