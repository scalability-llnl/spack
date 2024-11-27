# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class LlvmOpenmpOmpt(CMakePackage):
    """The OpenMP subproject provides an OpenMP runtime for use with the
    OpenMP implementation in Clang. This branch includes experimental
    changes for OMPT, the OpenMP Tools interface"""

    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    git = "https://github.com/OpenMPToolsInterface/LLVM-openmp.git"

    license("MIT")

    # tr6_forwards branch (last commit from 2017)
    version("tr6_forwards", commit="4b29de49ce90cfb5c3cbc6bb7d91660b70bddb5d")
    version("3.9.2b2", commit="5cdca5dd3c0c336d42a335ca7cff622e270c9d47")

    # align-to-tr-rebased branch
    version("3.9.2b", commit="982a08bcf3df9fb5afc04ac3bada47f19cc4e3d3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # variant for building llvm-openmp-ompt as a stand alone library
    variant(
        "standalone",
        default=False,
        description="Build llvm openmpi ompt library as a \
                         stand alone entity.",
    )
    # variant for building libomptarget
    variant(
        "libomptarget", default=True, description="Enable building libomptarget for offloading"
    )

    depends_on("cmake@2.8:", type="build")
    depends_on("llvm", when="~standalone")
    depends_on("ninja@1.5:", type="build")
    depends_on("perl@5.22.0:", type="build")
    depends_on("elf", when="+libomptarget")
    depends_on("libffi", when="+libomptarget")

    generator("ninja")

    def cmake_args(self):
        cmake_args = [
            "-DLIBOMP_OMPT_SUPPORT=on",
            "-DLIBOMP_OMPT_BLAME=on",
            "-DLIBOMP_OMPT_TRACE=on",
            "-DCMAKE_C_COMPILER=%s" % spack_cc,
            "-DCMAKE_CXX_COMPILER=%s" % spack_cxx,
        ]

        # Build llvm-openmp-ompt as a stand alone library
        # CMAKE rpath variable prevents standalone error
        # where this package wants the llvm tools path
        if self.spec.satisfies("+standalone"):
            cmake_args.extend(
                [
                    "-DLIBOMP_STANDALONE_BUILD=true",
                    "-DCMAKE_BUILD_WITH_INSTALL_RPATH=true",
                    "-DLIBOMP_USE_DEBUGGER=false",
                ]
            )

        # Build llvm-openmp-ompt using the tr6_forwards branch
        # This requires the version to be 5.0 (50)
        if self.spec.satisfies("@tr6_forwards"):
            cmake_args.extend(["-DLIBOMP_OMP_VERSION=50"])

        # Disable support for libomptarget
        if self.spec.satisfies("~libomptarget"):
            cmake_args.extend(["-DOPENMP_ENABLE_LIBOMPTARGET=OFF"])

        return cmake_args

    @property
    def libs(self):
        return find_libraries("libomp", root=self.prefix, recursive=True)
