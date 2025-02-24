# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Seissol(CMakePackage, CudaPackage, ROCmPackage):
    """Seissol - A scientific software for the numerical simulation
    of seismic wave phenomena and earthquake dynamics.
    """

    homepage = "http://www.seissol.org"
    git = "https://github.com/SeisSol/SeisSol.git"
    version("master", branch="master", submodules=True)
    # we cannot use the tar.gz file because it does not contains submodules
    version(
        "1.3.0", tag="v1.3.0", commit="91377508af4412914d707b04481f8b678b1c4044", submodules=True
    )
    version(
        "1.2.0", tag="v1.2.0", commit="2057e6e81965e0789128c6d177592800bcf956e1", submodules=True
    )
    version(
        "1.1.4", tag="v1.1.4", commit="6d301757378ad8446173e0a12c095a695a708aaf", submodules=True
    )
    version(
        "1.1.3", tag="v1.1.3", commit="01ae1b127fcc6f766b819d2e797df6a3547d730a", submodules=True
    )
    version(
        "1.1.2", tag="v1.1.2", commit="71002c1c1498ebd6f50a954731da68fa4f9d436b", submodules=True
    )

    version(
        "1.0.1", tag="v1.0.1", commit="9b1b0ec970af4ad79a155c63035234b660838476", submodules=True
    )

    maintainers("Thomas-Ulrich", "davschneller", "vikaskurapati")

    variant("asagi", default=True, description="Use ASAGI for material input")
    variant(
        "convergence_order",
        default="4",
        description="polynomial degree plus one",
        values=(str(v) for v in range(2, 9)),
        multi=False,
    )
    variant(
        "precision",
        default="double",
        description="float numerical precision",
        values=("single", "double"),
        multi=False,
    )
    variant(
        "dr_quad_rule",
        default="stroud",
        description="dynamic rupture quadrature rule",
        values=("stroud", "dunavant"),
        multi=False,
    )
    variant(
        "plasticity_method",
        default="nb",
        description="Plasticity method",
        values=("nb", "ib"),
        multi=False,
    )
    variant(
        "equations",
        default="elastic",
        description="equation set used",
        values=("elastic", "anisotropic", "viscoelastic2", "poroelastic"),
        multi=False,
    )
    variant(
        "number_of_mechanisms", default="3", description="number of mechanisms for viscoelasticity"
    )
    variant("netcdf", default=True, description="Enable Netcdf")
    variant(
        "graph_partitioning_libs",
        default="parmetis",
        description="graph partitioning library for mesh partitioning",
        values=("none", "parmetis", "ptscotch", "parhip"),
        multi=True,
    )

    # GPU options
    variant("intel_gpu", default=False, description="Compile for Intel GPUs")
    variant(
        "intel_gpu_arch",
        default="none",
        values=("none", "bdw", "skl", "pvc"),
        description="The Intel GPU to compile for",
        when="+intel_gpu",
    )

    forwarded_variants = ["cuda", "intel_gpu", "rocm"]
    for v in forwarded_variants:
        variant(
            "sycl_backend",
            default="acpp",
            description="SYCL backend to use for DR and point sources",
            values=("acpp", "oneapi"),
            when=f"+{v}",
        )
        variant(
            "sycl_gemm",
            default=False,
            description="Use SYCL also for the wave propagation part (default for Intel GPUs)",
            when=f"+{v}",
        )

    requires(
        "-cuda -rocm -intel_gpu",
        "+cuda",
        "+rocm",
        "+intel_gpu",
        policy="one_of",
        msg="You may either compile for one GPU backend, or for CPU.",
    )

    requires("%oneapi", when="sycl_backend=oneapi")

    depends_on("hipsycl@0.9.3: +cuda", when="+cuda sycl_backend=acpp")

    # TODO: this one needs to be +rocm as well--but that's not implemented yet
    depends_on("hipsycl@develop", when="+rocm sycl_backend=acpp")

    # TODO: extend as soon as level zero is available
    depends_on("hipsycl@develop", when="+intel_gpu sycl_backend=acpp")

    # TODO: once adaptivecpp supports NVHPC, forward that (SYCL_USE_NVHPC)

    # GPU architecture requirements
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="A value for cuda_arch must be specified. Add cuda_arch=XX",
    )

    conflicts(
        "amdgpu_target=none",
        when="+rocm",
        msg="A value for amdgpu_arch must be specified. Add amdgpu_arch=XX",
    )

    conflicts(
        "intel_gpu_arch=none",
        when="+intel_gpu",
        msg="A value for intel_gpu_arch must be specified. Add intel_gpu_arch=XX",
    )

    conflicts(
        "%intel",
        when="@1.3:",
        msg="The Intel compiler is unsupported from v1.3 onward. Please use e.g.gcc or oneapi",
    )

    variant(
        "gemm_tools_list",
        default="LIBXSMM,PSpaMM",
        description="gemm toolkit(s) for the (CPU) code generator",
        values=("LIBXSMM", "MKL", "OpenBLAS", "BLIS", "PSpaMM", "Eigen", "LIBXSMM_JIT"),
        multi=True,
    )

    variant("memkind", default=True, description="Use memkind library for hbw memory support")

    depends_on("mpi")

    with when("+cuda"):
        for var in ["openmpi", "mpich", "mvapich", "mvapich2", "mvapich2-gdr"]:
            depends_on(f"{var} +cuda", when=f"^[virtuals=mpi] {var}")

    with when("+rocm"):
        for var in ["mpich", "mvapich2-gdr"]:
            depends_on(f"{var} +rocm", when=f"^[virtuals=mpi] {var}")

    # with cuda 12 and llvm 14:15, we have the issue: "error: no template named 'texture"
    # https://github.com/llvm/llvm-project/issues/61340
    conflicts("cuda@12", when="+cuda ^llvm@14:15")
    depends_on("cuda@11:", when="+cuda")
    depends_on("hip", when="+rocm")

    # graph partitioning
    with when("graph_partitioning_libs=parmetis"):
        depends_on("parmetis +int64 +shared")
        depends_on("metis +int64 +shared")

    depends_on(
        "scotch +mpi +mpi_thread +shared +threads +int64", when="graph_partitioning_libs=ptscotch"
    )
    depends_on("kahip", when="graph_partitioning_libs=parhip")

    depends_on("hdf5 +shared +threadsafe +hl +mpi")

    depends_on("netcdf-c@4.6: +shared +mpi", when="+netcdf")

    depends_on("asagi +mpi +mpi3", when="+asagi")

    depends_on("easi ~asagi jit=impalajit,lua", when="~asagi")
    depends_on("easi +asagi jit=impalajit,lua", when="+asagi")

    depends_on("intel-mkl threads=none", when="gemm_tools_list=MKL")
    depends_on("blis threads=none", when="gemm_tools_list=BLIS")
    depends_on("openblas threads=none", when="gemm_tools_list=OpenBLAS")
    depends_on("libxsmm@main", when="gemm_tools_list=LIBXSMM_JIT")

    conflicts("gemm_tools_list=LIBXSMM", when="gemm_tools_list=LIBXSMM_JIT")

    depends_on("memkind", when="+memkind target=x86_64:")

    depends_on("yaml-cpp@0.6.2")
    depends_on("eigen@3.4.0")

    # build dependencies (code generation)
    with default_args(type="build"):
        # https://seissol.readthedocs.io/en/latest/installing-dependencies.html
        depends_on("cmake@3.20:")
        depends_on("python@3.9:")
        depends_on("py-setuptools")
        depends_on("py-numpy@1.12:")
        depends_on("py-scipy")
        depends_on("py-matplotlib")
        depends_on("py-pspamm", when="gemm_tools_list=PSpaMM")

        forwarded_variants = ["cuda", "intel_gpu", "rocm"]
        for v in forwarded_variants:
            depends_on("py-gemmforge", when=f"+{v}")
            depends_on("py-chainforgecodegen", when=f"+{v}")

        depends_on("libxsmm@=1.17 +generator", when="gemm_tools_list=LIBXSMM target=x86_64:")

    def cmake_args(self):
        args = [
            "-DMPI=ON",
            self.define_from_variant("ASAGI", "asagi"),
            self.define_from_variant("PRECISION", "precision"),
            self.define_from_variant("PLASTICITY_METHOD", "plasticity_method"),
            self.define_from_variant("DR_QUAD_RULE", "dr_quad_rule"),
            self.define_from_variant("ORDER", "convergence_order"),
            self.define_from_variant("EQUATIONS", "equations"),
            self.define_from_variant("NETCDF", "netcdf"),
        ]

        gemm_tools_list = ",".join(self.spec.variants["gemm_tools_list"].value)
        args.append(f"-DGEMM_TOOLS_LIST={gemm_tools_list}")

        graph_partitioning_libs = ",".join(self.spec.variants["graph_partitioning_libs"].value)
        args.append(f"-DGRAPH_PARTITIONING_LIBS={graph_partitioning_libs}")

        if self.spec.variants["equations"].value != "viscoelastic2":
            args.append("-DNUMBER_OF_MECHANISMS=0")
        else:
            args.append(self.define_from_variant("NUMBER_OF_MECHANISMS", "number_of_mechanisms"))

        with_gpu = (
            self.spec.satisfies("+cuda")
            or self.spec.satisfies("+rocm")
            or self.spec.satisfies("+intel_gpu")
        )

        if with_gpu:
            # Nvidia GPUs
            if self.spec.satisfies("+cuda"):
                cuda_arch = self.spec.variants["cuda_arch"].value[0]
                args.append(f"-DDEVICE_ARCH=sm_{cuda_arch}")
                args.append("-DUSE_GRAPH_CAPTURING=ON -DENABLE_PROFILING_MARKERS=ON")
                if self.spec.satisfies("~sycl_gemm"):
                    args.append("-DDEVICE_BACKEND=cuda")

            # ROCm/AMD GPUs
            if self.spec.satisfies("+rocm"):
                amdgpu_target = self.spec.variants["amdgpu_target"].value[0]
                args.append(f"-DDEVICE_ARCH={amdgpu_target}")
                args.append("-DENABLE_PROFILING_MARKERS=ON")

                if self.spec.satisfies("+rocm@:5.6"):
                    args.append("-DUSE_GRAPH_CAPTURING=OFF")
                else:
                    args.append("-DUSE_GRAPH_CAPTURING=ON")

                if self.spec.satisfies("~sycl_gemm"):
                    args.append("-DDEVICE_BACKEND=hip")

            # Intel GPUs
            if self.spec.satisfies("+intel_gpu"):
                assert self.spec.variants["intel_gpu_arch"].value != "none"
                intel_gpu_arch = self.spec.variants["intel_gpu_arch"].value
                if self.spec.satisfies("@:1.1.3"):
                    args.append("-DUSE_GRAPH_CAPTURING=OFF")
                else:
                    args.append("-DUSE_GRAPH_CAPTURING=ON")
                args.append(f"-DDEVICE_ARCH={intel_gpu_arch}")

            # SYCL
            sycl_backends = {"acpp": "hipsycl", "oneapi": "oneapi"}
            syclcc_backends = {"acpp": "hipsycl", "oneapi": "dpcpp"}

            sycl_backend = self.spec.variants["sycl_backend"].value
            args.append(f"-DSYCLCC={syclcc_backends[sycl_backend]}")
            if self.spec.satisfies("+sycl_gemm"):
                args.append(f"-DDEVICE_BACKEND={sycl_backends[sycl_backend]}")

        # CPU arch

        # cf. https://spack.readthedocs.io/en/latest/basic_usage.html#support-for-specific-microarchitectures

        # basic family matching
        hostarch = "noarch"
        if str(self.spec.target) == "aarch64":
            hostarch = "neon"
        if str(self.spec.target) == "x86_64":
            # pure x86_64v1 doesn't support anything above SSE3
            hostarch = "noarch"
        if str(self.spec.target) == "x86_64_v2":
            # AVX is only required for x86_64v3 and upwards
            hostarch = "wsm"
        if str(self.spec.target) == "x86_64_v3":
            hostarch = "hsw"
        if str(self.spec.target) == "x86_64_v4":
            hostarch = "skx"

        # specific architecture matching
        if self.spec.target >= "westmere":
            hostarch = "wsm"
        if self.spec.target >= "sandybridge":
            hostarch = "snb"
        if self.spec.target >= "haswell":
            hostarch = "hsw"
        if self.spec.target >= "mic_knl":
            hostarch = "knl"
        if self.spec.target >= "skylake_avx512":
            hostarch = "skx"
        if self.spec.target >= "zen":
            hostarch = "naples"
        if self.spec.target >= "zen2":
            hostarch = "rome"
        if self.spec.target >= "zen3":
            hostarch = "milan"
        if self.spec.target >= "zen4":
            hostarch = "bergamo"
        if self.spec.target >= "thunderx2":
            hostarch = "thunderx2t99"
        if self.spec.target >= "power9":
            hostarch = "power9"
        if self.spec.target >= "m1":
            hostarch = "apple-m1"
        if self.spec.target >= "m2":
            hostarch = "apple-m2"
        if self.spec.target >= "a64fx":
            hostarch = "a64fx"

        args.append(f"-DHOST_ARCH={hostarch}")

        args.append(self.define("PYTHON_EXECUTABLE", self.spec["python"].command.path))

        return args

    def setup_run_environment(self, env):
        # for seissol-launch
        env.prepend_path("PATH", self.prefix.share)
