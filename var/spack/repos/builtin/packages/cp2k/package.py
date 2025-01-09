# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import os
import os.path
import sys

import spack.util.environment
from spack.build_environment import dso_suffix
from spack.build_systems import cmake, makefile
from spack.package import *

GPU_MAP = {
    "35": "K40",
    "37": "K80",
    "60": "P100",
    "70": "V100",
    "80": "A100",
    "90": "H100",
    "gfx906": "Mi50",
    "gfx908": "Mi100",
    "gfx90a": "Mi250",
    "gfx90a:xnack-": "Mi250",
    "gfx90a:xnack+": "Mi250",
}


class Cp2k(MakefilePackage, CMakePackage, CudaPackage, ROCmPackage):
    """CP2K is a quantum chemistry and solid state physics software package
    that can perform atomistic simulations of solid state, liquid, molecular,
    periodic, material, crystal, and biological systems
    """

    build_system(conditional("cmake", when="@2023.2:"), "makefile", default="cmake")

    homepage = "https://www.cp2k.org"
    url = "https://github.com/cp2k/cp2k/releases/download/v3.0.0/cp2k-3.0.tar.bz2"
    git = "https://github.com/cp2k/cp2k.git"
    list_url = "https://github.com/cp2k/cp2k/releases"

    maintainers("dev-zero", "mtaillefumier")

    license("GPL-2.0-or-later")

    version("2024.3", sha256="a6eeee773b6b1fb417def576e4049a89a08a0ed5feffcd7f0b33c7d7b48f19ba")
    version("2024.2", sha256="cc3e56c971dee9e89b705a1103765aba57bf41ad39a11c89d3de04c8b8cdf473")
    version("2024.1", sha256="a7abf149a278dfd5283dc592a2c4ae803b37d040df25d62a5e35af5c4557668f")
    version("2023.2", sha256="adbcc903c1a78cba98f49fe6905a62b49f12e3dfd7cedea00616d1a5f50550db")
    version("2023.1", sha256="dff343b4a80c3a79363b805429bdb3320d3e1db48e0ff7d20a3dfd1c946a51ce")
    version("2022.2", sha256="1a473dea512fe264bb45419f83de432d441f90404f829d89cbc3a03f723b8354")
    version("2022.1", sha256="2c34f1a7972973c62d471cd35856f444f11ab22f2ff930f6ead20f3454fd228b")
    version("9.1", sha256="fedb4c684a98ad857cd49b69a3ae51a73f85a9c36e9cb63e3b02320c74454ce6")
    version("8.2", sha256="2e24768720efed1a5a4a58e83e2aca502cd8b95544c21695eb0de71ed652f20a")
    version("8.1", sha256="7f37aead120730234a60b2989d0547ae5e5498d93b1e9b5eb548c041ee8e7772")
    version("7.1", sha256="ccd711a09a426145440e666310dd01cc5772ab103493c4ae6a3470898cd0addb")
    version("master", branch="master", submodules="True")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    generator("ninja")

    variant("mpi", default=True, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")
    variant(
        "smm",
        default="libxsmm",
        values=("libxsmm", "libsmm", "blas"),
        description="Library for small matrix multiplications",
    )
    variant("plumed", default=False, description="Enable PLUMED support")
    variant(
        "libint", default=True, description="Use libint, required for HFX (and possibly others)"
    )
    variant("libxc", default=True, description="Support additional functionals via libxc")
    variant(
        "pexsi",
        default=False,
        description="Enable the alternative PEXSI method for density matrix evaluation",
        when="+mpi",
    )
    variant(
        "elpa",
        default=False,
        description="Enable optimised diagonalisation routines from ELPA",
        when="+mpi",
    )
    variant(
        "dlaf",
        default=False,
        description="Enable DLA-Future eigensolver and Cholesky decomposition",
        when="@2024.1: build_system=cmake +mpi",
    )
    # sirius support was introduced in 7, but effectively usable starting from CP2K 9
    variant(
        "sirius",
        default=False,
        description="Enable planewave electronic structure calculations via SIRIUS",
        when="@9: +mpi",
    )
    variant("cosma", default=False, description="Use COSMA for p?gemm", when="@8: +mpi")
    variant(
        "libvori",
        default=False,
        description="Enable support for Voronoi integration and BQB compression",
        when="@8:",
    )
    variant("spglib", default=False, description="Enable support for spglib")
    variant(
        "spla",
        default=False,
        description="Use SPLA off-loading functionality. Only relevant when CUDA or ROCM"
        " are enabled",
    )
    variant("pytorch", default=False, description="Enable libtorch support")
    variant("quip", default=False, description="Enable quip support")
    variant("mpi_f08", default=False, description="Use MPI F08 module")

    variant(
        "enable_regtests",
        default=False,
        description="Configure cp2k to run the regtests afterwards."
        " It build cp2k normally but put the executables in exe/cmake-build-* instead of the"
        " conventional location. This option is only relevant when regtests need to be run.",
    )

    with when("+cuda"):
        variant(
            "cuda_arch_35_k20x",
            default=False,
            description=(
                "CP2K (resp. DBCSR) has specific parameter sets for"
                " different GPU models. Enable this when building"
                " with cuda_arch=35 for a K20x instead of a K40"
            ),
        )
        variant(
            "cuda_fft", default=False, description="Use CUDA also for FFTs in the PW part of CP2K"
        )
        variant(
            "cuda_blas",
            default=False,
            when="@:7",  # req in CP2K v8+
            description="Use CUBLAS for general matrix operations in DBCSR",
        )

    HFX_LMAX_RANGE = range(4, 8)

    variant(
        "lmax",
        description="Maximum supported angular momentum (HFX and others)",
        default="5",
        values=[str(x) for x in HFX_LMAX_RANGE],
        multi=False,
    )

    depends_on("python@3", type="build")

    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api@3")

    # Force openmp propagation on some providers of blas / fftw-api
    with when("+openmp"):
        depends_on("fftw+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("amdfftw+openmp", when="^[virtuals=fftw-api] amdfftw")
        depends_on("cray-fftw+openmp", when="^[virtuals=fftw-api] cray-fftw")
        depends_on("armpl-gcc threads=openmp", when="^[virtuals=blas] armpl-gcc")
        depends_on("openblas threads=openmp", when="^[virtuals=blas] openblas")
        # The Cray compiler wrappers will automatically add libsci_mp with
        # -fopenmp. Since CP2K unconditionally links blas/lapack/scalapack
        # we have to be consistent.
        depends_on("cray-libsci+openmp", when="^[virtuals=blas] cray-libsci")

    with when("smm=libxsmm"):
        depends_on("libxsmm~header-only")
        # require libxsmm-1.11+ since 1.10 can leak file descriptors in Fortran
        depends_on("libxsmm@1.11:")
        depends_on("libxsmm@1.17:", when="@9.1:")
        # build needs to be fixed for libxsmm@2 once it is released
        depends_on("libxsmm@:1")
        # use pkg-config (support added in libxsmm-1.10) to link to libxsmm
        depends_on("pkgconfig", type="build")

    with when("+libint"):
        depends_on("pkgconfig", type="build", when="@7.0:")
        for lmax in HFX_LMAX_RANGE:
            depends_on(f"libint@2.6.0:+fortran tune=cp2k-lmax-{lmax}", when=f"@7.0: lmax={lmax}")
            # AOCC only works with libint@2.6.0
            depends_on(
                f"libint@=2.6.0+fortran tune=cp2k-lmax-{lmax}", when=f"@7.0: lmax={lmax} %aocc"
            )

    with when("+libxc"):
        depends_on("pkgconfig", type="build", when="@7.0:")
        depends_on("libxc@4.0.3:4", when="@7.0:8.1")
        depends_on("libxc@5.1.3:5.1", when="@8.2:8")
        depends_on("libxc@5.1.7:5.1", when="@9:2022.2")
        depends_on("libxc@6.1:", when="@2023.1:")
        depends_on("libxc@6.2:", when="@2023.2:")
        depends_on("libxc@:6", when="@:2024.3")

    with when("+spla"):
        depends_on("spla+cuda+fortran", when="+cuda")
        depends_on("spla+rocm+fortran", when="+rocm")

    with when("+mpi"):
        depends_on("mpi@2:")
        depends_on("mpi@3:", when="@2023.1:")
        depends_on("scalapack")
        depends_on("mpich+fortran", when="^[virtuals=mpi] mpich")
        conflicts("~mpi_f08", when="^mpich@4.1:")

    with when("+cosma"):
        depends_on("cosma+scalapack")
        depends_on("cosma@2.5.1:", when="@9:")
        depends_on("cosma@2.6.3:", when="@2023.2:")
        depends_on("cosma+cuda", when="+cuda")
        depends_on("cosma+rocm", when="+rocm")

    with when("+elpa"):
        depends_on("elpa+openmp", when="+openmp")
        depends_on("elpa~openmp", when="~openmp")
        depends_on("elpa+cuda", when="+cuda")
        depends_on("elpa~cuda", when="~cuda")
        depends_on("elpa+rocm", when="+rocm")
        depends_on("elpa~rocm", when="~rocm")
        depends_on("elpa@2021.05:", when="@8.3:")
        depends_on("elpa@2021.11.001:", when="@9.1:")
        depends_on("elpa@2023.05.001:", when="@2023.2:")

    with when("+dlaf"):
        with when("@:2024.1"):
            depends_on("dla-future@0.2.1: +scalapack")
            depends_on("dla-future ~cuda", when="~cuda")
            depends_on("dla-future ~rocm", when="~rocm")
            depends_on("dla-future +cuda", when="+cuda")
            depends_on("dla-future +rocm", when="+rocm")

        with when("@2024.2:"):
            depends_on("dla-future-fortran@0.1.0:")
            depends_on("dla-future-fortran@0.2.0:", when="@2025.1:")

            # Use a direct dependency on dla-future so that constraints can be expressed
            # WARN: In the concretizer output, dla-future will appear as dependency of CP2K
            #       instead of dla-future-fortran
            depends_on("dla-future ~cuda", when="~cuda")
            depends_on("dla-future ~rocm", when="~rocm")
            depends_on("dla-future +cuda", when="+cuda")
            depends_on("dla-future +rocm", when="+rocm")

    conflicts(
        "+plumed",
        when="@:2024.1 build_system=cmake",
        msg="PLUMED support is broken in cp2k@:2024.1 with CMake",
    )
    with when("+plumed"):
        depends_on("plumed+shared")
        depends_on("plumed+mpi", when="+mpi")
        depends_on("plumed~mpi", when="~mpi")

    # while we link statically against PEXSI, its own deps may be linked in
    # dynamically, therefore can't set this as pure build-type dependency.
    depends_on("pexsi+fortran@0.10.0:", when="+pexsi")

    # only OpenMP should be consistently used, all other common things
    # like ELPA, SCALAPACK are independent and Spack will ensure that
    # a consistent/compatible combination is pulled into the dependency graph.
    with when("+sirius"):
        depends_on("sirius+fortran+shared")
        depends_on("sirius+cuda", when="+cuda")
        depends_on("sirius+rocm", when="+rocm")
        depends_on("sirius+openmp", when="+openmp")
        depends_on("sirius~openmp", when="~openmp")
        depends_on("sirius@7.3:", when="@9.1")
        depends_on("sirius@7.4:7.5", when="@2023.2")
        depends_on("sirius@7.5:", when="@2024.1:")
        depends_on("sirius@7.6: +pugixml", when="@2024.2:")
    with when("+libvori"):
        depends_on("libvori@201219:", when="@8.1")
        depends_on("libvori@210412:", when="@8.2:")
        depends_on("libvori@220621:", when="@2023.1:")

    # the bundled libcusmm uses numpy in the parameter prediction (v7+)
    # which is written using Python 3
    depends_on("py-numpy", when="@7:+cuda")
    depends_on("python@3.6:", when="@7:+cuda")
    depends_on("py-fypp")

    depends_on("spglib", when="+spglib")

    with when("build_system=cmake"):
        depends_on("cmake@3.22:", type="build")

        # DBCSR as external dependency
        depends_on("dbcsr@2.6: ~examples")
        depends_on("dbcsr+openmp", when="+openmp")
        depends_on("dbcsr+mpi", when="+mpi")
        depends_on("dbcsr+cuda", when="+cuda")
        depends_on("dbcsr+rocm", when="+rocm")
        depends_on("dbcsr smm=libxsmm", when="smm=libxsmm")
        depends_on("dbcsr smm=blas", when="smm=blas")

    with when("@2022: +rocm"):
        depends_on("hipblas")
        depends_on("hipfft")

    # The CMake build system and AOCC are not compatible as of AOCC 5
    requires("build_system=makefile", when="%aocc")

    # CP2K needs compiler specific compilation flags, e.g. optflags
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%nag")
    conflicts(
        "%aocc@:3.2",
        msg="Please use AOCC 4.0+ that better support modern Fortran features CP2K requires",
    )

    conflicts("~openmp", when="@8:", msg="Building without OpenMP is not supported in CP2K 8+")

    # We only support specific cuda_archs for which we have parameter files
    # for optimal kernels. Note that we don't override the cuda_archs property
    # from the parent class, since the parent class defines constraints for all
    # versions. Instead just mark all unsupported cuda archs as conflicting.

    supported_cuda_arch_list = ("35", "37", "60", "70", "80", "90")
    supported_rocm_arch_list = ("gfx906", "gfx908", "gfx90a", "gfx90a:xnack-", "gfx90a:xnack+")
    cuda_msg = "cp2k only supports cuda_arch {0}".format(supported_cuda_arch_list)
    rocm_msg = "cp2k only supports amdgpu_target {0}".format(supported_rocm_arch_list)

    conflicts("+cuda", when="cuda_arch=none")

    # ROCm already emits an error if +rocm amdgpu_target=none is given

    with when("+cuda"):
        for arch in CudaPackage.cuda_arch_values:
            if arch not in supported_cuda_arch_list:
                conflicts("+cuda", when="cuda_arch={0}".format(arch), msg=cuda_msg)

    with when("+rocm"):
        for arch in ROCmPackage.amdgpu_targets:
            if arch not in supported_rocm_arch_list:
                conflicts("+rocm", when="amdgpu_target={0}".format(arch), msg=rocm_msg)

    # Fix 2- and 3-center integral calls to libint
    patch(
        "https://github.com/cp2k/cp2k/commit/5eaf864ed2bd21fb1b05a9173bb77a815ad4deda.patch?full_index=1",
        sha256="3617abb877812c4b933f601438c70f95e21c6161bea177277b1d4125fd1c0bf9",
        when="@8.2",
    )

    # Patch for compilers with stricter C99 checks
    patch("posix_c_source.patch", when="@7.1%aocc@4.0:")
    patch("posix_c_source.patch", when="@7.1%gcc@13:")

    # Fix missing variable in OpenMP private clause
    patch(
        "https://github.com/cp2k/cp2k/commit/be86bd7f6cd6af7d68f8957dcdb67e7c3d586741.patch?full_index=1",
        sha256="1bb5a8e80603684a743e7821d24d41b31b60ccbb7d4257df1d2da53a3630e5bf",
        when="@2022.1:2022.2",
    )

    # Avoid using NULL() as subroutine argument as doing so breaks some versions of AOCC compiler
    # These patches backport 2023.x fixes to previous versions
    patch("backport_avoid_null_2022.x.patch", when="@2022.1:2022.2 %aocc@:4.0")
    patch("backport_avoid_null_9.1.patch", when="@9.1 %aocc@:4.0")

    patch("cmake-fixes-2023.2.patch", when="@2023.2 build_system=cmake")

    # Allow compilation with build_type=RelWithDebInfo and build_type=MinSizeRel
    # after NDEBUG support was dropped in https://github.com/cp2k/cp2k/pull/3172
    # The patch applies https://github.com/cp2k/cp2k/pull/3251 to version 2024.1
    patch("cmake-relwithdebinfo-2024.1.patch", when="@2024.1 build_system=cmake")

    # Bugfix for D4 dispersion correction in CP2K 2024.3
    # https://github.com/cp2k/cp2k/issues/3688
    patch("d4-dispersion-bugfix-2024.3.patch", when="@2024.3")

    # Fix segmentation faults caused by accessing unallocated arrays
    # https://github.com/cp2k/cp2k/pull/3733
    patch(
        "https://github.com/cp2k/cp2k/commit/7a99649828ecf7d5dc53d952a1bf7be6970deabe.patch?full_index=1",
        sha256="37f4f1a76634ff4a5617fe0c670e6acfe2afa2b2cfc5b2875e438a54baa4525e",
        when="@2024.2:2024.3",
    )

    def patch(self):
        # Patch for an undefined constant due to incompatible changes in ELPA
        if self.spec.satisfies("@9.1:2022.2 +elpa"):
            if self.spec["elpa"].satisfies("@2022.05.001:"):
                filter_file(
                    r"ELPA_2STAGE_REAL_INTEL_GPU",
                    "ELPA_2STAGE_REAL_INTEL_GPU_SYCL",
                    "src/fm/cp_fm_elpa.F",
                )

        # Patch for resolving .mod file conflicts in ROCm by implementing 'USE, INTRINSIC'
        if self.spec.satisfies("+rocm"):
            for directory, subdirectory, files in os.walk(os.getcwd()):
                for i in files:
                    file_path = os.path.join(directory, i)
                    filter_file("USE ISO_C_BINDING", "USE,INTRINSIC :: ISO_C_BINDING", file_path)
                    filter_file(
                        "USE ISO_FORTRAN_ENV", "USE,INTRINSIC :: ISO_FORTRAN_ENV", file_path
                    )
                    filter_file("USE omp_lib", "USE,INTRINSIC :: omp_lib", file_path)
                    filter_file("USE OMP_LIB", "USE,INTRINSIC :: OMP_LIB", file_path)
                    filter_file("USE iso_c_binding", "USE,INTRINSIC :: iso_c_binding", file_path)
                    filter_file(
                        "USE iso_fortran_env", "USE,INTRINSIC :: iso_fortran_env", file_path
                    )

    def url_for_version(self, version):
        url = "https://github.com/cp2k/cp2k/releases/download/v{0}/cp2k-{0}.tar.bz2"
        return url.format(version)


class MakefileBuilder(makefile.MakefileBuilder):
    def edit(self, pkg, spec, prefix):
        pkgconf = which("pkg-config")

        fftw = spec["fftw-api:openmp" if "+openmp" in spec else "fftw-api"]
        fftw_header_dir = fftw.headers.directories[0]

        # some providers (mainly Intel) keep the fftw headers in a subdirectory, find it
        for incdir in [join_path(f, "fftw") for f in fftw.headers.directories]:
            if os.path.exists(incdir):
                fftw_header_dir = incdir
                break

        optimization_flags = {
            "gcc": ["-O2", "-funroll-loops", "-ftree-vectorize"],
            "intel": ["-O2", "-pc64", "-unroll"],
            "nvhpc": ["-fast"],
            "cce": ["-O2"],
            "xl": ["-O3"],
            "aocc": ["-O2"],
            "rocmcc": ["-O1"],
        }

        dflags = ["-DNDEBUG"] if spec.satisfies("@:2023.2") else []
        if fftw.name in ("intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"):
            cppflags = ["-D__FFTW3_MKL", "-I{0}".format(fftw_header_dir)]
        else:
            cppflags = ["-D__FFTW3", "-I{0}".format(fftw_header_dir)]

        # CP2K requires MPI 3 starting at version 2023.1
        # and __MPI_VERSION is not supported anymore.
        if spec.satisfies("@:2022.2"):
            if spec.satisfies("^mpi@3:"):
                cppflags.append("-D__MPI_VERSION=3")
            elif spec.satisfies("^mpi@2:"):
                cppflags.append("-D__MPI_VERSION=2")

        cflags = optimization_flags[spec.compiler.name][:]
        cxxflags = optimization_flags[spec.compiler.name][:]
        fcflags = optimization_flags[spec.compiler.name][:]
        nvflags = ["-O3"]
        ldflags = []
        libs = []

        # CP2K Makefile doesn't set C standard
        if spec.satisfies("@2023.2:"):
            # Use of DBL_DECIMAL_DIG
            cflags.append(pkg.compiler.c11_flag)
        else:
            # C99-style for-loops with inline definition of iterating variable.
            cflags.append(pkg.compiler.c99_flag)

        if spec.satisfies("%intel"):
            cflags.append("-fp-model precise")
            cxxflags.append("-fp-model precise")
            fcflags += ["-fp-model precise", "-heap-arrays 64", "-g", "-traceback"]
        elif spec.satisfies("%gcc"):
            fcflags += [
                "-ffree-form",
                "-ffree-line-length-none",
                "-ggdb",  # make sure we get proper Fortran backtraces
            ]
        elif spec.satisfies("%aocc") or spec.satisfies("%rocmcc"):
            fcflags += ["-ffree-form", "-Mbackslash"]
        elif spec.satisfies("%nvhpc"):
            fcflags += ["-Mfreeform", "-Mextend"]
        elif spec.satisfies("%cce"):
            fcflags += ["-emf", "-ffree", "-hflex_mp=strict"]
        elif spec.satisfies("%xl"):
            fcflags += ["-qpreprocess", "-qstrict", "-q64"]
            ldflags += ["-Wl,--allow-multiple-definition"]

        if "%gcc@10: +mpi" in spec and spec["mpi"].name in ["mpich", "cray-mpich"]:
            fcflags += [
                "-fallow-argument-mismatch"
            ]  # https://github.com/pmodels/mpich/issues/4300
        if spec.satisfies("@7.1%gcc@13:"):
            fcflags.append("-fallow-argument-mismatch")

        if spec.satisfies("+openmp"):
            cflags.append(pkg.compiler.openmp_flag)
            cxxflags.append(pkg.compiler.openmp_flag)
            fcflags.append(pkg.compiler.openmp_flag)
            ldflags.append(pkg.compiler.openmp_flag)
            nvflags.append('-Xcompiler="{0}"'.format(pkg.compiler.openmp_flag))
        elif spec.satisfies("%cce"):  # Cray enables OpenMP by default
            cflags += ["-hnoomp"]
            cxxflags += ["-hnoomp"]
            fcflags += ["-hnoomp"]
            ldflags += ["-hnoomp"]

        if spec.satisfies("@7:"):  # recent versions of CP2K use C++14 CUDA code
            cxxflags.append(pkg.compiler.cxx14_flag)
            nvflags.append(pkg.compiler.cxx14_flag)

        ldflags.append(fftw.libs.search_flags)

        if spec.satisfies("^superlu-dist@4.3"):
            ldflags.insert(0, "-Wl,--allow-multiple-definition")

        if spec.satisfies("+libint"):
            cppflags += ["-D__LIBINT"]

            if spec.satisfies("@:6.9"):
                cppflags += ["-D__LIBINT_MAX_AM=6", "-D__LIBDERIV_MAX_AM1=5"]

                # libint-1.x.y has to be linked statically to work around
                # inconsistencies in its Fortran interface definition
                # (short-int vs int) which otherwise causes segfaults at
                # runtime due to wrong offsets into the shared library
                # symbols.
                libs += [
                    join_path(spec["libint"].libs.directories[0], "libderiv.a"),
                    join_path(spec["libint"].libs.directories[0], "libint.a"),
                ]

            else:
                fcflags += pkgconf("--cflags", "libint2", output=str).split()
                libs += pkgconf("--libs", "libint2", output=str).split()

        if spec.satisfies("+libxc"):
            cppflags += ["-D__LIBXC"]

            if spec.satisfies("@:6.9"):
                libxc = spec["libxc:fortran,static"]
                cppflags += [libxc.headers.cpp_flags]
                ldflags.append(libxc.libs.search_flags)
                libs.append(str(libxc.libs))
            else:
                fcflags += pkgconf("--cflags", "libxcf03", output=str).split()
                # some Fortran functions seem to be direct wrappers of the
                # C functions such that we get a direct dependency on them,
                # requiring `-lxc` to be present in addition to `-lxcf03`
                libs += pkgconf("--libs", "libxcf03", "libxc", output=str).split()

        if spec.satisfies("+pexsi"):
            cppflags.append("-D__LIBPEXSI")
            fcflags.append("-I" + join_path(spec["pexsi"].prefix, "fortran"))
            libs += [
                join_path(spec["pexsi"].libs.directories[0], "libpexsi.a"),
                join_path(spec["superlu-dist"].libs.directories[0], "libsuperlu_dist.a"),
                join_path(
                    spec["parmetis"].libs.directories[0], "libparmetis.{0}".format(dso_suffix)
                ),
                join_path(spec["metis"].libs.directories[0], "libmetis.{0}".format(dso_suffix)),
            ]

        if spec.satisfies("+elpa"):
            elpa = spec["elpa"]
            elpa_suffix = "_openmp" if "+openmp" in elpa else ""
            elpa_incdir = elpa.headers.directories[0]

            fcflags += ["-I{0}".format(join_path(elpa_incdir, "modules"))]

            # Currently AOCC support only static libraries of ELPA
            if spec.satisfies("%aocc"):
                libs.append(
                    join_path(
                        elpa.prefix.lib, ("libelpa{elpa_suffix}.a".format(elpa_suffix=elpa_suffix))
                    )
                )
            else:
                libs.append(elpa.libs.ld_flags)

            if spec.satisfies("@:4"):
                if elpa.satisfies("@:2014.5"):
                    cppflags.append("-D__ELPA")
                elif elpa.satisfies("@2014.6:2015.10"):
                    cppflags.append("-D__ELPA2")
                else:
                    cppflags.append("-D__ELPA3")
            else:
                cppflags.append(
                    "-D__ELPA={0}{1:02d}".format(elpa.version[0], int(elpa.version[1]))
                )
                fcflags += ["-I{0}".format(join_path(elpa_incdir, "elpa"))]

            if "+cuda" in spec and "+cuda" in elpa:
                cppflags += ["-D__ELPA_NVIDIA_GPU"]

        if spec.satisfies("+sirius"):
            sirius = spec["sirius"]
            cppflags.append("-D__SIRIUS")
            fcflags += ["-I{0}".format(sirius.prefix.include.sirius)]
            libs += list(sirius.libs)

        if spec.satisfies("+plumed"):
            dflags.extend(["-D__PLUMED2"])
            cppflags.extend(["-D__PLUMED2"])
            libs += [join_path(spec["plumed"].prefix.lib, "libplumed.{0}".format(dso_suffix))]

        if spec.satisfies("+libvori"):
            cppflags += ["-D__LIBVORI"]
            libvori = spec["libvori"].libs
            ldflags += [libvori.search_flags]
            libs.append(libvori.ld_flags)
            libs += ["-lstdc++"]

        if spec.satisfies("+spglib"):
            cppflags += ["-D__SPGLIB"]
            spglib = spec["spglib"].libs
            ldflags += [spglib.search_flags]
            libs.append(spglib.ld_flags)

        cc = spack_cc if "~mpi" in spec else spec["mpi"].mpicc
        cxx = spack_cxx if "~mpi" in spec else spec["mpi"].mpicxx
        fc = spack_fc if "~mpi" in spec else spec["mpi"].mpifc

        # Intel
        if spec.satisfies("%intel"):
            cppflags.extend(["-D__INTEL", "-D__HAS_ISO_C_BINDING", "-D__USE_CP2K_TRACE"])
            fcflags.extend(["-diag-disable 8290,8291,10010,10212,11060", "-free", "-fpp"])

        # FFTW, LAPACK, BLAS
        lapack = spec["lapack"].libs
        blas = spec["blas"].libs
        ldflags.append((lapack + blas).search_flags)
        libs += [str(x) for x in (fftw.libs, lapack, blas)]

        if spec.satisfies("platform=darwin"):
            cppflags.extend(["-D__NO_STATM_ACCESS"])

        if spec["blas"].name in ("intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"):
            cppflags += ["-D__MKL"]
        elif spec["blas"].name == "accelerate":
            cppflags += ["-D__ACCELERATE"]

        if spec.satisfies("+cosma"):
            # add before ScaLAPACK to override the p?gemm symbols
            cosma = spec["cosma"].libs
            ldflags.append(cosma.search_flags)
            libs += cosma

        # MPI
        if spec.satisfies("+mpi"):
            cppflags.extend(["-D__parallel", "-D__SCALAPACK"])

            if spec["mpi"].name == "intel-oneapi-mpi":
                mpi = [join_path(spec["intel-oneapi-mpi"].libs.directories[0], "libmpi.so")]
            else:
                mpi = spec["mpi:cxx"].libs

            # while intel-mkl has a mpi variant and adds the scalapack
            # libs to its libs, intel-oneapi-mkl does not.
            if spec["scalapack"].name == "intel-oneapi-mkl":
                mpi_impl = "openmpi" if spec["mpi"].name in ["openmpi", "hpcx-mpi"] else "intelmpi"
                scalapack = [
                    join_path(
                        spec["intel-oneapi-mkl"].libs.directories[0], "libmkl_scalapack_lp64.so"
                    ),
                    join_path(
                        spec["intel-oneapi-mkl"].libs.directories[0],
                        "libmkl_blacs_{0}_lp64.so".format(mpi_impl),
                    ),
                ]
            else:
                scalapack = spec["scalapack"].libs
                ldflags.append(scalapack.search_flags)

            libs += scalapack
            libs += mpi
            libs += pkg.compiler.stdcxx_libs

            if spec.satisfies("+mpi_f08"):
                cppflags.append("-D__MPI_F08")

            if spec.satisfies("^wannier90"):
                cppflags.append("-D__WANNIER90")
                wannier = join_path(spec["wannier90"].libs.directories[0], "libwannier.a")
                libs.append(wannier)

        gpuver = ""
        if spec.satisfies("+cuda"):
            libs += [
                "-L{}".format(spec["cuda"].libs.directories[0]),
                "-L{}/stubs".format(spec["cuda"].libs.directories[0]),
                "-lcuda",
                "-lcudart",
                "-lnvrtc",
                "-lstdc++",
            ]

            if spec.satisfies("@9:"):
                if spec.satisfies("@2022:"):
                    cppflags += ["-D__OFFLOAD_CUDA"]

                acc_compiler_var = "OFFLOAD_CC"
                acc_flags_var = "OFFLOAD_FLAGS"
                cppflags += ["-D__DBCSR_ACC", "-D__GRID_CUDA", "-DOFFLOAD_TARGET=cuda"]
                libs += ["-lcublas"]

                if spec.satisfies("+cuda_fft"):
                    if spec.satisfies("@:9"):
                        cppflags += ["-D__PW_CUDA"]

                    libs += ["-lcufft"]
                else:
                    if spec.satisfies("@2022:"):
                        cppflags += ["-D__NO_OFFLOAD_PW"]
            else:
                acc_compiler_var = "NVCC"
                acc_flags_var = "NVFLAGS"
                cppflags += ["-D__ACC"]
                if spec.satisfies("+cuda_blas"):
                    cppflags += ["-D__DBCSR_ACC=2"]
                    libs += ["-lcublas"]
                else:
                    cppflags += ["-D__DBCSR_ACC"]

                if spec.satisfies("+cuda_fft"):
                    cppflags += ["-D__PW_CUDA"]
                    libs += ["-lcufft", "-lcublas"]

            cuda_arch = spec.variants["cuda_arch"].value[0]
            gpuver = GPU_MAP[cuda_arch]
            if cuda_arch == "35" and spec.satisfies("+cuda_arch_35_k20x"):
                gpuver = "K20X"

        if spec.satisfies("@2022: +rocm"):
            libs += [
                "-L{}".format(spec["hip"].prefix.lib),
                "-lamdhip64",
                "-lhipblas",
                "-lhipfft",
                "-lstdc++",
            ]

            acc_compiler_var = "hipcc"
            acc_flags_var = "NVFLAGS"
            cppflags += ["-D__ACC"]
            cppflags += ["-D__DBCSR_ACC"]
            cppflags += ["-D__HIP_PLATFORM_AMD__"]
            cppflags += ["-D__GRID_HIP"]

            gpuver = GPU_MAP[spec.variants["amdgpu_target"].value[0]]

        if spec.satisfies("smm=libsmm"):
            lib_dir = join_path("lib", self.makefile_architecture, self.makefile_version)
            mkdirp(lib_dir)
            try:
                copy(env["LIBSMM_PATH"], join_path(lib_dir, "libsmm.a"))
            except KeyError:
                raise KeyError(
                    "Point environment variable LIBSMM_PATH to "
                    "the absolute path of the libsmm.a file"
                )
            except IOError:
                raise IOError(
                    "The file LIBSMM_PATH pointed to does not "
                    "exist. Note that it must be absolute path."
                )
            cppflags.extend(["-D__HAS_smm_dnn", "-D__HAS_smm_vec"])
            libs.append("-lsmm")

        elif spec.satisfies("smm=libxsmm"):
            cppflags += ["-D__LIBXSMM"]
            cppflags += pkgconf("--cflags-only-other", "libxsmmf", output=str).split()
            fcflags += pkgconf("--cflags-only-I", "libxsmmf", output=str).split()
            libs += pkgconf("--libs", "libxsmmf", output=str).split()

        dflags.extend(cppflags)
        cflags.extend(cppflags)
        cxxflags.extend(cppflags)
        fcflags.extend(cppflags)
        nvflags.extend(cppflags)

        with open(self.makefile, "w") as mkf:
            if spec.satisfies("+plumed"):
                mkf.write(
                    "# include Plumed.inc as recommended by"
                    "PLUMED to include libraries and flags"
                )
                mkf.write("include {0}\n".format(self.pkg["plumed"].plumed_inc))

            mkf.write("\n# COMPILER, LINKER, TOOLS\n\n")
            mkf.write(
                "FC  = {0}\n" "CC  = {1}\n" "CXX = {2}\n" "LD  = {3}\n".format(fc, cc, cxx, fc)
            )

            if spec.satisfies("%intel"):
                intel_bin_dir = ancestor(pkg.compiler.cc)
                # CPP is a commented command in Intel arch of CP2K
                # This is the hack through which cp2k developers avoid doing :
                #
                # ${CPP} <file>.F > <file>.f90
                #
                # and use `-fpp` instead
                mkf.write("CPP = # {0} -P\n".format(spack_cc))
                mkf.write("AR  = {0}/xiar -qs\n".format(intel_bin_dir))
            else:
                mkf.write("CPP = # {0} -E\n".format(spack_cc))
                mkf.write("AR  = ar -qs\n")  # r = qs is a GNU extension

            if spec.satisfies("+cuda"):
                mkf.write(
                    "{0} = {1}\n".format(
                        acc_compiler_var, join_path(spec["cuda"].prefix, "bin", "nvcc")
                    )
                )

            # Write compiler flags to file
            def fflags(var, lst):
                return "{0} = {1}\n\n".format(var, " \\\n\t".join(lst))

            mkf.write("\n# FLAGS & LIBRARIES\n")
            mkf.write(fflags("DFLAGS", dflags))
            mkf.write(fflags("CPPFLAGS", cppflags))
            mkf.write(fflags("CFLAGS", cflags))
            mkf.write(fflags("CXXFLAGS", cxxflags))
            if spec.satisfies("+cuda"):
                mkf.write(fflags(acc_flags_var, nvflags))
            if "+rocm" in spec:
                mkf.write("OFFLOAD_TARGET = hip\n")

            mkf.write(fflags("FCFLAGS", fcflags))
            mkf.write(fflags("LDFLAGS", ldflags))
            mkf.write(fflags("LIBS", libs))

            if spec.satisfies("%intel"):
                mkf.write(fflags("LDFLAGS_C", ldflags + ["-nofor-main"]))

            if spec.satisfies("%aocc@5:"):
                # ensure C based applications can be build properly
                mkf.write(fflags("LDFLAGS_C", ldflags + ["-fno-fortran-main"]))
                # This flag is required for the correct runtime behaviour of the code with aocc@5.0
                mkf.write(fflags("FCFLAGS", fcflags + ["-mllvm -enable-newgvn=true"]))

            mkf.write("# CP2K-specific flags\n\n")
            mkf.write("GPUVER = {0}\n".format(gpuver))
            mkf.write("DATA_DIR = {0}\n".format(prefix.share.data))

    def build(self, pkg, spec, prefix):
        if "+cuda" in spec and len(spec.variants["cuda_arch"].value) > 1:
            raise InstallError("cp2k supports only one cuda_arch at a time")

        # Apparently the Makefile bases its paths on PWD
        # so we need to set PWD = self.build_directory
        with spack.util.environment.set_env(PWD=self.build_directory):
            super().build(pkg, spec, prefix)

            with working_dir(self.build_directory):
                make("libcp2k", *self.build_targets)

    def install(self, pkg, spec, prefix):
        exe_dir = join_path("exe", self.makefile_architecture)
        lib_dir = join_path("lib", self.makefile_architecture, self.makefile_version)

        install_tree(exe_dir, self.prefix.bin)
        install_tree("data", self.prefix.share.data)
        install_tree(lib_dir, self.prefix.lib)

        mkdirp(self.prefix.include)
        install("src/start/libcp2k.h", join_path(self.prefix.include, "libcp2k.h"))

    @property
    def build_directory(self):
        build_dir = self.pkg.stage.source_path

        if self.spec.satisfies("@:6"):
            # prior to version 7.1 was the Makefile located in makefiles/
            build_dir = join_path(build_dir, "makefiles")

        return build_dir

    @property
    def build_targets(self):
        return [
            "ARCH={0}".format(self.makefile_architecture),
            "VERSION={0}".format(self.makefile_version),
        ]

    @property
    def makefile(self):
        makefile_basename = ".".join([self.makefile_architecture, self.makefile_version])
        return join_path("arch", makefile_basename)

    @property
    def makefile_architecture(self):
        return "{0.architecture}-{0.compiler.name}".format(self.spec)

    @property
    def makefile_version(self):
        return "{prefix}{suffix}".format(
            prefix="p" if "+mpi" in self.spec else "s",
            suffix="smp" if "+openmp" in self.spec else "opt",
        )

    @property
    def archive_files(self):
        return [join_path(self.pkg.stage.source_path, self.makefile)]

    def check(self):
        data_dir = join_path(self.pkg.stage.source_path, "data")

        # CP2K < 7 still uses $PWD to detect the current working dir
        # and Makefile is in a subdir, account for both facts here:
        with spack.util.environment.set_env(CP2K_DATA_DIR=data_dir, PWD=self.build_directory):
            with working_dir(self.build_directory):
                make("test", *self.build_targets)

    @run_after("install", when="@9.1:")
    def fix_package_config(self):
        """
        Default build procedure generates libcp2k.pc with invalid paths,
        because they are collected from temporary directory.

        Ignoring invalid paths, most library-related switches are correct
        except for fftw and openblas.

        This procedure is appending two missing switches (tested with GROMACS 2022.2 + CP2K).

        In case such approach causes issues in the future, it might be necessary
        to generate and override entire libcp2k.pc.
        """
        pkgconfig_file = join_path(self.prefix.lib.pkgconfig, "libcp2k.pc")
        filter_file(r"(^includedir=).*", r"\1{0}".format(self.prefix.include), pkgconfig_file)
        filter_file(r"(^libdir=).*", r"\1{0}".format(self.prefix.lib), pkgconfig_file)

        with open(pkgconfig_file, "r+") as handle:
            content = handle.read().rstrip()

            content += " " + self.spec["blas"].libs.ld_flags
            content += " " + self.spec["lapack"].libs.ld_flags
            content += " " + self.spec["fftw-api"].libs.ld_flags

            fftw = self.spec["fftw-api"]
            if fftw.name in ["fftw", "amdfftw", "cray-fftw"] and fftw.satisfies("+openmp"):
                content += " -lfftw3_omp"

            content += "\n"

            handle.seek(0)
            handle.write(content)


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("+cuda"):
            if (len(spec.variants["cuda_arch"].value) > 1) or spec.satisfies("cuda_arch=none"):
                raise InstallError("CP2K supports only one cuda_arch at a time.")
            else:
                gpu_ver = GPU_MAP[spec.variants["cuda_arch"].value[0]]
                args += [
                    self.define("CP2K_USE_ACCEL", "CUDA"),
                    self.define("CP2K_WITH_GPU", gpu_ver),
                ]

        if spec.satisfies("+rocm"):
            if len(spec.variants["amdgpu_target"].value) > 1:
                raise InstallError("CP2K supports only one amdgpu_target at a time.")
            else:
                gpu_ver = GPU_MAP[spec.variants["amdgpu_target"].value[0]]
                args += [
                    self.define("CP2K_USE_ACCEL", "HIP"),
                    self.define("CP2K_WITH_GPU", gpu_ver),
                ]

        args += [
            self.define_from_variant("CP2K_ENABLE_REGTESTS", "enable_regtests"),
            self.define_from_variant("CP2K_USE_ELPA", "elpa"),
            self.define_from_variant("CP2K_USE_DLAF", "dlaf"),
            self.define_from_variant("CP2K_USE_LIBINT2", "libint"),
            self.define_from_variant("CP2K_USE_SIRIUS", "sirius"),
            self.define_from_variant("CP2K_USE_SPLA", "spla"),
            self.define_from_variant("CP2K_USE_COSMA", "cosma"),
            self.define_from_variant("CP2K_USE_LIBXC", "libxc"),
            self.define_from_variant("CP2K_USE_LIBTORCH", "pytorch"),
            self.define_from_variant("CP2K_USE_METIS", "pexsi"),
            self.define_from_variant("CP2K_USE_SUPERLU", "pexsi"),
            self.define_from_variant("CP2K_USE_PLUMED", "plumed"),
            self.define_from_variant("CP2K_USE_SPGLIB", "spglib"),
            self.define_from_variant("CP2K_USE_VORI", "libvori"),
            self.define_from_variant("CP2K_USE_SPLA", "spla"),
            self.define_from_variant("CP2K_USE_QUIP", "quip"),
            self.define_from_variant("CP2K_USE_MPI_F08", "mpi_f08"),
        ]

        # we force the use elpa openmp threading support. might need to be revisited though
        args += [
            self.define(
                "CP2K_ENABLE_ELPA_OPENMP_SUPPORT",
                ("+elpa +openmp" in spec) or ("^elpa +openmp" in spec),
            )
        ]

        if "spla" in spec and (spec.satisfies("+cuda") or spec.satisfies("+rocm")):
            args += ["-DCP2K_USE_SPLA_GEMM_OFFLOADING=ON"]

        args += ["-DCP2K_USE_FFTW3=ON"]

        if spec.satisfies("smm=libxsmm"):
            args += ["-DCP2K_USE_LIBXSMM=ON"]
        else:
            args += ["-DCP2K_USE_LIBXSMM=OFF"]

        lapack = spec["lapack"]
        blas = spec["blas"]

        if blas.name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            args += ["-DCP2K_BLAS_VENDOR=MKL"]
            if sys.platform == "darwin":
                args += [
                    self.define("CP2K_BLAS_VENDOR", "CUSTOM"),
                    self.define("CP2K_SCALAPACK_VENDOR", "GENERIC"),
                    self.define(
                        "CP2K_SCALAPACK_LINK_LIBRARIES", spec["scalapack"].libs.joined(";")
                    ),
                ]
            else:
                args += ["-DCP2K_SCALAPACK_VENDOR=MKL"]
        else:
            args.extend(
                [
                    self.define("CP2K_LAPACK_FOUND", True),
                    self.define("CP2K_LAPACK_LINK_LIBRARIES", lapack.libs.joined(";")),
                    self.define("CP2K_BLAS_FOUND", True),
                    self.define("CP2K_BLAS_LINK_LIBRARIES", blas.libs.joined(";")),
                    self.define("CP2K_SCALAPACK_FOUND", True),
                    self.define("CP2K_SCALAPACK_INCLUDE_DIRS", spec["scalapack"].prefix.include),
                    self.define("CP2K_BLAS_VENDOR", "CUSTOM"),
                    self.define("CP2K_SCALAPACK_VENDOR", "GENERIC"),
                    self.define(
                        "CP2K_SCALAPACK_LINK_LIBRARIES", spec["scalapack"].libs.joined(";")
                    ),
                ]
            )

        return args
