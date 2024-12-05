# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fstrack(MakefilePackage):
    """Package with tools to analyze symmetry components of elastic tensors,
    predict synthetic waveforms and compute automated shear wave splitting
    along ray paths, and to track finite strain and predict LPO from mantle
    flow given on GMT/netcdf grds."""

    homepage = "http://www-udc.ig.utexas.edu/external/becker/data.html#fstrack"
    url = "http://www-udc.ig.utexas.edu/external/becker/software/fstrack-0.5.3.092918.tgz"

    license("Unlicense")

    version(
        "0.5.3.092918", sha256="34b31687fdfa207b9659425238b805eaacf0b0209e7e3343c1a3cb4c9e62345d"
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("flow", default=True, description="Build the flow tracker")

    depends_on("gmt@4.0:4", when="+flow")
    depends_on("netcdf-c", when="+flow")

    parallel = False

    def setup_build_environment(self, env):
        # Compilers
        env.set("F90", spack_fc)

        # Compiler flags (assumes GCC)
        env.set("CFLAGS", "-O2")
        env.set("FFLAGS", "-ffixed-line-length-132 -x f77-cpp-input -O2")
        env.set("FFLAGS_DEBUG", "-g -x f77-cpp-input")
        env.set("F90FLAGS", "-O2 -x f95-cpp-input")
        env.set("F90FLAGS_DEBUG", "-g -x f95-cpp-input")
        env.set("LDFLAGS", "-lm")

        if self.spec.satisfies("+flow"):
            env.set("GMTHOME", self.spec["gmt"].prefix)
            env.set("NETCDFDIR", self.spec["netcdf-c"].prefix)

    def build(self, spec, prefix):
        with working_dir("eispack"):
            make()

        with working_dir("d-rex"):
            make()

        with working_dir("fstrack"):
            if spec.satisfies("+flow"):
                make("really_all")
            else:
                make()
