# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.config
import spack.repo
import spack.util.spack_yaml as syaml
from spack.main import SpackCommand
from spack.spec import Spec
from spack.test.conftest import create_test_repo

solve = SpackCommand("solve")


def update_packages_config(conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set("packages", conf["packages"], scope="concretize")


_pkgx1 = (
    "x1",
    """\
class X1(Package):
    version("1.2")
    version("1.1")

    depends_on("x2")
    depends_on("x3")
""",
)


_pkgx2 = (
    "x2",
    """\
class X2(Package):
    version("2.1")
    version("2.0")

    depends_on("x4@4.1")
""",
)


_pkgx3 = (
    "x3",
    """\
class X3(Package):
    version("3.5")
    version("3.4")

    depends_on("x4@4.0")
""",
)


_pkgx4 = (
    "x4",
    """\
class X4(Package):
    version("4.1")
    version("4.0")
""",
)


_pkgy1 = (
    "y1",
    """\
class Y1(Package):
    version("1.2")
    version("1.1")

    depends_on("y2+v1")
    depends_on("y3")
""",
)


_pkgy2 = (
    "y2",
    """\
class Y2(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    depends_on("y4@4.1", when="+v1")
    depends_on("y4")
""",
)


_pkgy3 = (
    "y3",
    """\
class Y3(Package):
    version("3.5")
    version("3.4")

    depends_on("y4@4.0")
""",
)


_pkgy4 = (
    "y4",
    """\
class Y4(Package):
    version("4.1")
    version("4.0")
""",
)


_pkgz1 = (
    "z1",
    """\
class Z1(Package):
    version("1.2")
    version("1.1")

    variant("v1", default=True)

    depends_on("z2")

    depends_on("z3")
    depends_on("z3+v2", when="~v1")

    conflicts("+v1", when="@:1.1")
""",
)


_pkgz2 = (
    "z2",
    """\
class Z2(Package):
    version("3.1")
    version("3.0")

    depends_on("z3@:2.0")
""",
)


_pkgz3 = (
    "z3",
    """\
class Z3(Package):
    version("2.1")
    version("2.0")

    variant("v2", default=True, when="@2.1:")
""",
)


# Cluster of packages that includes requirements - goal is to "chain"
# the requirements like other constraints.
_pkgw4 = (
    "w4",
    """\
class W4(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    depends_on("w2")
    depends_on("w2@:2.0", when="@:2.0")

    # test_errmsg_requirements stresses these constraints and generates
    # a good error message: "w4@:2.0 ^w3@2.1"
    depends_on("w3")
    depends_on("w3~v1", when="@2.0")
""",
)


_pkgw3 = (
    "w3",
    """\
class W3(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    requires("+v1", when="@2.1")

    depends_on("w1")
""",
)


_pkgw2 = (
    "w2",
    """\
class W2(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    requires("~v1", when="@:2.0")

    depends_on("w1")
""",
)


_pkgw1 = (
    "w1",
    """\
class W1(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)
""",
)


# Like the W* packages, but encodes the config requirements constraints
# into the packages to see if that improves the error from
# test_errmsg_requirements_cfg
_pkgt4 = (
    "t4",
    """\
class T4(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    # test_errmsg_requirements_2 stresses these constraints and
    # generates a bad error message: "t4@:2.0 ^t2+v1"
    depends_on("t2")
    depends_on("t2@:2.0", when="@:2.0")

    depends_on("t3")
    depends_on("t3~v1", when="@2.0")
""",
)


_pkgt3 = (
    "t3",
    """\
class T3(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    requires("+v1", when="@2.1")

    depends_on("t1")
""",
)


_pkgt2 = (
    "t2",
    """\
class T2(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)

    # requires("~v1", when="@:2.0")
    conflicts("+v1", when="@:2.0")

    depends_on("t1")
""",
)


_pkgt1 = (
    "t1",
    """\
class T1(Package):
    version("2.1")
    version("2.0")

    variant("v1", default=True)
""",
)


all_pkgs = [
    _pkgx1,
    _pkgx2,
    _pkgx3,
    _pkgx4,
    _pkgy1,
    _pkgy2,
    _pkgy3,
    _pkgy4,
    _pkgz1,
    _pkgz2,
    _pkgz3,
    _pkgw1,
    _pkgw2,
    _pkgw3,
    _pkgw4,
    _pkgt1,
    _pkgt2,
    _pkgt3,
    _pkgt4,
]


def _add_import(pkg_def):
    return "from spack.package import *\n" + pkg_def


all_pkgs = list((x, _add_import(y)) for (x, y) in all_pkgs)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(tmpdir, all_pkgs)


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


# Error message is good
def test_diamond_with_pkg_conflict1(concretize_scope, test_repo):
    Spec("x2").concretized()
    Spec("x3").concretized()
    Spec("x4").concretized()

    Spec("x1").concretized()


# Error message is good (has some redundancy though)
def test_diamond_with_pkg_conflict2(concretize_scope, test_repo):
    Spec("y1").concretized()


# This error message is not so great
def test_version_range_null(concretize_scope, test_repo):
    Spec("x2@3:4").concretized()


# This error message is hard to follow: neither z2 or z3
# are mentioned, so if this hierarchy had 10 other "OK"
# packages, a user would be conducting a tedious manual
# search
def test_null_variant_for_requested_version(concretize_scope, test_repo):
    Spec("z1").concretized()
    # output = solve("--show=asp", "z1@1.1")
    # with open(, "w") as f:
    #    f.write(output)
    Spec("z1@1.1").concretized()


# Error message for requirement introduced in the package
# definition seems OK: requirements generate `condition`s, which
# should be traceable as condition causes in error_messages.lp
def test_errmsg_requirements_1(concretize_scope, test_repo):
    # output = solve("--show=asp", "w4@:2.0 ^w3@2.1")
    # with open("/Users/scheibel1/Desktop/spack/spack/err-msg-asp/good-w.txt", "w") as f:
    #    f.write(output)

    Spec("w4@:2.0 ^w3@2.1").concretized()


# This error message is short. Would it be good if I encoded
# it in the package.py?
def test_errmsg_requirements_cfg(concretize_scope, test_repo):
    conf_str = """\
packages:
  w2:
    require:
    - spec: "~v1"
      when: "@2.0"
"""
    len(conf_str)
    # update_packages_config(conf_str)

    # Spec("w4@2.0").concretized()

    # output = solve("--show=asp", "w4@2.0 ^w2+v1")
    # with open("/Users/scheibel1/Desktop/spack/spack/err-msg-asp/bad-w.txt", "w") as f:
    #    f.write(output)

    Spec("w4@2.0 ^w2+v1").concretized()


# Short error message: this reencodes test_errmsg_requirements_cfg
# in terms of package `requires`, and demonstrates that the message
# is still lacking in detail
# (Jan. 9th update) something has changed so that this now generates
# a good error message, this was not true for 14cb20e from Oct. 15th
# 2024
# The error message is only good when the constraint is encoded as a
# conflict and not as a requirement
def test_errmsg_requirements_2(concretize_scope, test_repo):
    Spec("t4@:2.0 ^t2+v1").concretized()
