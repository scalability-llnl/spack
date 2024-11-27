# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xcfun(CMakePackage):
    """Exchange-Correlation functionals with arbitrary order derivatives."""

    homepage = "https://github.com/dftlibs/xcfun"
    url = "https://github.com/dftlibs/xcfun/archive/v2.1.0.tar.gz"

    maintainers("robertodr", "bast")

    license("MPL-2.0-no-copyleft-exception")

    version("2.1.1", sha256="8b602df74c7be83d501532565deafd1b7881946d94789122f24c309a669298ab")
    version("2.1.0", sha256="64aac8c933cc129ce6326f3827e342abfd10b94ea4a302aaca9f10d342ad7656")
    version("2.0.2", sha256="b79a71861a9e1d0e33c1be89b34f6f052d430cd495a7df982c407ad0140c1dcd")
    version("2.0.1", sha256="719383c3fffdd5da5b005f56ffd97457b0b2fb48317e955263ef5384d53ddfca")
    version("2.0.0", sha256="34398e935c522d0b55e1803fd6116e7cd40677d1add8894ef08362361705cf25")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    extends("python")
    depends_on("cmake@3.14:", type="build")
    depends_on("python@3:")
    depends_on("py-pybind11")
    depends_on("py-numpy")

    def cmake_args(self):
        spec = self.spec

        args = [
            "-DCMAKE_INSTALL_LIBDIR=lib",
            "-DPYMOD_INSTALL_LIBDIR=/python{0}/site-packages".format(spec["python"].version[:-1]),
            "-DXCFUN_MAX_ORDER=8",
            "-DXCFUN_PYTHON_INTERFACE=ON",
            "-DENABLE_TESTALL=OFF",
        ]
        return args
