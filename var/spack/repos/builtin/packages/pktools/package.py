# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class Pktools(CMakePackage):
    """Processing Kernel for geospatial data"""

    homepage = "http://pktools.nongnu.org/html/index.html"
    url = "http://download.savannah.gnu.org/releases/pktools/pktools-2.6.7.tar.gz"

    license("GPL-3.0-or-later")

    version("2.6.7.1", sha256="519b6a500ce3c5ef3793c1cda1f5377f13b7d7591b5ccc376b2bd1de4bd4f7e5")
    version("2.6.7", sha256="f566647e93037cc01cebfe17ea554d798177fe5081887c70223dcca817f4fe7f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("fann", default=True, description="Build with libfann to enable related programs")
    variant("liblas", default=False, description="Build with libLAS support")

    depends_on("gdal")
    depends_on("gsl")
    depends_on("armadillo")
    depends_on("nlopt")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("fann", when="+fann")
    depends_on("liblas", when="+liblas")

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_CXX_STANDARD=11")
        args.append("-DPKTOOLS_WITH_UTILITIES=ON")
        if "+fann" in self.spec:
            args.append("-DBUILD_WITH_FANN=ON")
        else:
            args.append("-DBUILD_WITH_FANN=OFF")
        if "+liblas" in self.spec:
            args.append("-DBUILD_WITH_LIBLAS=ON")
        else:
            args.append("-DBUILD_WITH_LIBLAS=OFF")
        return args
