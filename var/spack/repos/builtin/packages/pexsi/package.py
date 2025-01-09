# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


class Pexsi(MakefilePackage, CMakePackage):
    """The PEXSI library is written in C++, and uses message passing interface
    (MPI) to parallelize the computation on distributed memory computing
    systems and achieve scalability on more than 10,000 processors.

    The Pole EXpansion and Selected Inversion (PEXSI) method is a fast
    method for electronic structure calculation based on Kohn-Sham density
    functional theory. It efficiently evaluates certain selected elements
    of matrix functions, e.g., the Fermi-Dirac function of the KS Hamiltonian,
    which yields a density matrix. It can be used as an alternative to
    diagonalization methods for obtaining the density, energy and forces
    in electronic structure calculations.
    """

    homepage = "https://math.berkeley.edu/~linlin/pexsi/index.html"

    build_system(
        conditional("cmake", when="@1:"), conditional("makefile", when="@0"), default="cmake"
    )

    license("BSD-3-Clause-LBNL")

    version("2.0.0", sha256="c5c83c2931b2bd0c68a462a49eeec983e78b5aaa1f17dd0454de4e27b91ca11f")
    version("1.2.0", sha256="8bfad6ec6866c6a29e1cc87fb1c17a39809795e79ede98373c8ba9a3aaf820dd")
    version("0.10.2", sha256="8714c71b76542e096211b537a9cb1ffb2c28f53eea4f5a92f94cc1ca1e7b499f")
    version("0.9.0", sha256="e5efe0c129013392cdac3234e37f1f4fea641c139b1fbea47618b4b839d05029")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    patch("fujitsu-add-link-flags.patch", when="%fj")

    depends_on("parmetis")
    depends_on("superlu-dist@5.1.2:5.3", when="@0.10.2:0")
    depends_on("superlu-dist@:6.1.0", when="@1")  # Upper limit from CP2K toolchain
    depends_on("superlu-dist@7", when="@2")

    with when("build_system=cmake"):
        depends_on("cmake@3.10:", type="build")
        depends_on("cmake@3.17:", type="build", when="@2:")

    variant("openmp", default=False, description="Build with OpenMP support", when="@1.2")
    variant("fortran", default=False, description="Builds the Fortran interface")

    def url_for_version(self, version):
        if version == Version("0"):
            return f"https://math.berkeley.edu/~linlin/pexsi/download/pexsi_v{version}.tar.gz"

        return f"https://bitbucket.org/berkeleylab/pexsi/downloads/pexsi_v{version}.tar.gz"


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    parallel = False

    def edit(self, pkg, spec, prefix):
        substitutions = [
            ("@MPICC", spec["mpi"].mpicc),
            ("@MPICXX_LIB", spec["mpi:cxx"].libs.joined()),
            ("@MPICXX", spec["mpi"].mpicxx),
            ("@MPIFC", spec["mpi"].mpifc),
            ("@RANLIB", "ranlib"),
            ("@PEXSI_STAGE", pkg.stage.source_path),
            ("@SUPERLU_PREFIX", spec["superlu-dist"].prefix),
            ("@METIS_PREFIX", spec["metis"].prefix),
            ("@PARMETIS_PREFIX", spec["parmetis"].prefix),
            ("@LAPACK_PREFIX", spec["lapack"].prefix),
            ("@BLAS_PREFIX", spec["blas"].prefix),
            ("@LAPACK_LIBS", spec["lapack"].libs.joined()),
            ("@BLAS_LIBS", spec["blas"].libs.joined()),
            # FIXME : what to do with compiler provided libraries ?
            ("@STDCXX_LIB", " ".join(pkg.compiler.stdcxx_libs)),
        ]

        fldflags = ""
        if "@0.9.2" in spec:
            fldflags += " -Wl,--allow-multiple-definition"

        if "^superlu +openmp" in spec or "^openblas threads=openmp" in spec:
            fldflags += " " + pkg.compiler.openmp_flag

        substitutions.append(("@FLDFLAGS", fldflags.lstrip()))

        template = join_path(os.path.dirname(__file__), "make.inc")
        makefile = join_path(pkg.stage.source_path, "make.inc")
        copy(template, makefile)
        for key, value in substitutions:
            filter_file(key, value, makefile)

    def build(self, pkg, spec, prefix):
        super().build(pkg, spec, prefix)
        if "+fortran" in spec:
            make("-C", "fortran")

    def install(self, pkg, spec, prefix):
        # 'make install' does not exist, despite what documentation says
        mkdirp(pkg.prefix.lib)

        install(
            join_path(pkg.stage.source_path, "src", "libpexsi_linux.a"),
            join_path(pkg.prefix.lib, "libpexsi.a"),
        )

        install_tree(join_path(pkg.stage.source_path, "include"), pkg.prefix.include)

        # fortran "interface"
        if "+fortran" in spec:
            install_tree(
                join_path(pkg.stage.source_path, "fortran"), join_path(pkg.prefix, "fortran")
            )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define_from_variant("PEXSI_ENABLE_FORTRAN", "fortran"),
            self.define_from_variant("PEXSI_ENABLE_OPENMP ", "openmp"),
        ]

        if self.spec.satisfies("%fj"):
            args.append(self.define("BLAS_LIBRARIES", self.spec["blas"].libs.link_flags))

        return args
