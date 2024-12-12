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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
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

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
""",
)


_pkgx4 = (
    "x4",
    """\
from spack.package import *    

class X4(Package):
    version("4.1")
    version("4.0")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
""",
)


_glibc = (
    "glibc",
    """\
from spack.package import *    

class Glibc(Package):
    provides("libc")
""",
)


# This includes libc dependency, unlike compiler_runtime.test repo
_gcc_runtime = (
    "gcc-runtime",
    """\
from spack.package import *

class GccRuntime(Package):
    has_code = False

    requires("%gcc")

    provides("fortran-rt", "libgfortran")
    provides("libgfortran@3", when="%gcc@:6")
    provides("libgfortran@4", when="%gcc@7")
    provides("libgfortran@5", when="%gcc@8:")

    depends_on("libc", type="link", when="platform=linux")
"""
)


_gcc = (
    "gcc",
    """\
from spack.package import *

class Gcc(Package):
    homepage = "http://www.example.com/"
    has_code = False

    version("13.2.0")
    version("12.3.0")

    @classmethod
    def runtime_constraints(cls, *, spec, pkg):
        pkg("*").depends_on(
            "gcc-runtime",
            when="%gcc",
            type="link",
            description="If any package uses %gcc, it depends on gcc-runtime",
        )
        pkg("*").depends_on(
            f"gcc-runtime@{str(spec.version)}:",
            when=f"%{str(spec)}",
            type="link",
            description=f"If any package uses %{str(spec)}, "
            f"it depends on gcc-runtime@{str(spec.version)}:",
        )
        # The version of gcc-runtime is the same as the %gcc used to "compile" it
        pkg("gcc-runtime").requires(f"@={str(spec.version)}", when=f"%{str(spec)}")

        # If a node used %gcc@X.Y its dependencies must use gcc-runtime@:X.Y
        pkg("*").propagate(f"%gcc@:{str(spec.version)}", when=f"%{str(spec)}")
"""
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
            _glibc,
            _gcc,
            _gcc_runtime,
        ],
    )


import spack.solver.asp
import os
import spack.paths


@pytest.fixture
def enable_runtimes():
    original = spack.solver.asp.WITH_RUNTIME
    spack.solver.asp.WITH_RUNTIME = True
    yield
    spack.solver.asp.WITH_RUNTIME = original


@pytest.fixture
def test_repo(_create_test_repo, monkeypatch, mock_stage):
    with spack.repo.use_repositories(_create_test_repo) as mock_repo_path:
        yield mock_repo_path


def test_diamond(concretize_scope, test_repo):
    Spec("x1").concretized()


install = SpackCommand("install")
solve = SpackCommand("solve")


import spack.platforms
from spack.platforms._platform import Platform
import spack.operating_systems
import archspec.cpu
import spack.compiler


class TestLinux(Platform):
    front_end = "x86_64"
    back_end = "x86_64"
    default = "x86_64"

    front_os = "debian6"
    back_os = "debian6"
    default_os = "debian6"

    def __init__(self):
        super().__init__("linux")
        self.add_target(self.default, archspec.cpu.TARGETS[self.default])
        self.add_target(self.front_end, archspec.cpu.TARGETS[self.front_end])

        os = spack.operating_systems.OperatingSystem("debian", 6)
        self.add_operating_system(
            self.default_os, os
        )
        self.add_operating_system(
            self.front_os, os
        )


@pytest.fixture
def pretend_linux(monkeypatch, tmpdir):
    pretend_libc = Spec("glibc@=2.28")
    pretend_libc.external_path = str(tmpdir.join("fake-libc").ensure(dir=True))

    monkeypatch.setattr(spack.compiler.Compiler, "default_libc", pretend_libc)
    with spack.platforms.use_platform(TestLinux()):
        yield


def test_with_cfg(mutable_mock_env_path, install_mockery, mock_fetch, concretize_scope, test_repo, pretend_linux, enable_runtimes):
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
    target: x86_64
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
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
"""
    update_cfg_section("compilers", test_cfg)

    output = solve("--show=asp", "x4%gcc")

    import pdb; pdb.set_trace()

    install("x1%gcc")
    # output = solve("--show=asp", "x1%aocc")
    x = Spec("x1%aocc").concretized()
    output = solve("--reuse", "x1%aocc")
    import pdb; pdb.set_trace()
    print("hi")