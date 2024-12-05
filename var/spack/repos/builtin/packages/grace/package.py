# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grace(AutotoolsPackage):
    """Grace is a WYSIWYG 2D plotting tool for the X Window System and M*tif."""

    homepage = "https://plasma-gate.weizmann.ac.il/Grace"
    # The main site (ftp://plasma-gate.weizmann.ac.il/pub/grace/)
    # is currently unavailable so we use one of the mirrors instead.
    url = "ftp://ftp.fu-berlin.de/unix/graphics/grace/src/grace5/grace-5.1.25.tar.gz"

    maintainers("RemiLacroix-IDRIS")

    license("GPL-2.0-or-later")

    version("5.1.25", sha256="751ab9917ed0f6232073c193aba74046037e185d73b77bab0f5af3e3ff1da2ac")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("libx11")
    depends_on("libxext")
    depends_on("libxmu")
    depends_on("libxp")
    depends_on("libxt")
    depends_on("libice")
    depends_on("libsm")
    depends_on("motif")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("fftw@2.0:2")
    depends_on("netcdf-c")

    def patch(self):
        # Spack's FFTW2 has prefixed headers so patch the code accordingly.
        # We are not patching "ac-tools/aclocal.m4" since it is not needed
        # currently and would require to run "autoreconf".
        filter_file("<fftw.h>", "<dfftw.h>", "configure", "src/fourier.c")
        filter_file(
            "char   filename[128];",
            "char   filename[4096];",
            "T1lib/type1/scanfont.c",
            string=True,
        )
        filter_file(
            "char CurFontName[120];",
            "char CurFontName[4096];",
            "T1lib/type1/fontfcn.c",
            string=True,
        )

    def configure_args(self):
        args = []
        args.append("--with-fftw")
        # Spack's FFTW2 has prefixed libraries
        args.append("--with-fftw-library=-ldfftw")
        for driver in ["jpeg", "png"]:
            args.append("--enable-{0}drv".format(driver))
        args.append("--enable-netcdf")
        return args

    def setup_run_environment(self, env):
        # Grace installs a subfolder in the prefix directory
        # so we account for that...
        env.prepend_path("PATH", self.prefix.grace.bin)
