# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dbcsr(CMakePackage, CudaPackage, ROCmPackage):
    """Distributed Block Compressed Sparse Row matrix library."""

    homepage = "https://github.com/cp2k/dbcsr"
    git = "https://github.com/cp2k/dbcsr.git"
    url = "https://github.com/cp2k/dbcsr/releases/download/v2.2.0/dbcsr-2.2.0.tar.gz"
    list_url = "https://github.com/cp2k/dbcsr/releases"

    maintainers("dev-zero", "mtaillefumier")

    license("GPL-2.0-or-later")

    version("develop", branch="develop")
    version("2.7.0", sha256="25c367b49fb108c5230bcfb127f05fc16deff2bb467f437023dfa6045aff66f6")
    version("2.6.0", sha256="c67b02ff9abc7c1f529af446a9f01f3ef9e5b0574f220259128da8d5ca7e9dc6")
    version("2.5.0", sha256="91fda9b2502e5d0a2a6cdd5a73ef096253cc7e75bd01ba5189a4726ad86aef08")
    version("2.4.1", sha256="b3d5ae62ca582b72707a2c932e8074a4f2f61d61085d97bd374213c70b8dbdcf")
    version("2.4.0", sha256="cf2b774328c9a30677501f49b79955841bd08915a7ca53c8533bfdf14a8f9bd4")
    version("2.3.0", sha256="f750de586cffa66852b646f7f85eb831eeb64fa2d25ce50ed10e1df016dd3364")
    version("2.2.0", sha256="245b0382ddc7b80f85af8288f75bd03d56ec51cdfb6968acb4931529b35173ec")
    version("2.1.0", sha256="9e58fd998f224632f356e479d18b5032570d00d87b86736b6a6ac2d03f8d4b3c")
    version("2.0.1", sha256="61d5531b661e1dab043353a1d67939ddcde3893d3dc7b0ab3d05074d448b485c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Compile with MPI")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("shared", default=True, description="Build shared library")
    variant(
        "smm",
        default="libxsmm",
        values=("libxsmm", "blas"),
        description="Library for small matrix multiplications",
    )
    variant(
        "cuda_arch_35_k20x",
        default=False,
        description=(
            "CP2K (resp. DBCSR) has specific parameter sets for"
            " different GPU models. Enable this when building"
            " with cuda_arch=35 for a K20x instead of a K40"
        ),
    )
    variant("examples", default=True, description="Build examples")

    variant("opencl", default=False, description="Enable OpenCL backend")
    variant("mpi_f08", default=False, when="@2.6:", description="Use mpi F08 module")

    variant("g2g", default=False, description="GPU-aware MPI with CUDA/HIP")
    conflicts("+g2g", when="~cuda ~rocm", msg="GPU-aware MPI requires +cuda or +rocm")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")

    with when("smm=libxsmm"):
        depends_on("libxsmm~header-only")
        depends_on("libxsmm@1.11:1")

    depends_on("cmake@3.10:", type="build")
    depends_on("cmake@3.12:", type="build", when="@2.1:")
    depends_on("cmake@3.17:", type="build", when="@2.2:")
    depends_on("cmake@3.22:", type="build", when="@2.3:")

    depends_on("py-fypp", type="build")
    depends_on("py-fypp@3.1:", type="build", when="@2.6:")
    depends_on("pkgconfig", type="build")
    depends_on("python@3.6:", type="build", when="+cuda")

    depends_on("hipblas", when="+rocm")

    depends_on("opencl", when="+opencl")

    # All examples require MPI
    conflicts("+examples", when="~mpi", msg="Examples require MPI")

    # We only support specific gpu archs for which we have parameter files
    # for optimal kernels. Note that we don't override the parent class arch
    # properties, since the parent class defines constraints for different archs
    # Instead just mark all unsupported cuda archs as conflicting.
    dbcsr_cuda_archs = ("35", "37", "60", "70", "80", "90")
    cuda_msg = "dbcsr only supports cuda_arch {0}".format(dbcsr_cuda_archs)

    for arch in CudaPackage.cuda_arch_values:
        if arch not in dbcsr_cuda_archs:
            conflicts("+cuda", when="cuda_arch={0}".format(arch), msg=cuda_msg)

    conflicts("+cuda", when="cuda_arch=none", msg=cuda_msg)

    dbcsr_amdgpu_targets = ("gfx906", "gfx910", "gfx90a", "gfx90a:xnack-", "gfx90a:xnack+")
    amd_msg = f"DBCSR supports these AMD gpu targets:  {', '.join(dbcsr_amdgpu_targets)}"

    for arch in ROCmPackage.amdgpu_targets:
        if arch not in dbcsr_amdgpu_targets:
            conflicts("+rocm", when="amdgpu_target={0}".format(arch), msg=amd_msg)

    accel_msg = "CUDA, ROCm and OpenCL support are mutually exlusive"
    conflicts("+cuda", when="+rocm", msg=accel_msg)
    conflicts("+cuda", when="+opencl", msg=accel_msg)
    conflicts("+rocm", when="+opencl", msg=accel_msg)

    # Require openmp threading for OpenBLAS by making other options conflict
    conflicts("^openblas threads=pthreads", when="+openmp")
    conflicts("^openblas threads=none", when="+openmp")

    conflicts("smm=blas", when="+opencl")

    with when("+mpi"):
        # When using mpich 4.1 or higher, mpi_f08 has to be used, otherwise:
        # Error: Type mismatch in argument 'baseptr' at (1); passed TYPE(c_ptr)
        # to INTEGER(8)
        conflicts("^mpich@4.1:", when="@:2.5")
        conflicts("~mpi_f08", when="^mpich@4.1:")
        depends_on("mpich+fortran", when="^[virtuals=mpi] mpich")

    generator("ninja")
    depends_on("ninja@1.10:", type="build")

    def cmake_args(self):
        spec = self.spec

        if "+cuda" in spec and len(spec.variants["cuda_arch"].value) > 1:
            raise InstallError("dbcsr supports only one cuda_arch at a time")

        if "+rocm" in spec and len(spec.variants["amdgpu_target"].value) > 1:
            raise InstallError("DBCSR supports only one amdgpu_arch at a time")

        args = [
            "-DUSE_SMM=%s" % ("libxsmm" if "smm=libxsmm" in spec else "blas"),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define_from_variant("USE_OPENMP", "openmp"),
            # C API needs MPI
            self.define_from_variant("WITH_C_API", "mpi"),
            "-DBLAS_FOUND=true",
            "-DBLAS_LIBRARIES=%s" % (spec["blas"].libs.joined(";")),
            "-DLAPACK_FOUND=true",
            "-DLAPACK_LIBRARIES=%s" % (spec["lapack"].libs.joined(";")),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("WITH_EXAMPLES", "examples"),
            self.define_from_variant("WITH_G2G", "g2g"),
        ]

        # Switch necessary as a result of a bug.
        if spec.satisfies("@2.1:2.2"):
            args += ["-DBUILD_TESTING=ON"]

        if self.spec.satisfies("+cuda"):
            cuda_arch = self.spec.variants["cuda_arch"].value[0]

            gpu_map = {
                "35": "K40",
                "37": "K80",
                "60": "P100",
                "70": "V100",
                "80": "A100",
                "90": "H100",
            }

            gpuver = gpu_map[cuda_arch]
            if cuda_arch == "35" and self.spec.satisfies("+cuda_arch_35_k20x"):
                gpuver = "K20X"

            args += ["-DWITH_GPU=%s" % gpuver, "-DUSE_ACCEL=cuda"]

        if self.spec.satisfies("+rocm"):
            amd_arch = self.spec.variants["amdgpu_target"].value[0]
            gpuver = {
                "gfx906": "Mi50",
                "gfx908": "Mi100",
                "gfx90a": "Mi250",
                "gfx90a:xnack-": "Mi250",
                "gfx90a:xnack+": "Mi250",
            }[amd_arch]

            args += ["-DWITH_GPU={0}".format(gpuver), "-DUSE_ACCEL=hip"]

        if self.spec.satisfies("+opencl"):
            args += ["-DUSE_ACCEL=opencl"]

        if self.spec.satisfies("+mpi_f08"):
            args += ["-DUSE_MPI_F08=ON"]

        return args

    def check(self):
        """Override CMakePackage's check() to enforce seralized test runs
        since they are already parallelized"""
        with working_dir(self.build_directory):
            self._if_ninja_target_execute("test", parallel=False)
