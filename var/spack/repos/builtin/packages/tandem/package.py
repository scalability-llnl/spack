# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Tandem(CMakePackage, CudaPackage, ROCmPackage):
    """Tandem is a scientific software for SEAS modelling and for solving Poisson
    and linear elasticity problems. It implements the Symmetric Interior Penalty
    Galerkin (SIPG) method using unstructured simplicial meshes (triangle meshes
    in 2D, tetrahedral meshes in 3D)."""

    homepage = "https://tandem.readthedocs.io/en/latest/"
    git = "https://github.com/TEAR-ERC/tandem.git"

    license("BSD-3-Clause")

    version("main", branch="main", submodules=True)
    version("develop", branch="thomas/develop", submodules=True)

    # we cannot use the tar.gz file because it does not contains submodules
    version(
        "1.1.0", tag="v1.1.0", commit="17c42dc9ae0ec519dcc1b5732681b2e4054666f1", submodules=True
    )
    version("1.0", tag="v1.0", commit="eccab10cbdf5842ed9903fac7a023be5e2779f36", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    patch(
        "fix_v1.0_compilation.diff",
        when="@1.0",
        sha256="ef7325c1e59811e1992e3846044232154e4286fcaeae2ea5575a6ae77dda8b7d",
    )

    maintainers("dmay23", "Thomas-Ulrich")
    variant("polynomial_degree", default="2", description="Polynomial degree")
    variant(
        "domain_dimension",
        default="2",
        description="Dimension of the domain",
        values=("2", "3"),
        multi=False,
    )
    variant(
        "min_quadrature_order",
        default="0",
        description="Minimum order of quadrature rule, 0 = automatic",
    )
    variant("libxsmm", default=False, description="Install libxsmm-generator")
    variant("python", default=False, description="installs python and numpy")

    depends_on("mpi")

    for var in ["openmpi", "mpich"]:
        for tgt in CudaPackage.cuda_arch_values:
            depends_on(
                f"{var} +cuda cuda_arch={tgt}", when=f"+cuda cuda_arch={tgt} ^[virtuals=mpi] {var}"
            )
    # these 2 are not cuda packages
    for var in ["mvapich", "mvapich2", "mvapich2-gdr"]:
        depends_on(f"{var} +cuda", when=f"+cuda ^[virtuals=mpi] {var}")

    for var in ["mpich", "mvapich2-gdr"]:
        depends_on(f"{var} +rocm", when=f"+rocm ^[virtuals=mpi] {var}")

    depends_on("parmetis +int64 +shared")
    depends_on("metis +int64 +shared")
    depends_on("libxsmm@1.17 +generator", when="+libxsmm target=x86_64:")
    depends_on("lua@5.3.2:5.4.4")
    depends_on("eigen@3.4.0")

    depends_on("zlib-api")

    # Dictionary for architecture alignments
    arch_alignments = {
        "x86_64": 8,
        "x86_64_v2": 16,
        "x86_64_v3": 32,
        "x86_64_v4": 64,
        "westmere": 16,
        "sandybridge": 32,
        "haswell": 32,
        "mic_knl": 64,
        "skylake": 64,
        "cascadelake": 64,
        "icelake": 64,
        "naples": 32,
        "rome": 32,
        "milan": 64,
        "bergamo": 64,
        "thunderx2": 64,
        "power9": 64,
        "apple-m1": 128,
        "apple-m2": 128,
        "a64fx": 128,
        "aarch64": 16,  # For completeness, include aarch64 if needed
        "neon": 16,
        "zen": 32,
        "zen2": 32,
        "zen3": 64,
        "zen4": 64,
    }

    possible_memalign = ("32", "64", "128", "256", "512", "1024", "2048", "4096", "8192", "none")

    conflicts("^petsc memalign=4")
    conflicts("^petsc memalign=8")
    conflicts("^petsc memalign=16")

    for arch, align in arch_alignments.items():
        for forbidden in possible_memalign:
            if forbidden != f"{align}":
                conflicts(f"^petsc memalign={forbidden}", when=f"target={arch}")

    depends_on("petsc +int64 +mumps +scalapack")
    depends_on("petsc@3.22:", when="@1.2:")
    depends_on("petsc@3.16:3.17", when="@:1.1")

    depends_on("petsc +knl", when="target=skylake:")

    with when("+cuda"):
        for tgt in CudaPackage.cuda_arch_values:
            depends_on(f"petsc +cuda cuda_arch={tgt}", when=f"+cuda cuda_arch={tgt}")
    with when("+rocm"):
        for tgt in ROCmPackage.amdgpu_targets:
            depends_on(f"petsc +rocm amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")

    depends_on("python@3", type="build", when="+python")
    depends_on("python@3.9:", type="build", when="@:1.2 +python")
    depends_on("py-numpy", type="build", when="+python")
    depends_on("py-setuptools", type="build", when="+python")

    # see https://github.com/TEAR-ERC/tandem/issues/45
    conflicts("%intel")

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

    def cmake_args(self):
        args = [
            self.define_from_variant("DOMAIN_DIMENSION", "domain_dimension"),
            self.define_from_variant("POLYNOMIAL_DEGREE", "polynomial_degree"),
            self.define_from_variant("MIN_QUADRATURE_ORDER", "min_quadrature_order"),
        ]

        # basic family matching
        hostarch = "noarch"
        if self.spec.target >= "aarch64":
            hostarch = "neon"
        if self.spec.target >= "x86_64":
            # pure x86_64v1 doesn't support anything above SSE3
            hostarch = "noarch"
        if self.spec.target >= "x86_64_v2":
            # AVX is only required for x86_64v3 and upwards
            hostarch = "wsm"
        if self.spec.target >= "x86_64_v3":
            hostarch = "hsw"
        if self.spec.target >= "x86_64_v4":
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

        args.append(f"-DARCH={hostarch}")

        return args

    def install(self, spec, prefix):
        self.cmake(spec, prefix)
        self.build(spec, prefix)
        install_tree(self.build_directory, prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.app)
