# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Starpu(AutotoolsPackage):
    """StarPU runtime system

    StarPU is a runtime support for scheduling applications written as
    task graphs on heterogeneous multi-core architectures. Tasks may
    define several implementations, for different architectures (e.g
    one implementation for CPUs, and one implementation for CUDA).
    StarPU takes care of scheduling and executing those tasks as
    efficiently as possible over the entire machine. It also provides
    a high-level data management library which enforces memory
    coherency over the differents processing units of the machine, and
    over a cluster when using distributed computing. Various data
    structures are supported mainline (vectors, dense matrices,
    CSR/BCSR/COO sparse matrices, ...), but application-specific data
    structures can also be supported.
    """

    homepage = "https://starpu.gitlabpages.inria.fr/"
    url = "https://files.inria.fr/starpu/starpu-1.4.0/starpu-1.4.0.tar.gz"
    git = "https://gitlab.inria.fr/starpu/starpu.git"

    maintainers("nfurmento", "sthibaul")

    version("1.4.7", sha256="1eb3df551089153fe6e0b172ad95118434b4a81ea9eaa5a2c38725d0db53b13e")
    version("1.4.6", sha256="579f38e150ab78c9ab299649d8649a043dbf49786e54acbf3dad90c160672cc7")
    version("1.4.5", sha256="28f389b34df57a2a4e4743b40554b0f8d098ff2199e9eb8fbbe20aa377b64541")
    version("1.4.4", sha256="37f37739911451bbea063cff52779114f76bc681ea8de3a2ab65fc517d0ea112")
    version("1.4.3", sha256="848cce0a2fbaa75b104d9878da928e19b1c3bc9b978193081672ac882e63bbea")
    version("1.4.2", sha256="6c1fce80593a96d599881c1e9697a10e2072195b1c4c64a99528192b6715ddd6")
    version("1.4.1", sha256="f023aa53da245a0f43944c3a13f63b4bfdf1324f3e66bf5cd367ce51e2044925")
    version("1.4.0", sha256="5058127761a0604606a852fd6d20b07040d5fbd9f798c5383e49f336b4eeaca1")
    version("1.3.11", sha256="580c6d98d49bacd2c666504c88890335d2689b6547d97f6a088d4ab4812df36e")
    version("1.3.10", sha256="757cd9a54f53751d37364965ac36102461a85df3a50b776447ac0acc0e1e2612")
    version("1.3.9", sha256="73adf2a5d25b04023132cfb1a8d9293b356354af7d1134e876122a205128d241")
    version("1.3.8", sha256="d35a27b219af8e7973888ebbff728ec0112ae9cda88d6b79c4cc7a1399b4d052")
    version("1.3.7", sha256="1d7e01567fbd4a66b7e563626899374735e37883226afb96c8952fea1dab77c2")
    version("1.3.6", sha256="ca71bfc5e66bbef6838a81de80fe62ff1037c3bbf902f25d3812a6f63fd8091a")
    version("1.3.5", sha256="910456a44cbac798709d3d3dfa808b5730b56cb79d6e3d8af9c3723856c26eb9")
    version("1.3.3", sha256="9dee3ac5ead3fb6911ac0eb5bef6681e8b6d70be2d55e3df5f725dd1268ca942")
    version("1.3.2", sha256="6c49441bf9d91d8e707d7c4a1df6124138e8a89a55c5f9ff514843415ff7e0b8")
    version("1.3.1", sha256="84120ec1e5b8655d4778a1263ac6e82857c7287279d8e4f8df24bfffc92613ba")
    version("1.3.0", sha256="7e06841bddb4b4c7e04e87230cd76b839ef9618d6f4e8ac9b045ec1a80a631c4")
    version("1.2.8", sha256="b6666dfbc8f248d20df232f27b0edbbb0b426258eac55ec693e45373ba5a75fb")
    version("1.2.7", sha256="be301a2718d2ca24e125d0c70f98d5bb74525f5908b3d10e63fb980918b5a16f")
    version("1.2.6", sha256="eb67a7676777b6ed583722aca5a9f63145b842f390ac2f5b3cbc36fe910d964c")
    version("1.2.5", sha256="1f22eae5c9ee4cae1c8020c5a18f4e36c05c43624bd2ba1f5356a8962d2bdae9")
    version("1.2.4", sha256="4c99f41a29a5056685a086dc6e299f5bd8c79146f1f0543f1a5882ec5100a9bd")
    version("1.2.3", sha256="295d39da17ad17752c1cb91e0009fc9b3630bc4ac7db7e2e43433ec9024dc6db")
    version("1.2.2", sha256="1677990bb9aa8e574634f2407a63aa797313fcb9a0d544b7ac60df90a37e3057")
    version("1.2.1", sha256="2e0c13f9be7bf7f3c2ce73340ca773d7a0c25bf66a822e44d8fe6407a04f8d77")
    version("1.2.0", sha256="c0b09a946bcbc680dd169d75856dc759abd98685da777afccc3366998b218a75")
    version("1.1.6", sha256="c28749b8f0a1586b814cb7d49dffb0f2631dde849591e697c40ef693a8fd54d8")

    version("develop", branch="master")
    version("master", branch="master")
    version("git-1.1", branch="starpu-1.1")
    version("git-1.2", branch="starpu-1.2")
    version("git-1.3", branch="starpu-1.3")
    version("git-1.4", branch="starpu-1.4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build STARPU as a shared library")
    variant("fast", default=True, description="Disable runtime assertions")
    variant("debug", default=False, description="Enable debug symbols")
    variant("verbose", default=False, description="Enable verbose debugging")
    variant("fxt", default=False, description="Enable FxT tracing support")
    variant("mpi", default=True, description="Enable MPI support")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("opencl", default=False, description="Enable OpenCL support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant("fortran", default=False, description="Enable Fortran interface and examples")
    variant("simgrid", default=False, description="Enable SimGrid support")
    variant("simgridmc", default=False, description="Enable SimGrid model checker support")
    variant("examples", default=True, description="Enable Examples")
    variant("papi", default=False, description="Enable PAPI support", when="@master:")
    variant("blocking", default=False, description="Enable blocking drivers support")

    depends_on("pkgconfig", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("m4", type="build")
    depends_on("hwloc")
    depends_on("hwloc+cuda", when="+cuda")
    depends_on("mpi", when="+mpi~simgrid")
    depends_on("cuda", when="+cuda~simgrid")
    depends_on("fxt", when="+fxt")
    depends_on("fxt+static", when="+fxt+simgrid+mpi")
    depends_on("simgrid", when="+simgrid")
    depends_on("simgrid+smpi", when="+simgrid+mpi")
    depends_on("simgrid+mc", when="+simgridmc")
    depends_on("papi", when="+papi")

    conflicts(
        "+shared", when="+mpi+simgrid", msg="Simgrid MPI cannot be built with a shared library"
    )

    conflicts("+papi", when="+simgrid")
    conflicts("~blocking", when="+simgrid")

    def autoreconf(self, spec, prefix):
        if not os.path.isfile("./configure"):
            autogen = Executable("./autogen.sh")
            autogen()

    def configure_args(self):
        spec = self.spec

        config_args = ["--disable-build-doc", "--enable-blas-lib=none", "--disable-mlr"]

        # add missing lib for simgrid static compilation,
        # already fixed since StarPU 1.2.1
        if spec.satisfies("+fxt"):
            mf = FileFilter("configure")
            mf.filter("libfxt.a -lrt", "libfxt.a -lrt -lbfd")

        mpicc = ""
        if spec.satisfies("+mpi~simgrid"):
            mpicc = spec["mpi"].mpicc
        elif spec.satisfies("+mpi+simgrid"):
            mpicc = "%s/bin/smpicc" % spec["simgrid"].prefix

        config_args.extend(
            [
                "--%s-shared" % ("enable" if "+shared" in spec else "disable"),
                "--%s-debug" % ("enable" if "+debug" in spec else "disable"),
                "--%s-verbose" % ("enable" if "+verbose" in spec else "disable"),
                "--%s-fast" % ("enable" if "+fast" in spec else "disable"),
                "--%s-build-tests" % ("enable" if "+examples" in spec else "disable"),
                "--%s-build-examples" % ("enable" if "+examples" in spec else "disable"),
                "--%s-fortran" % ("enable" if "+fortran" in spec else "disable"),
                "--%s-openmp" % ("enable" if "+openmp" in spec else "disable"),
                "--%s-blocking-drivers" % ("enable" if "+blocking" in spec else "disable"),
                "--%s-papi" % ("enable" if "+papi" in spec else "disable"),
                "--%s-opencl"
                % ("disable" if "~opencl" in spec or "+simgrid" in spec else "enable"),
                "--%s-cuda" % ("disable" if "~cuda" in spec or "+simgrid" in spec else "enable"),
                "--disable-mpi" if "~mpi" in spec else "--enable-mpi",
                "--without-mpicc" if "~mpi" in spec else "--with-mpicc=%s" % mpicc,
                "--with-hwloc=%s" % spec["hwloc"].prefix,
            ]
        )

        if spec.satisfies("+fxt"):
            config_args.append("--with-fxt=%s" % spec["fxt"].prefix)
            if spec.satisfies("@1.2:") or spec.satisfies("@git-1.2"):
                config_args.append("--enable-paje-codelet-details")

        if spec.satisfies("+simgrid"):
            config_args.append("--enable-simgrid")
            config_args.append("--with-simgrid-dir=%s" % spec["simgrid"].prefix)
            if spec.satisfies("+simgridmc"):
                config_args.append("--enable-simgrid-mc")

        # On OSX, deactivate glpk
        if spec.satisfies("platform=darwin"):
            config_args.append("--disable-glpk")

        return config_args
