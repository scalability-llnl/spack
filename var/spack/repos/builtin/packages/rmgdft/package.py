# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Rmgdft(CMakePackage, CudaPackage):
    """RMGDFT is a high performance real-space density functional code
    designed for large scale electronic structure calculations."""

    homepage = "http://www.rmgdft.org/"
    git = "https://github.com/RMGDFT/rmgdft.git"
    maintainers("elbriggs")
    tags = ["ecp", "ecp-apps"]
    version("master", branch="master")
    version("6.1.0", tag="v6.1.0", commit="4dd5862725006b35d3118705197f89f13b24b858")
    version("5.4.0", tag="v5.4.0", commit="471251b191abb5f6ffdca4333c1fcb2add3c52f2")
    version("5.3.1", tag="v5.3.1", commit="dd6217ed82a8fe335acd0c030023b539d1be920a")
    version("5.2.0", tag="v5.2.0", commit="e95a84a258f84a3c33f36eb34ebb9daba691b649")
    version("5.0.5", tag="v5.0.5", commit="f67a5d80e4bb418d31f35586a19b21c9b52e7832")
    version("5.0.4", tag="v5.0.4", commit="30faadeff7dc896169d011910831263fb19eb965")
    version("5.0.1", tag="v5.0.1", commit="60b3ad64b09a4fccdd2b84052350e7947e3e8ad0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant("qmcpack", default=True, description="Build with qmcpack interface.")

    variant("local_orbitals", default=True, description="Build O(N) variant.")

    variant("rocm", default=False, description="Build rocm enabled variant.")

    # Normally we want this but some compilers (e.g. IBM) are
    # very slow when this is on so provide the option to disable
    variant(
        "internal_pp",
        default=True,
        description="Include built-in pseudopotentials. Normally "
        "enabled but some compilers are slow when "
        "this is on so provide a disable option.",
    )

    # RMGDFT 4.0.0 or later requires compiler support for C++14
    compiler_warning14 = "RMGDFT 4.0.0 or later requires a compiler with support for C++14"
    conflicts("%gcc@:4", when="@3.6.0:", msg=compiler_warning14)
    conflicts("%intel@:17", when="@3.6.0:", msg=compiler_warning14)
    conflicts("%pgi@:17", when="@3.6.0:", msg=compiler_warning14)
    conflicts("%llvm@:3.4", when="@3.6.0:", msg=compiler_warning14)

    # RMGDFT 5.0.0 requires C++17 and increase the minimum gcc to 8
    compiler_warning17 = "RMGDFT 5.0.0 or later requires a compiler with support for C++17"
    conflicts("%gcc@:7", when="@5.0.0:", msg=compiler_warning17)

    depends_on("cmake", type="build")
    depends_on("boost+filesystem+iostreams+thread+program_options+system", type="build")
    depends_on("boost@1.61.0:1.82.0")
    depends_on("fftw-api@3")
    depends_on("mpi")
    depends_on("hdf5")
    depends_on("cuda", when="+cuda")
    with when("+rocm"):
        depends_on("hipblas")
        depends_on("rocfft")
        depends_on("rocsolver")

    # RMG is a hybrid MPI/threads code and performance is
    # highly dependent on the threading model of the blas
    # libraries. Openblas-openmp is known to work well
    # so if spack yields a non-performant build you can
    # try to adjust your system config to use it.
    depends_on("blas")
    conflicts("^atlas", msg="The atlas threading model is incompatible with RMG")

    @property
    def build_targets(self):
        spec = self.spec
        if "+cuda" in spec:
            targets = ["rmg-gpu"]
            cuda_arch_list = spec.variants["cuda_arch"].value
            cuda_arch = cuda_arch_list[0]
            if cuda_arch != "none":
                args.append("-DCUDA_FLAGS=-arch=sm_{0}".format(cuda_arch))
            if "+local_orbitals" in spec:
                targets.append("rmg-on-gpu")
        else:
            targets = ["rmg-cpu"]
            if "+local_orbitals" in spec:
                targets.append("rmg-on-cpu")
        return targets

    def cmake_args(self):
        spec = self.spec
        args = []
        if "+qmcpack" in spec:
            args.append("-DQMCPACK=1")
        else:
            args.append("-DQMCPACK=0")
        if "+internal_pp" in spec:
            args.append("-DUSE_INTERNAL_PSEUDOPOTENTIALS=1")
        else:
            args.append("-DUSE_INTERNAL_PSEUDOPOTENTIALS=0")
        if "+cuda" in spec:
            args.append("-DRMG_CUDA_ENABLED=1")
        return args

    def install(self, spec, prefix):
        # create top-level directories
        mkdirp(prefix.bin)
        mkdirp(prefix.share.tests.RMG)

        with working_dir(self.build_directory):
            if "+cuda" in spec:
                install("rmg-gpu", prefix.bin)
                if "+local_orbitals" in spec:
                    install("rmg-on-gpu", prefix.bin)
            else:
                install("rmg-cpu", prefix.bin)
                if "+local_orbitals" in spec:
                    install("rmg-on-cpu", prefix.bin)

        # install tests
        with working_dir(self.build_directory):
            install_tree("tests/RMG", prefix.share.tests.RMG)
