# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.build_systems.generic
import spack.config
import spack.error
import spack.package_base
import spack.repo
import spack.util.spack_yaml as syaml
import spack.version
from spack.main import SpackCommand
from spack.spec import Spec
from spack.test.conftest import create_test_repo

solve = SpackCommand("solve")


def update_cfg_section(section, conf_str):
    conf = syaml.load_config(conf_str)
    spack.config.set(section, conf[section], scope="concretize")


_pkgx1 = (
    "x1",
    """\
from spack.package import *

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
from spack.package import *    

class X2(Package):
    version("2.1")
    version("2.0")
    depends_on("x4")
""",
)


_pkgx3 = (
    "x3",
    """\
from spack.package import *

class X3(Package):
    version("3.5")
    version("3.4")
    depends_on("x4")
""",
)


_pkgx4 = (
    "x4",
    """\
from spack.package import *    

class X4(Package):
    version("4.1")
    version("4.0")
""",
)


@pytest.fixture
def _create_test_repo(tmpdir, mutable_config):
    yield create_test_repo(
        tmpdir,
        [
            _pkgx1,
            _pkgx2,
            _pkgx3,
            _pkgx4,
        ],
    )


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


def test_diamond(concretize_scope, test_repo):
    Spec("x1").concretized()


install = SpackCommand("install")
solve = SpackCommand("solve")


def test_with_cfg(mutable_mock_env_path, install_mockery, mock_fetch, concretize_scope, test_repo):
    test_cfg = """\
compilers::
- compiler:
    spec: gcc@11.0.0
    paths:
      cc: /usr/bin/gcc
      cxx: /usr/bin/g++
      f77: /usr/bin/gfortran
      fc: /usr/bin/gfortran
    flags: {}
    operating_system: debian6
    target: aarch64
    modules: []
    environment: {}
    extra_rpaths: []
- compiler:
    spec: aocc@5.0.0
    paths:
      cc: /usr/bin/clang
      cxx: /usr/bin/clang++
      f77: /usr/bin/flang
      fc: /usr/bin/flang
    flags: {}
    operating_system: debian6
    target: aarch64
    modules: []
    environment: {}
    extra_rpaths: []
"""
    update_cfg_section("compilers", test_cfg)

    install("x1%gcc")
    # output = solve("--show=asp", "x1%aocc")
    x = Spec("x1%aocc").concretized()
    output = solve("--reuse", "x1%aocc")
    import pdb; pdb.set_trace()
    print("hi")