# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LdcBootstrap(CMakePackage):
    """The LDC project aims to provide a portable D programming language
    compiler with modern optimization and code generation capabilities.

    LDC is fully Open Source; the parts of the code not taken/adapted from
    other projects are BSD-licensed (see the LICENSE file for details).

    Consult the D wiki for further information: https://wiki.dlang.org/LDC

    This old version of the compiler is needed to bootstrap newer ones.
    """

    homepage = "https://dlang.org/"
    url = "https://github.com/ldc-developers/ldc/releases/download/v0.17.4/ldc-0.17.4-src.tar.gz"

    license("LGPL-2.1-or-later")

    # This is the last version that does not require a D compiler to bootstrap
    version("0.17.4", sha256="48428afde380415640f3db4e38529345f3c8485b1913717995547f907534c1c3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("llvm@3.7:")
    depends_on("zlib-api")
    depends_on("libconfig")
    depends_on("curl")
    depends_on("libedit")
    depends_on("binutils")

    def setup_dependent_build_environment(self, env, dep_spec):
        # The code below relies on this function being executed after the
        # environment has been sanitized (because LD_LIBRARY_PATH is among
        # the variables that get unset)

        # We need libphobos in LD_LIBRARY_PATH
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.lib)

    def cmake_args(self):
        return ["-DBUILD_SHARED_LIBS:BOOL=ON"]
