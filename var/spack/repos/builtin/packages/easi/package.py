# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Easi(CMakePackage):
    """easi is a library for the Easy Initialization of models
    in three (or less or more) dimensional domains.
    """

    homepage = "https://easyinit.readthedocs.io"
    git = "https://github.com/SeisSol/easi.git"

    maintainers("Thomas-Ulrich", "davschneller", "vikaskurapati")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.5.0", tag="v1.5.0", commit="391698ab0072f66280d08441974c2bdb04a65ce0")
    version("1.4.0", tag="v1.4.0", commit="0d8fcf936574d93ddbd1d9222d46a93d4b119231")
    version("1.3.0", tag="v1.3.0", commit="99309a0fa78bf11d668c599b3ee469224f04d55b")
    version("1.2.0", tag="v1.2.0", commit="305a119338116a0ceac6b68b36841a50250d05b1")
    version("1.1.2", tag="v1.1.2", commit="4c87ef3b3dca9415d116ef102cb8de750ef7e1a0")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("python", default=True, description="Install python bindings")
    extends("python", when="+python")

    variant("asagi", default=True, description="build with ASAGI support")
    variant(
        "jit",
        default="impalajit,lua",
        description="build with JIT support",
        values=("impalajit", "impalajit-llvm", "lua"),
        multi=True,
    )

    depends_on("asagi +mpi +mpi3", when="+asagi")
    depends_on("yaml-cpp@0.6.2")

    depends_on("impalajit@llvm-1.0.0", when="jit=impalajit-llvm")
    depends_on("lua@5.3.2", when="jit=lua")
    depends_on("impalajit@main", when="jit=impalajit")

    depends_on("py-pybind11@2.6.2:", type="build", when="+python")

    conflicts("jit=impalajit", when="jit=impalajit-llvm")
    conflicts("jit=impalajit-llvm", when="jit=impalajit")

    conflicts("jit=impalajit", when="target=aarch64:")
    conflicts("jit=impalajit", when="target=ppc64:")
    conflicts("jit=impalajit", when="target=ppc64le:")
    conflicts("jit=impalajit", when="target=riscv64:")

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("ASAGI", "asagi"))
        args.append(self.define_from_variant("PYTHON_BINDINGS", "python"))
        self.define("PYBIND11_USE_FETCHCONTENT", False)
        spec = self.spec
        if spec.satisfies("jit=impalajit") or spec.satisfies("jit=impalajit-llvm"):
            args.append(self.define("IMPALAJIT", True))
            backend_type = "llvm" if "jit=impalajit-llvm" in spec else "original"
            args.append(self.define("IMPALAJIT_BACKEND", backend_type))
        else:
            args.append(self.define("IMPALAJIT", False))

        if spec.satisfies("jit=lua"):
            args.append(self.define("LUA", True))

        if spec.satisfies("+python"):
            args += [self.define("easi_INSTALL_PYTHONDIR", python_platlib)]

        return args

    def setup_run_environment(self, env):
        if self.spec.satisfies("+python"):
            full_path = os.path.join(python_platlib, "easilib/cmake/easi/python_wrapper")
            env.prepend_path("PYTHONPATH", full_path)
