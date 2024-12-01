# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class P4est(AutotoolsPackage):
    """Dynamic management of a collection (a forest) of adaptive octrees in
    parallel"""

    homepage = "https://www.p4est.org"

    # Only use the official tarball releases provided on p4est.org or
    # p4est.github.io. The automatically generated releases from the
    # Github repository lack important parts.
    url = "https://p4est.github.io/release/p4est-2.8.tar.gz"

    maintainers("davydden")

    license("GPL-2.0-only")

    version("2.8", sha256="6a0586e3abac06c20e31b1018f3a82a564a6a0d9ff6b7f6c772a9e6b0f0cc5e4")
    version("2.3.2", sha256="076df9e5578e0e7fcfbe12e1a0b080104001f8c986ab1d5a69ec2220050df8e6")
    version("2.3.1", sha256="be66893b039fb3f27aca3d5d00acff42c67bfad5aa09cea9253cdd628b2bdc9a")
    version("2.2", sha256="1549cbeba29bee2c35e7cc50a90a04961da5f23b6eada9c8047f511b90a8e438")
    version("2.1", sha256="07ab24bd63a652a30576fbca12c0fc068dffa615d888802d7f229fa994a9c1ef")
    version("2.0", sha256="c522c5b69896aab39aa5a81399372a19a6b03fc6200d2d5d677d9a22fe31029a")
    version("1.1", sha256="0b5327a35f0c869bf920b8cab5f20caa4eb55692eaaf1f451d5de30285b25139")

    depends_on("c", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI")
    variant("openmp", default=False, description="Enable OpenMP")

    # build dependencies
    depends_on("automake", when="@2.0", type="build")
    depends_on("autoconf", when="@2.0", type="build")
    depends_on("libtool@2.4.2:", type="build")

    # other dependencies
    depends_on("mpi", when="+mpi")
    depends_on("zlib-api")

    # from sc upstream, correct the default libraries
    patch(
        "https://github.com/cburstedde/libsc/commit/b506aab224b988fec210cc212469f2c4f58b2d04.patch?full_index=1",
        sha256="e03437c5b580deacdfa0e8112d0a3d40af1f5e4757fe1dd00347d0523f6c16d5",
        working_dir="sc",
        when="@2.0",
    )
    patch(
        "https://github.com/cburstedde/libsc/commit/b45a51a7ef97883a3d4dcbd05cb2c77890a76f75.patch?full_index=1",
        sha256="f5c9f784408481b12babd802cc3bedde2a8c4f84de4fd58c54017690b7520a01",
        working_dir="sc",
        when="@2.0",
    )

    def autoreconf(self, spec, prefix):
        if self.spec.satisfies("@2.0"):
            bootstrap = Executable("./bootstrap")
            bootstrap()

    def configure_args(self):
        args = [
            "--enable-shared",
            "--disable-vtk-binary",
            "--without-blas",
            "CPPFLAGS=-DSC_LOG_PRIORITY=SC_LP_ESSENTIAL",
            "CFLAGS=-O2",
        ]

        if "~mpi" in self.spec:
            args.append("--disable-mpi")
        else:
            args.append("--enable-mpi")
            args.append("CC=%s" % self.spec["mpi"].mpicc)
            args.append("CXX=%s" % self.spec["mpi"].mpicxx)
            args.append("FC=%s" % self.spec["mpi"].mpifc)
            args.append("F77=%s" % self.spec["mpi"].mpif77)

        if "+openmp" in self.spec:
            try:
                args.append("--enable-openmp={0}".format(self.compiler.openmp_flag))
            except UnsupportedCompilerFlag:
                args.append("--enable-openmp")
        else:
            args.append("--disable-openmp")

        return args
