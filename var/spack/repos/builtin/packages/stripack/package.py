# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stripack(MakefilePackage):
    """STRIPACK:
    Delaunay Triangulation rewritten in Fortran 90 by John Burkardt at
    https://people.sc.fsu.edu/~jburkardt/f_src/stripack/stripack.html

    The original Fortran 77 package STRIPACK is available from netlib as algorithm number 772 at
    https://www.netlib.org/toms/772.gz
    Dr. Renka's articles were published in the ACM Transactions on Mathematical Software, Vol. 23, No 3, September 1997
    https://dl.acm.org/doi/10.1145/275323.275329
    """

    homepage = "https://people.sc.fsu.edu/~jburkardt/f_src/stripack/stripack.html"

    maintainers("cessenat")

    license("MIT")

    version(
        "develop",
        sha256="26c074bc46fb8549d7a42ec713636798297d7327c8f3ce0ba2d3348a501ffa7c",
        expand=False,
        url="https://people.sc.fsu.edu/~jburkardt/f_src/stripack/stripack.f90",
    )

    @run_before("build")
    def run_mkmake(self):
        config = [
            "BUILDIR ?= " + join_path(self.build_directory, "build"),
            "DYLIB=" + dso_suffix,
            "F90=" + self.compiler.fc,
            "LD=" + self.compiler.fc,
            "FFLAGS=" + self.compiler.fc_pic_flag,
            "LDFLAGS=" + self.compiler.fc_pic_flag,
            ".SUFFIXES: .f .f90 .F90",
            "$(BUILDIR)/%.o: %.f90",
            "\t$(F90) $(FFLAGS) -c $< -o $@",
            "all: $(BUILDIR)/stripack.o",
            "\t$(LD) -shared $(LDFLAGS) -o $(BUILDIR)/libstripack.$(DYLIB)"
            + " $(BUILDIR)/stripack.o $(LIBS)",
        ]
        with open("Makefile", "w") as fh:
            fh.write("\n".join(config))
        mkdirp(join_path(self.build_directory, "build"))

    def setup_run_environment(self, env):
        # This is smartly used by VisIt
        env.set(
            "VISIT_FFP_STRIPACK_PATH", join_path(self.spec.prefix.lib, "libstripack." + dso_suffix)
        )

    def build(self, spec, prefix):
        fflags = spec.compiler_flags["fflags"]
        # Setting the double precision mode
        # needed for the original Fortran 77 version
        satisfies = spec.satisfies
        if satisfies("%gcc") or satisfies("%clang") or satisfies("%flang"):
            fflags += ["-fdefault-real-8", "-fdefault-double-8"]
        elif satisfies("%intel") or satisfies("%oneapi") or satisfies("%aocc"):
            fflags += ["-r8"]
        elif satisfies("%xl") or satisfies("%xl_r"):
            fflags += ["-qrealsize=8"]
        elif satisfies("%fj"):
            fflags += ["-CcdRR8"]
        elif satisfies("%nvhpc"):
            fflags += ["-r8"]
        fflags += [self.compiler.fc_pic_flag]
        make("all", "FFLAGS={0}".format(" ".join(fflags)))

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        install(join_path(self.build_directory, "build", "libstripack." + dso_suffix), prefix.lib)
