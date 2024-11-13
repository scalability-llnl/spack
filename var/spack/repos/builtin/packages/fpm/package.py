# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import stat

from spack.package import *


class Fpm(Package):
    """
    Fortran Package Manager (fpm) is a package manager and build system for Fortran.
    Its key goal is to improve the user experience of Fortran programmers.
    It does so by making it easier to build your Fortran program or library, run the
    executables, tests, and examples, and distribute it as a dependency to other
    Fortran projects.
    """

    homepage = "https://github.com/fortran-lang/fpm"
    url = "https://github.com/fortran-lang/fpm/releases/download/v0.4.0/fpm-0.4.0.zip"

    maintainers("awvwgk")

    license("MIT")

    version("0.10.0", sha256="00d687e17bdada4dcae0ff1ea2e01bad287dcc77a74c3bbde0c9ff9633b655bb")
    version("0.9.0", sha256="484debabd7d22186ac41f865ddf63475c279a61a51aaff5636ed615860b5b8d7")
    version("0.8.2", sha256="67fd8f4f78d19662c61855f531465e347ab0bc913ba59bd419f75f4022d2cd70")
    version("0.8.1", sha256="0bd978bb1d3f2a3297d82a0d6ac009746a466cfa9a59ba3b6513b74e5ce4b7bf")
    version("0.8.0", sha256="d63162a2ab013c19cefc938e52717c30f78e04de94384d4589c55a48be2724f1")
    version("0.7.0", sha256="536dec7d4502221734683b15e6ff64a6ab3f9910df122d18f851c9a68711f91f")
    version("0.6.0", sha256="365516f66b116a112746af043e8eccb3d854d6feb1fad0507c570433dacbf7be")
    version("0.5.0", sha256="e4a06956d2300f9aa1d06bd3323670480e946549617582e32684ded6921a921e")
    version("0.4.0", sha256="cd9b80b7f40d9cf357ca8d5d4fe289fd32dfccb729bad7d2a68f245e4cdd0045")
    version("0.3.0", sha256="3368d1b17e2d1368559174c796ce0e184cb6bf79c939938c6d166fbd15959fa3")

    variant("openmp", default=True, description="Use OpenMP parallelisation")

    depends_on("curl", type="build")
    depends_on("git@1.8.5:", type="build")

    def setup_build_environment(self, env):
        if self.spec.satisfies("@0.4.0"):
            env.set("FPM_C_COMPILER", self.compiler.cc)

        env.set("FPM_CC", self.compiler.cc)

        fflags = "-O3"
        if self.spec.satisfies("+openmp"):
            fflags += " " + self.compiler.openmp_flag
        env.set("FFLAGS", fflags)

    def install(self, spec, prefix):
        """
        A three step bootstrapping procedure to get the fpm binary:

        1. acquire single file source version of fpm (using curl)
        2. build bootstrap version from single file source version (using $FC)
        3. build full fpm version using bootstrap version

        This functionality is provided by the ``install.sh`` script.
        """

        # Perform `chmod +x ./install.sh`
        script_path = "./install.sh"
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IXUSR)

        script = Executable(script_path)
        script(*self.install_args())

    def install_args(self):
        args = ["--prefix={0}".format(self.prefix)]
        return args
