# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from llnl.util import tty

from spack.package import *
from spack.pkg.builtin.gcc_runtime import get_elf_libraries


class IntelOneapiRuntime(Package):
    """Package for OneAPI compiler runtime libraries"""

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"
    has_code = False

    tags = ["runtime"]

    requires("%oneapi")

    depends_on("gcc-runtime", type="link")

    LIBRARIES = [
        "imf",
        "intlc",
        "irng",
        "svml",
        "ifcore",  # Fortran
        "ifcoremt",  # Fortran
        "ifport",  # Fortran
        "iomp5",
        "sycl",
    ]

    # libifcore ABI
    provides("fortran-rt", "ifcore@5", when="%oneapi@2021:")
    provides("sycl")

    def install(self, spec, prefix):
        if spec.platform in ["linux", "cray", "freebsd"]:
            libraries = get_elf_libraries(compiler=self.compiler, libraries=self.LIBRARIES)
        else:
            raise RuntimeError("Unsupported platform")

        mkdir(prefix.lib)

        if not libraries:
            tty.warn("Could not detect any shared OneAPI runtime libraries")
            return

        for path, name in libraries:
            install(path, os.path.join(prefix.lib, name))
