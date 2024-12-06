# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Armadillo(CMakePackage):
    """Armadillo is a high quality linear algebra library (matrix maths)
    for the C++ language, aiming towards a good balance between speed and
    ease of use.
    """

    homepage = "http://arma.sourceforge.net/"
    url = "http://sourceforge.net/projects/arma/files/armadillo-7.200.1.tar.xz"

    version("8.100.1", md5="d9762d6f097e0451d0cfadfbda295e7c")
    version("7.950.1", md5="c06eb38b12cae49cab0ce05f96147147")
    version("7.900.1", md5="5ef71763bd429a3d481499878351f3be")
    version("7.500.0", md5="7d316fdf3c3c7ea92b64704180ae315d")
    version("7.200.2", md5="b21585372d67a8876117fd515d8cf0a2")
    version("7.200.1", md5="ed86d6df0058979e107502e1fe3e469e")

    variant("hdf5", default=False, description="Include HDF5 support")

    depends_on("cmake@2.8.12:", type="build")
    depends_on("arpack-ng")  # old arpack causes undefined symbols
    depends_on("blas")
    depends_on("lapack")
    depends_on("superlu@5.2:")
    depends_on("hdf5", when="+hdf5")

    patch("undef_linux.patch", when="platform=linux")

    def cmake_args(self):
        spec = self.spec

        # TUTORIAL: fix the lines below by adding the appropriate query to
        # the right dependency. To ask a dependency, e.g. `blas`, for the
        # list of libraries it provides it suffices to access its `libs`
        # attribute:
        #
        #    blas_libs = spec['blas'].libs
        #
        # The CMake variables below require a semicolon separated list:
        #
        #    blas_libs.joined(';')

        return [
            # ARPACK support
            "-DARPACK_LIBRARY={0}".format("FIXME: arpack-ng"),
            # BLAS support
            "-DBLAS_LIBRARY={0}".format("FIXME: blas"),
            # LAPACK support
            "-DLAPACK_LIBRARY={0}".format("FIXME: lapack"),
            # SuperLU support
            "-DSuperLU_INCLUDE_DIR={0}".format(spec["superlu"].prefix.include),
            "-DSuperLU_LIBRARY={0}".format("FIXME: superlu"),
            # HDF5 support
            "-DDETECT_HDF5={0}".format("ON" if "+hdf5" in spec else "OFF"),
        ]
