# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sprng(AutotoolsPackage):
    """SPRNG: A Scalable Library For Pseudorandom Number Generation
    Sprng is a distributed process-aware random number generator that
    avoids correlations in random number sequences across processes.
    """

    maintainers("kayarre")

    homepage = "http://www.sprng.org"
    url = "http://www.sprng.org/Version5.0/sprng5.tar.bz2"

    license("GPL-2.0-only")

    version("5.0", sha256="9172a495472cc24893e7489ce9b5654300dc60cba4430e436ce50d28eb749a66")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI support")
    variant("fortran", default=False, description="Enable Fortran support")

    depends_on("mpi", when="+mpi")

    def url_for_version(self, version):
        url = "http://www.sprng.org/Version{0}/sprng{1}.tar.bz2"
        return url.format(version, version.up_to(1))

    def configure_args(self):
        configure_args = []
        configure_args += self.with_or_without("mpi")
        configure_args += self.with_or_without("fortran")

        if "+mpi" in self.spec:
            mpi_link_flags = self.spec["mpi:cxx"].libs.link_flags
            configure_args.append("LIBS={0}".format(mpi_link_flags))
            configure_args.append("CC={0}".format(self.spec["mpi"].mpicc))
            configure_args.append("CXX={0}".format(self.spec["mpi"].mpicxx))
            if "+fortran" in self.spec:
                configure_args.append("FC={0}".format(self.spec["mpi"].mpifc))
        return configure_args

    # TODO: update after solution for virtual depedencies
    @run_before("configure")
    def mpicxx_check(self):
        # print(self.spec['mpi:fortran'].libs.names)
        if "+mpi" in self.spec:
            if "mpi_cxx" not in self.spec["mpi:cxx"].libs.names:
                msg = "SPRNG requires a mpi Cxx bindings to build"
                raise RuntimeError(msg)
            if "+fortran" in self.spec:
                if "fmpi" not in self.spec["fortran"].libs.names:
                    msg = "SPRNG requires fortran mpi " "libraries with mpi enabled"
                    raise RuntimeError(msg)
        # raise RuntimeError("test")

    # FIXME: update after features in #15702 are enabled
    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        def listisclose(a, b, rel_tol=1e-09, abs_tol=1.0e-20):
            for ai, bi in zip(a, b):
                if not abs(ai - bi) <= max(rel_tol * max(abs(ai), abs(bi)), abs_tol):
                    return False
            return True

        # Build and run a small program to test the installed sprng library
        spec = self.spec
        print("Checking sprng installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <cstdio>
#define SIMPLE_SPRNG   /* simple interface                        */
#include "sprng_cpp.h" /* SPRNG header file                       */

#define SEED 985456376

int main() {
  int seed = SEED;
  int i, j;
  double rn;
  for(j=0; j < 5; ++j) {
    init_sprng(seed, SPRNG_DEFAULT, j);
    for (i=0; i<3; ++i) {
        rn = sprng();
        printf("%f ", rn);
    }
  }
  printf("\n");
  return 0;
}
"""
            expected = [
                0.504272,
                0.558437,
                0.000848,
                0.707488,
                0.664048,
                0.005616,
                0.060190,
                0.415195,
                0.933915,
                0.085215,
                0.456461,
                0.244497,
                0.626037,
                0.917948,
                0.135160,
            ]
            with open("check.c", "w") as f:
                f.write(source)
            if "+mpi" in spec:
                cc = Executable(spec["mpi"].mpicxx)
            else:
                cc = Executable(self.compiler.cxx)
            cc(*(["-c", "check.c"] + spec["sprng"].headers.cpp_flags.split()))
            cc(*(["-o", "check", "check.o"] + spec["sprng"].libs.ld_flags.split()))
            try:
                check = Executable("./check")
                output = check(output=str)
            except ProcessError:
                output = ""
            out2float = [float(num) for num in output.split(" ")]

            success = listisclose(expected, out2float)
            if not success:
                print("Produced output does not match expected output.")
                print("Expected output:")
                print("-" * 80)
                print(expected)
                print("-" * 80)
                print("Produced output:")
                print("-" * 80)
                print(output)
                print("-" * 80)
                raise RuntimeError("sprng install check failed")
            else:
                print("test passed")
        shutil.rmtree(checkdir)
