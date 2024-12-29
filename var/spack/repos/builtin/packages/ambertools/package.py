# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ambertools(CMakePackage):
    """AmberTools is a free, useful standalone package and a prerequisite
    for installing Amber itself. The AmberTools suite is free of charge,
    and its components are mostly released under the GNU General Public
    License (GPL). A few components are included that are in the public
    domain or which have other, open-source, licenses. The libsander and
    libpbsa libraries use the LGPL license."""

    homepage = "https://ambermd.org/AmberTools.php"
    url = "https://ambermd.org/downloads/AmberTools22jlmrcc.tar.bz2"

    maintainers("d-beltran")

    version("22jlmrcc", sha256="1571d4e0f7d45b2a71dce5999fa875aea8c90ee219eb218d7916bf30ea229121")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("tcsh", type="build")
    depends_on("zlib", type=("build", "run"))
    depends_on("bzip2", type=("build", "run"))
    depends_on("blas", type=("build", "run"))
    depends_on("lapack", type=("build", "run"))
    depends_on("arpack-ng", type=("build", "run"))
    depends_on("netcdf-c", type=("build", "run"))
    depends_on("netcdf-fortran", type=("build", "run"))
    depends_on("fftw", type=("build", "run"))
    depends_on("readline", type=("build", "run"))
    depends_on("netlib-xblas~plain_blas", type=("build", "run"))
    # Specific variants needed for boost according to build logs
    depends_on(
        "boost+thread+system+program_options+iostreams+regex+timer+chrono+filesystem+graph",
        type=("build", "run"),
    )
    # Python dependencies
    depends_on("python@3.8:3.10 +tkinter", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))

    def cmake_args(self):
        # Translated from ambertools build/run_cmake script
        # We also add the TRUST_SYSTEM_LIBS argument mentioned in the ambertools guide
        #   https://ambermd.org/pmwiki/pmwiki.php/Main/CMake-Guide-to-Options
        args = [
            self.define("COMPILER", "GNU"),
            self.define("MPI", False),
            self.define("CUDA", False),
            self.define("INSTALL_TESTS", True),
            self.define("DOWNLOAD_MINICONDA", False),
            self.define("TRUST_SYSTEM_LIBS", True),
            # This is to avoid the x11 (X11_Xext_LIB) error
            # It is equivalent to the "-noX11" flag accoridng to the docs:
            # https://ambermd.org/pmwiki/pmwiki.php/Main/CMake-Common-Options
            self.define("BUILD_GUI", False),
        ]
        return args

    def setup_run_environment(self, env):
        env.set("AMBER_PREFIX", self.prefix)
        env.set("AMBERHOME", self.prefix)

    def setup_build_environment(self, env):
        env.set("AMBER_PREFIX", self.prefix)
        env.set("AMBERHOME", self.prefix)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        make("test.serial")

    # Temporarily copy netcdf.h header file to netcdf-fortran/include to pass the Ambertools
    # cmake check (quickest fix, will probably cause problems, needs to change)
    @run_before("cmake")
    def fix_check(self):
        cp = Executable("cp")
        cp(
            self.spec["netcdf-c"].headers.directories[0] + "/netcdf.h",
            self.spec["netcdf-fortran"].headers.directories[0],
        )
