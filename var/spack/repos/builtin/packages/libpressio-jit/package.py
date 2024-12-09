# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioJit(CMakePackage):
    """the FZ module compiler"""

    homepage = "https://github.com/robertu94/libpressio_jit"
    url = "https://github.com/robertu94/libpressio_jit/archive/refs/tags/0.0.1.tar.gz"
    git = "https://github.com/robertu94/libpressio_jit"

    maintainers("robertu94")
    license("BSD-4-Clause", checked_by="robertu94")

    version("0.0.1", sha256="6aa771c624980589cc941e8cfca1c5fb6cea3fef2b060f58bfdf07109eda8c08")

    depends_on("cxx", type="build")  # generated

    variant("poorjit", description="include the prototype poorjit compiler", default=True)

    depends_on("poorjit", when="+poorjit")
    depends_on("libpressio@0.99.1:")

    def cmake_args(self):
        args = [self.define_from_variant("LIBPRESSIO_JIT_HAS_POORJIT", "poorjit")]
        return args
