# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SstMacro(AutotoolsPackage):
    """The Structural Simulation Toolkit Macroscale Element Library simulates
    large-scale parallel computer architectures for the coarse-grained study
    of distributed-memory applications. The simulator is driven from either a
    trace file or skeleton application. SST/macro's modular architecture can
    be extended with additional network models, trace file formats, software
    services, and processor models.
    """

    homepage = "https://github.com/sstsimulator"
    git = "https://github.com/sstsimulator/sst-macro.git"
    url = "https://github.com/sstsimulator/sst-macro/releases/download/v14.1.0_Final/sstmacro-14.1.0.tar.gz"

    maintainers("berquist")

    version("14.1.0", sha256="241f42f5c460b0e7462592a7f412bda9c9de19ad7a4b62c22f35be4093b57014")
    version("14.0.0", sha256="3962942268dd9fe6ebd4462e2d6d305ab757f3f510487e84687146a8d461be13")
    version("13.1.0", sha256="022e39daae1067b56c0011dbe87e3234fee4587049fd53671e1ed6b23233f70e")
    version("13.0.0", sha256="410dad4ac0c7a4c0e16c54da308b6c6b631112af18ae2c37585c8a14472987d4")
    version("12.1.0", sha256="ee57e08acfd4b6429a0500d981d468ee6ded2638ec5abec7b47f172388b267f1")
    version("12.0.1", sha256="1491a149f4554777a6c3aa62730b3cd1a24c43a8d3d7fb61edfb4fe5c773aed8")
    version("12.0.0", sha256="259237a47cf341830ce3956cfadfd6e77ff1824da05da4a7b212fc5867ce64b2")
    version("11.1.0", sha256="4b1226e75e2e99faa42b218461d85e8e17c1d4f333dd973e72a5dc052328d34c")
    version("11.0.0", sha256="30367baed670b5b501320a068671556c9071286a0f0c478f9994a30d8fe5bdea")
    version("10.1.0", sha256="e15d99ce58d282fdff849af6de267746a4c89f3b8c5ab6c1e1e7b53a01127e73")
    version("10.0.0", sha256="064b732256f3bec9b553e00bcbc9a1d82172ec194f2b69c8797f585200b12566")
    version("9.1.0", sha256="ef735440c7297212e11ccf0559b028108562880ec55e81f57ebd0df68aa4b9f1")
    version("9.0.0", sha256="b582118afd379bb17b3fcf938d814c691d0941a70bf8c8685272556aef3b956d")
    version("8.0.0", sha256="8618a259e98ede9a1a2ce854edd4930628c7c5a770c3915858fa840556c1861f")
    version("7.2.0", sha256="df19a4ff5c5d35cfca2d8c37440525d8836cde4c0a45ae44f1a888550ae42bff")
    version("7.1.0", sha256="4bf154142f06ab8c15d9d95065fcd96581594b124ba50f86ce7ab60f366ac285")
    version("7.0.0", sha256="9c17fa43c48bf9cd669f6ef6ae6fb87257793c918433424f250eac862bfb4cc4")
    version("6.1.0", sha256="930b67313b594148d6356e550ca370214a9283858235321d3ef974191eb028d6")
    version("6.0.0", sha256="7b475a73ba69550ca3800ad96e58ce0e35fabf909896a3764f892743ef8e50d1")

    version("master", branch="master")
    version("develop", branch="devel")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    for version_name in ("master", "develop"):
        depends_on("autoconf@1.68:", type="build", when="@{}".format(version_name))
        depends_on("automake@1.11.1:", type="build", when="@{}".format(version_name))
        depends_on("libtool@1.2.4:", type="build", when="@{}".format(version_name))
        depends_on("m4", type="build", when="@{}".format(version_name))

    depends_on("binutils", type="build")
    depends_on("zlib-api", type=("build", "link"))
    depends_on("otf2", when="+otf2")
    depends_on("llvm+clang@5:9", when="+skeletonizer")
    depends_on("mpi", when="+pdes_mpi")
    # Allow mismatch between core dependency version and current macro version.
    depends_on("sst-core", when="+core")
    depends_on("gettext")

    variant("pdes_threads", default=True, description="Enable thread-parallel PDES simulation")
    variant("pdes_mpi", default=False, description="Enable distributed PDES simulation")
    variant("core", default=False, description="Use SST Core for PDES")
    variant("otf2", default=False, description="Enable OTF2 trace emission and replay support")
    variant(
        "skeletonizer",
        default=False,
        description="Enable Clang source-to-source autoskeletonization",
    )

    variant("static", default=True, description="Build static libraries")
    variant("shared", default=True, description="Build shared libraries")

    variant("werror", default=False, description="Build with all warnings as errors")
    variant("warnings", default=False, description="Build with all possible warnings")

    # force out-of-source builds
    build_directory = "spack-build"

    @when("@develop,master")
    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap.sh")

    def configure_args(self):
        args = ["--disable-regex"]

        spec = self.spec
        args.append("--enable-static=%s" % ("yes" if "+static" in spec else "no"))
        args.append("--enable-shared=%s" % ("yes" if "+shared" in spec else "no"))

        if spec.satisfies("@8.0.0:"):
            args.extend(
                [
                    "--%sable-otf2" % ("en" if "+otf2" in spec else "dis"),
                    "--%sable-multithread" % ("en" if "+pdes_threads" in spec else "dis"),
                ]
            )

            if "+skeletonizer" in spec:
                args.append("--with-clang=" + spec["llvm"].prefix)

        if spec.satisfies("@10:"):
            if "+warnings" in spec:
                args.append("--with-warnings")
            if "+werror" in spec:
                args.append("--with-werror")

        if "+core" in spec:
            args.append("--with-sst-core=%s" % spec["sst-core"].prefix)

        # Optional MPI support
        need_core_mpi = False
        if "+core" in spec:
            if "+pdes_mpi" in spec["sst-core"]:
                need_core_mpi = True
        if "+pdes_mpi" in spec or need_core_mpi:
            env["CC"] = spec["mpi"].mpicc
            env["CXX"] = spec["mpi"].mpicxx
            env["F77"] = spec["mpi"].mpif77
            env["FC"] = spec["mpi"].mpifc

        return args
