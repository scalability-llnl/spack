# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shtools(MakefilePackage):
    """SHTOOLS - Spherical Harmonic Tools"""

    homepage = "https://shtools.github.io/SHTOOLS/"
    url = "https://github.com/SHTOOLS/SHTOOLS/archive/v4.5.tar.gz"

    maintainers("eschnett")

    version("4.10.2", sha256="0caece67d65ddde19a79ec79bc6244f447f6fa878e5b2dc3f635cae2a3d1ee8c")
    version("4.10.1", sha256="f4fb5c86841fe80136b520d2040149eafd4bc2d49da6b914d8a843b812f20b61")
    version("4.9.1", sha256="5c22064f9daf6e9aa08cace182146993aa6b25a6ea593d92572c59f4013d53c2")
    version("4.8", sha256="c36fc86810017e544abbfb12f8ddf6f101a1ac8b89856a76d7d9801ffc8dac44")
    version("4.5", sha256="1975a2a2bcef8c527d321be08c13c2bc479e0d6b81c468a3203f95df59be4f89")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Note: This package also provides Python wrappers. We do not
    # install these properly yet, only the Fortran library is
    # installed.

    # The Makefile expects the "other" libtool, not the GNU libtool we have in
    # Spack
    patch("nolibtool.patch", when="@:4.9")

    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("blas")
    depends_on("fftw precision=double")
    depends_on("lapack")
    depends_on("py-flake8", type="test")

    def patch(self):
        """make check fix: Silence "do not use bare 'except'" in number of files"""
        filter_file("ignore=", "ignore=E722,", "Makefile")

    # Options for the Makefile
    def makeopts(self, spec, prefix):
        return [
            "F95={0}".format(self.compiler.fc),
            "F95FLAGS={0} -O3 -std=gnu -ffast-math".format(self.compiler.fc_pic_flag),
            "OPENMPFLAGS={0}".format(self.compiler.openmp_flag),
            "BLAS={0}".format(spec["blas"].libs),
            "FFTW={0}".format(spec["fftw"].libs),
            "LAPACK={0}".format(spec["lapack"].libs),
            "PREFIX={0}".format(prefix),
            "PWD={0}".format(self.build_directory),
        ]

    def build(self, spec, prefix):
        with working_dir(self.build_directory):
            # The 'fortran' and 'fortran-mp' targets must be built separately
            make("fortran", *self.makeopts(spec, prefix))
            if spec.satisfies("+openmp"):
                make("fortran-mp", *self.makeopts(spec, prefix))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install", *self.makeopts(spec, prefix))
