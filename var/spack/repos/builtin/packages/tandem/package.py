# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    # we cannot use the tar.gz file because it does not contains submodules
    version(
        "1.1.0", tag="v1.1.0", commit="17c42dc9ae0ec519dcc1b5732681b2e4054666f1", submodules=True
    )
    version("1.0", tag="v1.0", commit="eccab10cbdf5842ed9903fac7a023be5e2779f36", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    patch("fix_v1.0_compilation.diff", when="@1.0")

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

    for var in ["openmpi", "mpich", "mvapich", "mvapich2", "mvapich2-gdr"]:
        depends_on(f"{var} +cuda", when=f"+cuda ^[virtuals=mpi] {var}")

    for var in ["mpich", "mvapich2-gdr"]:
        depends_on(f"{var} +rocm", when=f"+rocm ^[virtuals=mpi] {var}")

    depends_on("parmetis +int64 +shared")
    depends_on("metis +int64 +shared")
    depends_on("libxsmm@1.17 +generator", when="+libxsmm target=x86_64:")
    depends_on("lua@5.3.2:5.4.4")
    depends_on("eigen@3.4.0")

    depends_on("zlib-api")
    depends_on("petsc@3.16: +int64 +mumps +scalapack memalign=32")
    depends_on("petsc +knl", when="target=skylake:")

    with when("+cuda"):
        for tgt in CudaPackage.cuda_arch_values:
            depends_on(f"petsc +cuda cuda_arch={tgt}", when=f"+cuda cuda_arch={tgt}")
    with when("+rocm"):
        for tgt in ROCmPackage.amdgpu_targets:
            depends_on(f"petsc +rocm amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")

    depends_on("python@3", type="build", when="+python")
    depends_on("py-numpy", type="build", when="+python")

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

        arch_dic = {}
        arch_dic["skylake"] = "skl"
        arch_dic["skylake_avx512"] = "skx"
        arch_dic["haswell"] = "hsw"
        arch_dic["sandybridge"] = "snb"
        arch_dic["zen2"] = "rome"
        arch_dic["zen"] = "naples"
        target = str(self.spec.target)

        if target in arch_dic:
            args.append("-DARCH=" + arch_dic[target])
        else:
            print(target, "not in arch list of tandem, using native")
            args.append("-DARCH=native")

        return args

    def install(self, spec, prefix):
        self.cmake(spec, prefix)
        self.build(spec, prefix)
        install_tree(self.build_directory, prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.app)
