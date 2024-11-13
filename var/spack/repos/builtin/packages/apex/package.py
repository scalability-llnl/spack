# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Apex(CMakePackage):
    """Autonomic Performance Environment for eXascale (APEX)."""

    maintainers("khuck")
    homepage = "https://uo-oaciss.github.io/apex"
    url = "https://github.com/UO-OACISS/apex/archive/v2.6.4.tar.gz"
    git = "https://github.com/UO-OACISS/apex"

    version("develop", branch="develop")
    version("master", branch="master")
    version("2.6.5", sha256="2ba29a1198c904ac209fc6bc02962304a1416443b249f34ef96889aff39644ce")
    version("2.6.4", sha256="281a673f447762a488577beaa60e48d88cb6354f220457cf8f05c1de2e1fce70")
    version("2.6.3", sha256="7fef12937d3bd1271a01abe44cb931b1d63823fb5c74287a332f3012ed7297d5")
    version("2.6.2", sha256="0c3ec26631db7925f50cf4e8920a778b57d11913f239a0eb964081f925129725")
    version("2.6.1", sha256="511dbab0af541489052a3d6379c48f9577e51654491d3b2c8545020e9d29fb29")
    version("2.6.0", sha256="25b4f6afd1083475dc6680b5da87759c62d31fcf368996185573694fc40d5317")
    version(
        "2.5.1",
        sha256="c01016e6a8a3a77e1021281ae53681cb83ea7a369c346ef85d45d27bacca2fca",
        deprecated=True,
    )
    version(
        "2.5.0",
        sha256="d4a95f6226985acf2143e2b779b7bba3caf823564b04826b022f1a0c31093a0f",
        deprecated=True,
    )
    version(
        "2.4.1",
        sha256="055d09dd36c529ebd3bab4defbec4ad1d227c004a291faf26e77e4ab79ce470c",
        deprecated=True,
    )
    version(
        "2.4.0",
        sha256="15d8957da7b37d2c684a6f0f32aef65b0b26be6558da17963cf71f3fd3cfdf2f",
        deprecated=True,
    )
    version(
        "2.3.2",
        sha256="acf37c024a2283cafbf206f508929208b62c8f800af22ad7c74c570863a31bb4",
        deprecated=True,
    )
    version(
        "2.3.1",
        sha256="86bf6933f2c53531fcb24cda9fc7dc9919909bed54740d1e0bc3e7ce6ed78091",
        deprecated=True,
    )
    version(
        "2.3.0",
        sha256="7e1d16c9651b913c5e28abdbad75f25c55ba25e9fa35f5d979c1d3f9b9852c58",
        deprecated=True,
    )
    version(
        "2.2.0",
        sha256="cd5eddb1f6d26b7dbb4a8afeca2aa28036c7d0987e0af0400f4f96733889c75c",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Disable some default dependencies on Darwin/OSX
    darwin_default = False
    if sys.platform != "darwin":
        darwin_default = True

    # Enable by default
    variant("activeharmony", default=False, description="Enables Active Harmony support")
    variant("plugins", default=True, description="Enables Policy Plugin support")
    variant("binutils", default=darwin_default, description="Enables Binutils support")
    variant("otf2", default=True, description="Enables OTF2 support")
    variant(
        "gperftools",
        default=darwin_default,
        description="Enables Google PerfTools TCMalloc support",
    )
    variant("openmp", default=darwin_default, description="Enables OpenMP support")
    variant("papi", default=darwin_default, description="Enables PAPI support")
    variant("kokkos", default=True, description="Enables Kokkos support")

    # Disable by default
    variant("cuda", default=False, description="Enables CUDA support")
    variant("hip", default=False, description="Enables ROCm/HIP support")
    variant("sycl", default=False, description="Enables Intel SYCL support (Level0)")
    variant("jemalloc", default=False, description="Enables JEMalloc support")
    variant("lmsensors", default=False, description="Enables LM-Sensors support")
    variant("mpi", default=False, description="Enables MPI support")
    variant("starpu", default=False, description="Enables StarPU support")
    variant("tests", default=False, description="Build Unit Tests")
    variant("examples", default=False, description="Build Examples")

    # Dependencies
    depends_on("zlib-api")
    depends_on("cmake@3.10.0:", type="build")
    depends_on("kokkos", type="build", when="+kokkos")
    depends_on("binutils@2.33:+libiberty+headers", when="+binutils")
    depends_on("gettext", when="+binutils ^binutils+nls")
    depends_on("activeharmony@4.6:", when="+activeharmony")
    depends_on("activeharmony@4.6:", when="+plugins")
    depends_on("otf2@2.1:", when="+otf2")
    depends_on("mpi", when="+mpi")
    depends_on("gperftools", when="+gperftools")
    depends_on("jemalloc", when="+jemalloc")
    depends_on("lm-sensors", when="+lmsensors")
    depends_on("papi@5.7.0:", when="+papi")
    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+hip")
    depends_on("sycl", when="+sycl")
    depends_on("roctracer-dev", when="+hip")
    depends_on("rocm-smi-lib", when="+hip")

    # Conflicts
    conflicts("+jemalloc", when="+gperftools")
    conflicts("+plugins", when="~activeharmony")
    # Compatibility fixed in 2.6.0 with
    # https://github.com/UO-OACISS/apex/commit/4a7bdbb93367c3b1172ccb978825c67316f8bf4a
    conflicts("^otf2@3:", when="@:2.5")

    # https://github.com/UO-OACISS/apex/pull/177#issuecomment-1726322959
    conflicts("+openmp", when="%gcc")

    # Up to 2.6.3 Kokkos support is always enabled. In 2.6.4 and 2.6.5 there is
    # a CMake option to disable Kokkos support but it doesn't work:
    # https://github.com/UO-OACISS/apex/issues/180.
    conflicts("~kokkos", when="@:2.6.5")

    # Patches

    # This patch ensures that the missing dependency_tree.hpp header is
    # installed
    patch("install-includes.patch", when="@2.3.2:2.4.1")

    def cmake_args(self):
        args = []
        spec = self.spec
        # CMake variables were updated in version 2.3.0, to make
        prefix = "APEX_WITH"
        test_prefix = "APEX_"
        if spec.satisfies("@2.2.0"):
            prefix = "USE"
            test_prefix = ""

        args.append(self.define_from_variant(prefix + "_ACTIVEHARMONY", "activeharmony"))
        args.append(self.define_from_variant(prefix + "_BFD", "binutils"))
        args.append(self.define_from_variant("APEX_WITH_CUDA", "cuda"))
        args.append(self.define_from_variant("APEX_WITH_HIP", "hip"))
        args.append(self.define_from_variant("APEX_WITH_LEVEL0", "sycl"))
        args.append(self.define_from_variant(prefix + "_MPI", "mpi"))
        args.append(self.define_from_variant(prefix + "_OMPT", "openmp"))
        args.append(self.define_from_variant(prefix + "_OTF2", "otf2"))
        args.append(self.define_from_variant(prefix + "_PAPI", "papi"))
        args.append(self.define_from_variant(prefix + "_PLUGINS", "plugins"))
        args.append(self.define_from_variant(prefix + "_LM_SENSORS", "lmsensors"))
        args.append(self.define_from_variant(prefix + "_TCMALLOC", "gperftools"))
        args.append(self.define_from_variant(prefix + "_JEMALLOC", "jemalloc"))
        args.append(self.define_from_variant(prefix + "_KOKKOS", "kokkos"))
        args.append(self.define_from_variant(test_prefix + "BUILD_TESTS", "tests"))
        args.append(self.define_from_variant(test_prefix + "BUILD_EXAMPLES", "examples"))

        if spec.satisfies("+activeharmony"):
            args.append("-DACTIVEHARMONY_ROOT={0}".format(spec["activeharmony"].prefix))

        if spec.satisfies("+binutils"):
            args.append("-DBFD_ROOT={0}".format(spec["binutils"].prefix))

        if spec.satisfies("+binutils ^binutils+nls"):
            if "intl" in self.spec["gettext"].libs.names:
                args.append("-DCMAKE_SHARED_LINKER_FLAGS=-lintl")

        if spec.satisfies("+otf2"):
            args.append("-DOTF2_ROOT={0}".format(spec["otf2"].prefix))

        if spec.satisfies("+papi"):
            args.append("-DPAPI_ROOT={0}".format(spec["papi"].prefix))

        if spec.satisfies("+gperftools"):
            args.append("-DGPERFTOOLS_ROOT={0}".format(spec["gperftools"].prefix))

        if spec.satisfies("+jemalloc"):
            args.append("-DJEMALLOC_ROOT={0}".format(spec["jemalloc"].prefix))

        if spec.satisfies("+hip"):
            args.append("-DROCM_ROOT={0}".format(spec["hip"].prefix))
            args.append("-DROCTRACER_ROOT={0}".format(spec["roctracer-dev"].prefix))
            args.append("-DROCTX_ROOT={0}".format(spec["roctracer-dev"].prefix))
            args.append("-DRSMI_ROOT={0}".format(spec["rocm-smi-lib"].prefix))

        return args
