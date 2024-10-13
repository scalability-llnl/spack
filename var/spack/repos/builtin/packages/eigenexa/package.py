# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Eigenexa(AutotoolsPackage):
    """EigenExa is a high-performance eigenvalue solver."""

    homepage = "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/eigenexa/"

    version("2.12", sha256="2a33999b09d4434a5ce2fbd18cabbfee1cff0b2a12df7ded1f67127157b08f86")
    version("2.11", sha256="87dee8ac13f410a007e82df2688fa7f143883229dac729fd20836f4a28fac43d")
    version("2.10", sha256="5b1806e132b191d23680b34fbc286d676ba20f58ee754122087a3ec3cacb8fa3")
    version("2.9", sha256="8788922035bf67abf1a7aecf8e30dd7564de387fda4ecd11c6b4cf9259d25990")
    version("2.8", sha256="3ee846d4db10336d393738eadab2f1c941dfc8fb501f2a4baf0823f0ff938f56")
    version("2.7", sha256="490f3d0217a8c101e66e785229baaba5b4d674508bc9a5aca6cc5fa074f3a8aa")
    version(
        "2.6",
        sha256="a1a4e571a8051443f28e7ea4889272993452a4babd036d2b4dd6b28154302f95",
        url="https://www.r-ccs.riken.jp/labs/lpnctrt/projects/eigenexa/EigenExa-2.6.tgz",
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mpi")
    depends_on("lapack")
    depends_on("scalapack")

    patch("fj_compiler.patch", when="%fj")
    patch("gcc_compiler.patch", when="@:2.6.99 %gcc")

    parallel = False
    force_autoreconf = True

    def url_for_version(self, version):
        return "https://www.r-ccs.riken.jp/labs/lpnctrt/projects/eigenexa/EigenExa-{0}.{1}".format(
            version, "tar.gz" if version >= Version("2.7") else ".tgz"
        )

    def setup_build_environment(self, env):
        env.set("FC", self.spec["mpi"].mpifc, force=True)
        env.set("F77", self.spec["mpi"].mpif77, force=True)
        env.set("CC", self.spec["mpi"].mpicc, force=True)
        env.set(
            "LAPACK_LIBS",
            "{0} {1}".format(
                self.spec["lapack"].libs.ld_flags, self.spec["scalapack"].libs.ld_flags
            ),
        )
        env.set(
            "LAPACK_PATH",
            "{0}".format(
                ":".join(
                    self.spec["lapack"].libs.directories + self.spec["scalapack"].libs.directories
                )
            ),
        )

        if self.spec.satisfies("%gcc@10:"):
            fflags = "-fallow-argument-mismatch"
            if self.spec.satisfies("@:2.8"):
                fflags += " -fallow-invalid-boz"
            env.set("FCFLAGS", fflags)
            env.set("FFLAGS", fflags)

    @run_after("install")
    def cache_test_sources(self):
        """Save off benchmark files for stand-alone tests."""
        cache_extra_test_sources(self, "benchmark")

    def test_benchmarks(self):
        """run benchmark checks"""
        # NOTE: This package would ideally build the test program using
        #   the installed software *each* time the tests are run since
        #   this package installs a library.

        test_cache_dir = join_path(self.test_suite.current_test_cache_dir, "benchmark")
        test_data_dir = self.test_suite.current_test_data_dir

        with working_dir(test_data_dir):
            opts = [
                "run-test.sh",
                self.spec["mpi"].prefix.bin.mpirun,
                "-n",
                "1",
                join_path(test_cache_dir, "eigenexa_benchmark"),
                "-f",
                join_path(test_cache_dir, "IN"),
            ]
            env["OMP_NUM_THREADS"] = "1"
            sh = which("sh")
            out = sh(*opts, output=str.split, error=str.split)
            assert "EigenExa Test Passed !" in out
