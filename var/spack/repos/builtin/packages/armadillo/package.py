# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Armadillo(CMakePackage):
    """Armadillo is a high quality linear algebra library (matrix maths)
    for the C++ language, aiming towards a good balance between speed and
    ease of use."""

    homepage = "https://arma.sourceforge.net/"
    url = "http://sourceforge.net/projects/arma/files/armadillo-8.100.1.tar.xz"
    git = "https://gitlab.com/conradsnicta/armadillo-code.git"

    license("Apache-2.0")

    version("14.0.2", sha256="248e2535fc092add6cb7dea94fc86ae1c463bda39e46fd82d2a7165c1c197dff")
    version("12.8.4", sha256="558fe526b990a1663678eff3af6ec93f79ee128c81a4c8aef27ad328fae61138")
    version("12.8.3", sha256="2922589f6387796504b340da6bb954bef3d87574c298515893289edd2d890151")
    version("12.8.2", sha256="03b62f8c09e4f5d74643b478520741b8e27b55e7e4525978fcae2f5d791ac3bf")
    version("12.8.1", sha256="2781dd3a6cc5f9a49c91a4519dde2b1c24335a5bfe0cc1c9881b6363142452b4")
    version("12.4.0", sha256="9905282781ced3f99769b0e45a705ecb50192ca1622300707b3302ea167dc883")
    version("12.2.0", sha256="b0dce042297e865add3351dad77f78c2c7638d6632f58357b015e50edcbd2186")
    version("12.0.1", sha256="230a5c75daad52dc47e1adce8f5a50f9aa4e4354e0f1bb18ea84efa2e70e20df")
    version("10.5.0", sha256="ea990c34dc6d70d7c95b4354d9f3b0819bde257dbb67796348e91e196082cb87")
    version("9.800.3", sha256="a481e1dc880b7cb352f8a28b67fe005dc1117d4341277f12999a2355d40d7599")
    version("8.100.1", sha256="54773f7d828bd3885c598f90122b530ded65d9b195c9034e082baea737cd138d")
    version("7.950.1", sha256="a32da32a0ea420b8397a53e4b40ed279c1a5fc791dd492a2ced81ffb14ad0d1b")

    depends_on("cxx", type="build")  # generated

    variant("hdf5", default=False, description="Include HDF5 support")

    depends_on("cmake@2.8.12:", type="build")
    depends_on("cmake@3.5:", type="build", when="@14:")
    depends_on("arpack-ng")  # old arpack causes undefined symbols
    depends_on("blas")
    depends_on("lapack")
    depends_on("superlu@5.2:")
    depends_on("hdf5", when="+hdf5")

    # Adds an `#undef linux` to prevent preprocessor expansion of include
    # directories with `linux` in them getting transformed into a 1.
    # E.g. `/path/linux-x86_64/dir` -> `/path/1-x86_64/dir` if/when a linux
    # platform's compiler is adding `#define linux 1`.
    patch("undef_linux.patch", when="platform=linux")

    def patch(self):
        # Do not include Find{BLAS_type} because we are specifying the
        # BLAS/LAPACK libraries explicitly.
        filter_file(
            r"include(ARMA_FindMKL)", "#include(ARMA_FindMKL)", "CMakeLists.txt", string=True
        )
        filter_file(
            r"include(ARMA_FindOpenBLAS)",
            "#include(ARMA_FindOpenBLAS)",
            "CMakeLists.txt",
            string=True,
        )
        filter_file(
            r"include(ARMA_FindATLAS)", "#include(ARMA_FindATLAS)", "CMakeLists.txt", string=True
        )

        # Comment out deprecated call to GET_FILENAME_COMPONENT. This allows
        # armadillo to be built with MKL.
        with working_dir(join_path(self.stage.source_path, "cmake_aux", "Modules")):
            filter_file("GET_FILENAME_COMPONENT", "#GET_FILENAME_COMPONENT", "ARMA_FindBLAS.cmake")
            filter_file(
                "GET_FILENAME_COMPONENT", "#GET_FILENAME_COMPONENT", "ARMA_FindLAPACK.cmake"
            )

    def cmake_args(self):
        spec = self.spec

        return [
            # ARPACK support
            self.define("ARPACK_LIBRARY", spec["arpack-ng"].libs.joined(";")),
            # BLAS support
            self.define("BLAS_LIBRARY", spec["blas"].libs.joined(";")),
            # LAPACK support
            self.define("LAPACK_LIBRARY", spec["lapack"].libs.joined(";")),
            # SuperLU support
            self.define("SuperLU_INCLUDE_DIR", spec["superlu"].prefix.include),
            self.define("SuperLU_LIBRARY", spec["superlu"].libs.joined(";")),
            # HDF5 support
            self.define("DETECT_HDF5", "ON" if spec.satisfies("+hdf5") else "OFF"),
        ]
