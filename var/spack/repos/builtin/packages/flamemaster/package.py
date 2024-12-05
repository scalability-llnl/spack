# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from os.path import join as pjoin

from spack.package import *


class Flamemaster(CMakePackage):
    """
    FlameMaster is an open source C++ program package for 0D combustion
    and 1D laminar flame calculations. FlameMaster is written by Heinz Pitsch.
    """

    homepage = "https://www.itv.rwth-aachen.de/downloads/flamemaster/"
    url = "file://{0}/flamemaster-4.3.1.tar.gz".format(os.getcwd())
    manual_download = True

    maintainers("amd-toolchain-support")

    version("4.3.1", sha256="8ff382f098e44a7978fe1bcc688272d65f0b374487af4523d94cca983dc57378")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("None", "Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant(
        "bilin_omega",
        default=True,
        description="Compile with bilinear interpolation" "for collision integrals (omega)",
    )
    variant(
        "combustion",
        default=False,
        description="Integrate comustion libraries" "for kinetics, thermodynamics, and transport",
    )
    variant(
        "fortran_code",
        default=False,
        description="Compile optional fortran code like dassl, the adiabatic"
        "flame temperature module, and a mechanism converter tool",
    )
    variant("scanmannew", default=False, description="Compile the new ScanMan")
    variant(
        "dco_chunk_tape", default=False, description="Dynamically allocate memory for the dco tape"
    )
    variant(
        "troe",
        default=False,
        description="FlameMaster mechanism format allows for specifying"
        "an additional parameter. This option disables the use of the"
        "paramter which is currently required to run adjoint sensitivity analysis.",
    )
    variant("jl_debug", default=False, description="Debug mode during development(Johannes Lotz)")
    variant(
        "flux_bc",
        default=False,
        description="Specify boundary conditions as velocity [m/s]"
        "or massflux in Counterflow (Physical Coord.)",
    )
    variant("full_diffusion", default=False, description="Compile with multi-component diffusion")
    variant("intel_prof", default=False, description="Enable -prof-gen and -prof-use")
    variant("soot_lib", default=False, description="Soot library with moment equation solving")
    variant(
        "newton_perf",
        default=False,
        description="Compile with time measurement of each Newton step",
    )
    variant("optima", default=False, description="Include code for Optima++ features")
    variant("opt_reaction_rates", default=True, description="Fast computation of reaction rates.")
    variant(
        "prem_upwind_convec",
        default=True,
        description="Use upwind scheme for the convective term.",
    )
    variant(
        "sundials_hint",
        default=False,
        description="No hints on how FlameMaster can install sundials.",
    )
    variant("simd_kinetics", default=False, description="WITH SIMD_KINETICS")
    variant(
        "solve_mom_log",
        default=False,
        description="Solve the soot Moments equation with logarithms",
    )
    variant(
        "solve_with_z",
        default=True,
        description="Counter flow diffusion flame implementation includes"
        "a solution of the mixture fraction equation",
    )
    variant("sundials_lapack", default=False, description="Link LAPACK in sundials")
    variant(
        "sundials_no_idas_search",
        default=False,
        description="Do not search for IDAS (part of sundials).",
    )
    variant(
        "sundials_use_static_lib",
        default=True,
        description="Use static linking for sundials libraries",
    )
    variant("sundials_diagnos", default=False, description="Only for troubleshooting")
    variant(
        "tests",
        default=False,
        description="Install google-test framework for unit tests" "and enable units tests.",
    )
    variant(
        "third_party_in_build_dir",
        default=True,
        description="Compile third party libraries and tools in build diretory",
    )
    variant("local_lewis", default=False, description="Write Lewis numbers at every grid point")
    variant(
        "flamemaster_prefix",
        default=True,
        description="Used to modify the installation directories",
    )
    variant("openmp", default=True, description="Build with OpenMP")
    variant("eigen", default=False, description="Build with Eigen Integration")
    variant("eglib", default=False, description="Build with EG lib")
    variant("sundials", default=True, description="with sundials")

    depends_on("blas")
    depends_on("lapack")
    depends_on("cmake@3.12", type="build")
    depends_on("bison")
    depends_on("flex")

    root_cmakelists_dir = "Repository"

    def setup_build_environment(self, env):
        env.set("LAPACK_HOME", self.spec["lapack"].prefix)
        env.set("BLIS_HOME", self.spec["blas"].prefix)

        if self.spec.satisfies("%aocc"):
            env.append_flags(
                "LDFLAGS",
                "-L{0} -lalm -lm -lstdc++".format(
                    pjoin(os.path.dirname(os.path.dirname(self.compiler.cxx)), "lib")
                ),
            )

    def cmake_args(self):
        spec = self.spec

        args = ["-DCMAKE_C_COMPILER=%s" % spack_cc, "-DCMAKE_CXX_COMPILER=%s" % spack_cxx]

        if spec.variants["build_type"].value == "Release":
            cxx_flags_release = []
            c_flags_release = []
            fortran_flags_release = []
            if self.spec.satisfies("%aocc") or self.spec.satisfies("%gcc"):
                cxx_flags_release.extend(["-Ofast", "-ffast-math"])
                c_flags_release.extend(["-Ofast", "-ffast-math"])
                fortran_flags_release.extend(["-Ofast"])
            args.extend(
                [
                    self.define("CMAKE_CXX_FLAGS_RELEASE", " ".join(cxx_flags_release)),
                    self.define("CMAKE_C_FLAGS_RELEASE", " ".join(c_flags_release)),
                    self.define("CMAKE_Fortran_FLAGS_RELEASE", " ".join(fortran_flags_release)),
                ]
            )
            if self.spec.satisfies("%icc"):
                cxxflags = "-Ofast -ffast-math -DNDEBUG -march=native\
                        -mtune=native -funroll-all-loops\
                        -qopt-multi-version-aggressive -ipo -parallel"
                cflags = "-Ofast -ffast-math -DNDEBUG -march=native\
                        -mtune=native -funroll-all-loops -ipo -parallel"
                fcflags = "-Ofast -march=native -mtune=native -ipo -parallel"
                args.extend(
                    [
                        "-DCMAKE_CXX_FLAGS_RELEASE=%s" % cxxflags,
                        "-DCMAKE_C_FLAGS_RELEASE=%s" % cflags,
                        "-DCMAKE_Fortran_FLAGS_RELEASE=%s" % fcflags,
                    ]
                )

        if self.spec.satisfies("%aocc"):
            OpenMP_CXX_FLAGS = "-fopenmp=libomp"
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            args.extend(
                [
                    "-DOpenMP_CXX_FLAGS=%s" % OpenMP_CXX_FLAGS,
                    "-DOpenMP_C_FLAGS=%s" % OpenMP_CXX_FLAGS,
                    "-DOpenMP_C_LIB_NAMES=libomp",
                    "-DOpenMP_CXX_LIB_NAMES=libomp",
                    "-DOpenMP_libomp_LIBRARY={0}/lib/libomp.so".format(clang_root),
                ]
            )

        args.append(self.define_from_variant("BILIN_OMEGA", "bilin_omega"))
        args.append(self.define_from_variant("COMBUSTION_LIBS", "combustion"))
        args.append(self.define_from_variant("COMPILE_FORTRAN_SRC", "fortran_code"))
        args.append(self.define_from_variant("COMPILE_SCANMANNEW", "scanmannew"))
        args.append(self.define_from_variant("DCO_CHUNK_TAPE", "dco_chunk_tape"))
        args.append(self.define_from_variant("CHEMKIN_TROE", "troe"))
        args.append(self.define_from_variant("JL_DEBUG", "jl_debug"))
        args.append(self.define_from_variant("FLUX_BC_COUNTERFLOW", "flux_bc"))
        args.append(self.define_from_variant("FULL_DIFFUSION", "full_diffusion"))
        args.append(self.define_from_variant("ITV_SOOT_LIB", "soot_lib"))
        args.append(self.define_from_variant("NEWTON_PERFORMANCE", "newton_perf"))
        args.append(self.define_from_variant("OPTIMAPP", "optima"))
        args.append(self.define_from_variant("OPT_REACTION_RATES", "opt_reaction_rates"))
        args.append(self.define_from_variant("PREM_UPWIND_CONVEC", "prem_upwind_convec"))
        args.append(self.define_from_variant("SILENCE_SUNDIALS_HINT", "sundials_hint"))
        args.append(self.define_from_variant("SIMD_KINETICS", "simd_kinetics"))
        args.append(self.define_from_variant("SOLVE_MOM_LOG", "solve_mom_log"))
        args.append(self.define_from_variant("SOLVE_WITH_Z", "solve_with_z"))
        args.append(self.define_from_variant("SUNDIALS_LAPACK", "sundials_lapack"))
        args.append(self.define_from_variant("SUNDIALS_NO_IDAS_SEARCH", "sundials_no_idas_search"))
        args.append(
            self.define_from_variant("SUNDIALS_USE_STATIC_LIBRARIES", "sundials_use_static_lib")
        )
        args.append(self.define_from_variant("TESTS", "tests"))
        args.append(
            self.define_from_variant("THIRD_PARTY_IN_BUILD_DIR", "third_party_in_build_dir")
        )
        args.append(self.define_from_variant("WRITE_LOCAL_LEWIS", "local_lewis"))
        args.append(self.define_from_variant("USE_FLAMEMASTER_PREFIX", "flamemaster_prefix"))
        args.append(self.define_from_variant("WITH_EG", "eglib"))
        args.append(self.define_from_variant("INSTALL_SUNDIALS", "sundials"))
        args.append("-DINTEL_PROF_GEN:BOOL=%s" % ("ON" if "+intel_prof" in spec else "OFF"))
        args.append("-DINTEL_PROF_USE:BOOL=%s" % ("ON" if "+intel_prof" in spec else "OFF"))
        args.append(
            "-DSUNDI_DIAGNOS_SEARCH_HEADER_FILES:BOOL=%s"
            % ("ON" if "+sundials_diagnos" in spec else "OFF")
        )
        args.append(
            "-DSUNDI_DIAGNOS_SEARCH_LIB_FILES:BOOL=%s"
            % ("ON" if "+sundials_diagnos" in spec else "OFF")
        )
        args.append("-DEIGEN_INTEGRATION:BOOL=%s" % ("ON" if "+eigen" in spec else "OFF"))
        args.append("-DINSTALL_EIGEN:BOOL=%s" % ("ON" if "+eigen" in spec else "OFF"))

        if spec.satisfies("[virtuals=lapack] ^amdlibflame"):
            args.append("-DBLA_VENDOR=FLAME")

        args.append("-DFLAMEMASTER_INSTALL_PREFIX:PATH={0}".format(spec.prefix))

        return args
