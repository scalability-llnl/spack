# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Tixi(CMakePackage):
    """TiXI is a fast and simple XML interface library and could be used
    from applications written in C, C++, Fortran, JAVA and Python."""

    homepage = "https://github.com/DLR-SC/tixi"
    url = "https://github.com/DLR-SC/tixi/archive/v3.0.3.tar.gz"
    git = "https://github.com/DLR-SC/tixi.git"

    maintainers("melven", "joergbrech")

    license("Apache-2.0")

    version("3.3.0", sha256="988d79ccd53c815d382cff0c244c0bb8e393986377dfb45385792766adf6f6a9")
    version("3.2.0", sha256="8df65c4d252d56e98c5ef2657c7aff6086a07b5686716e786891609adaca9d2d")
    version("3.1.0", sha256="4547133e452f3455b5a39045a8528955dce55faf059afe652a350ecf37d709ba")
    version("3.0.3", sha256="3584e0cec6ab811d74fb311a9af0663736b1d7f11b81015fcb378efaf5ad3589")
    version("2.2.4", sha256="9080d2a617b7c411b9b4086de23998ce86e261b88075f38c73d3ce25da94b21c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "shared", default=True, description="Enables the build of shared libraries", when="@3.0.3:"
    )
    variant("fortran", default=True, description="Enable Fortran bindings", when="@3.1.1:")
    variant("python", default=True, description="Add python bindings to PYTHONPATH")

    depends_on("python", when="~python", type="build")
    depends_on("python", when="+python", type=("build", "run"))
    conflicts("~shared", when="+python")
    depends_on("expat")
    depends_on("curl")
    depends_on("libxml2")
    depends_on("libxslt")

    @property
    def libs(self):
        # different library names for tixi@2 and tixi@3
        libname = "libtixi3" if "@3" in self.spec else "libTIXI"
        shared = "~shared" not in self.spec
        return find_libraries(libname, root=self.prefix, shared=shared, recursive=True)

    def cmake_args(self):
        return [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("TIXI_ENABLE_FORTRAN", "fortran"),
        ]

    def setup_run_environment(self, env):
        """Allow to import tixi3wrapper in python"""

        if "+python" in self.spec:
            # add tixi3wrapper.py to the PYTHONPATH
            if "@3" in self.spec:
                env.prepend_path("PYTHONPATH", self.spec.prefix.share.tixi3.python)
            else:
                env.prepend_path("PYTHONPATH", self.spec.prefix.share.tixi.python)

            # allow ctypes to find the tixi library
            libs = ":".join(self.spec["tixi"].libs.directories)
            if sys.platform == "darwin":
                env.prepend_path("DYLD_FALLBACK_LIBRARY_PATH", libs)
            else:
                env.prepend_path("LD_LIBRARY_PATH", libs)
