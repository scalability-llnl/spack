# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.hooks.sbang as sbang
from spack.package import *


class Phist(CMakePackage):
    """The Pipelined, Hybrid-parallel Iterative Solver Toolkit provides
    implementations of and interfaces to block iterative solvers for sparse
    linear and eigenvalue problems. In contrast to other libraries we support
    multiple backends (e.g. Trilinos, PETSc and our own optimized kernels),
    and interfaces in multiple languages such as C, C++, Fortran 2003 and
    Python. PHIST has a clear focus on portability and hardware performance:
    in particular support row-major storage of block vectors and using GPUs
    (via the ghost library or Trilinos/Tpetra).
    """

    homepage = "https://bitbucket.org/essex/phist/"
    url = "https://bitbucket.org/essex/phist/get/phist-1.12.1.tar.gz"
    git = "https://bitbucket.org/essex/phist.git"

    maintainers("jthies")
    tags = ["e4s"]

    # phist is a required part of spack GitLab CI pipelines. In them, mpich is requested
    # to provide 'mpi' like this: spack install phist ^mpich %gcc@7.5.0
    # Failure of this command to succeed breaks spack's gitlab CI pipelines!

    license("BSD-3-Clause")

    version("develop", branch="devel")
    version("master", branch="master")

    # fixes for tpetra/ghost, clang/Intel-LLVM
    version("1.12.1", sha256="6b8fe8a994bf6baf698aa691fc2cbecd62cc60219073e48bfe6fd954c0303b9f")

    # compatible with trilinos@14:
    version("1.12.0", sha256="0f02e39b16d14cf7c47a3c468e788c7c0e71857eb1c0a4edb601e1e5b67e8668")

    # compatible with python@3.11: and cray-libsci as BLAS/LAPACK provider
    version("1.11.2", sha256="e23f76307c26b930f7331a734b0a864ea6d7fb4a13c12f3c5d70c2c41481747b")

    # updated lapack interface to work with openblas and netlib-lapack
    version("1.11.0", sha256="36e6cc41a13884ba0a26f7be03e3f1882b1a2d14ca04353a609c0eec0cfb7a77")

    # updated the Trilinos interface to work with trilinos@13:
    # without using deprecated interfaces in tpetra
    version("1.10.0", sha256="3ec660c85d37818ee219edc80e977140dfb062bdca1f38623c94a45d13634bd1")

    # phist-1.9.6 updated from the older "use mpi" to the newer "use mpi_f08" (MPI3.1):
    # The motivation was fixing it on Cray: https://github.com/spack/spack/issues/26002
    # Documentation: https://www.mpi-forum.org/docs/mpi-3.1/mpi31-report/node408.htm
    # mpich does not provide mpi_f08.mod with gfortran-[789], it needs gfortran>=10:
    # https://stackoverflow.com/questions/65750862
    version("1.9.6", sha256="98ed5ccb22bb98d5b6bf9de0c9960105473e5244978853070b9a3c44138db662")

    version("1.9.5", sha256="24faa3373003f185c82a658c510e36cba9acc4110eb60cbfded9de370ae9ea32")
    version("1.9.4", sha256="9dde3ca0480358fa0877ec8424aaee4011c5defc929219a5930388a7cdb4c8a6")
    version("1.9.3", sha256="3ab7157e9f535a4c8537846cb11b516271ef13f82d0f8ebb7f96626fb9ab86cf")
    version("1.9.2", sha256="289678fa7172708f5d32d6bd924c8fdfe72b413bba5bbb8ce6373c85c5ec5ae5")
    version("1.9.1", sha256="6e6411115ec48afe605b4f2179e9bc45d60f15459428f474f3f32b80d2830f1f")
    version("1.9.0", sha256="990d3308fc0083ed0f9f565d00c649ee70c3df74d44cbe5f19dfe05263d06559")
    version("1.8.0", sha256="ee42946bce187e126452053b5f5c200b57b6e40ee3f5bcf0751f3ced585adeb0")
    version("1.7.5", sha256="f11fe27f2aa13d69eb285cc0f32c33c1603fa1286b84e54c81856c6f2bdef500")
    version("1.7.4", sha256="c5324f639b8c95b07cd29c3cd8dd7dd576c84a0b9228dbb88f8b87605424419e")
    version("1.7.3", sha256="ab2d853c9ba13bcd3069fcc61c359cb412466a2e4b22ebbd2f5263cffa685126")
    version("1.7.2", sha256="29b504d78b5efd57b87d2ca6e20bc8a32b1ba55b40f5a5b7189cc0d28e43bcc0")
    version("1.6.1", sha256="4ed4869f24f920a494aeae0f7d1d94fe9efce55ebe0d298a5948c9603e07994d")
    version("1.6.0", sha256="667a967b37d248242c275226c96efc447ef73a2b15f241c6a588d570d7fac07b")
    version("1.4.3", sha256="9cc1c7ba7f7a04e94f4497da14199e4631a0d02d0e4187f3e16f4c242dc777c1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        name="kernel_lib",
        default="builtin",
        description="select the kernel library (backend) for phist",
        values=["builtin", "epetra", "tpetra", "petsc", "eigen", "ghost"],
    )

    variant(name="int64", default=True, description="Use 64-bit global indices.")

    variant(
        name="outlev",
        default="2",
        values=["0", "1", "2", "3", "4", "5"],
        description="verbosity. 0: errors 1: +warnings 2: +info "
        "3: +verbose 4: +extreme 5: +debug",
    )

    variant(
        "host",
        default=True,
        description="allow PHIST to use compiler flags that lead to host-"
        "specific code. Set this to False when cross-compiling.",
    )

    variant("shared", default=True, description="Enables the build of shared libraries")

    variant(
        "mpi",
        default=True,
        description="enable/disable MPI (note that the kernel library may "
        "not support this choice)",
    )

    variant("openmp", default=True, description="enable/disable OpenMP")

    variant(
        "parmetis",
        default=False,
        description="enable/disable ParMETIS partitioning (only actually "
        "used with kernel_lib=builtin)",
    )

    variant(
        "scamac",
        default=True,
        description='enable/disable building the "SCAlable MAtrix '
        'Collection" matrix generators.',
    )

    variant(
        "trilinos",
        default=False,
        description="enable/disable Trilinos third-party libraries. "
        "For all kernel_libs, we can use Belos and Anasazi "
        "iterative solvers. For the Trilinos backends "
        "(kernel_lib=epetra|tpetra) we can use preconditioner "
        "packages such as Ifpack, Ifpack2 and ML.",
    )

    variant(
        "fortran",
        default=True,
        description="generate Fortran 2003 bindings (requires Python3 and " "a Fortran compiler)",
    )

    # Build error with LLVM and recent Trilinos, fixed in phist-1.12.1
    conflicts("%clang", when="kernel_lib=tpetra @:1.12.0")
    conflicts("%oneapi", when="kernel_lib=tpetra @:1.12.0")
    # Trilinos 14 had some tpetra/kokkos API changes that are reflected in the phist 1.12 tag
    conflicts("^trilinos@14:", when="@:1.11.2")
    # Build error with cray-libsci because they define macro 'I', workaround in phist-1.11.2
    conflicts("^cray-libsci", when="@:1.11.1")
    # phist@1.11.2 got rid of some deprecated python code + a patch below
    conflicts("^python@3.11:", when="@:1.11.1")
    # The builtin kernels switched from the 'mpi' to the 'mpi_f08' module in
    # phist 1.9.6, which causes compile-time errors with mpich and older
    # GCC versions.
    conflicts("kernel_lib=builtin", when="@1.9.6: ^mpich %gcc@:10")
    # in older versions, it is not possible to completely turn off OpenMP
    conflicts("~openmp", when="@:1.7.3")
    # in older versions, it is not possible to turn off the use of host-
    # specific compiler flags in Release mode.
    conflicts("~host", when="@:1.7.3")
    # builtin always uses 64-bit indices
    conflicts("~int64", when="kernel_lib=builtin")
    conflicts("+int64", when="kernel_lib=eigen")

    # ###################### Patches ##########################

    # remove 'rU' file mode in a python script
    patch("remove_rU_mode_in_python_script.patch", when="@:1.12.0 +fortran ^python@3.11:")
    # Avoid trying to compile some SSE code if SSE is not available
    # This patch will be part of phist 1.11.3 and greater and only affects
    # the 'builtin' kernel_lib.
    patch("avoid-sse.patch", when="@:1.11.2 kernel_lib=builtin")
    # Only applies to 1.9.4: While SSE instructions are handled correctly,
    # build fails on ppc64le unless -DNO_WARN_X86_INTRINSICS is defined.
    patch("ppc64_sse.patch", when="@1.9.4")
    patch("update_tpetra_gotypes.patch", when="@1.6:1.8")
    patch("sbang.patch", when="+fortran")
    patch("fortran-fixes-pre-1.11.patch", when="+fortran @1.7.0:1.10.0")
    patch("lapack-fixes-pre-1.11.patch", when="@:1.10.0")

    # ###################### Dependencies ##########################

    depends_on("cmake@3.8:", type="build")
    depends_on("blas")
    depends_on("lapack")
    # Python 3 or later is required for generating the Fortran 2003 bindings
    # since version 1.7, you can get rid of the dependency by switching off
    # the feature (e.g. use the '~fortran' variant)
    depends_on("python@3:", when="@1.7: +fortran", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("trilinos@12:+tpetra gotype=long_long", when="kernel_lib=tpetra +int64")
    depends_on("trilinos@12:+tpetra gotype=int", when="kernel_lib=tpetra ~int64")
    # Epetra backend also works with older Trilinos versions
    depends_on("trilinos+epetra", when="kernel_lib=epetra")
    depends_on("petsc +int64", when="kernel_lib=petsc +int64")
    depends_on("petsc ~int64", when="kernel_lib=petsc ~int64")
    depends_on("eigen", when="kernel_lib=eigen")
    depends_on("ghost", when="kernel_lib=ghost")

    depends_on("trilinos+anasazi+belos", when="+trilinos")
    depends_on("parmetis+int64", when="+parmetis+int64")
    depends_on("parmetis~int64", when="+parmetis~int64")
    depends_on("py-pytest", type="test")
    depends_on("py-numpy", type="test", when="+mpi")
    # The test_install compiles the examples and needs pkgconfig for it
    depends_on("pkgconfig", type="test")

    # in 1.10 we removed some use of deprecated Trilinos interfaces
    # (some functions in tpetra were renamed)
    conflicts("^trilinos@13.4:", when="@:1.9 kernel_lib=tpetra")
    conflicts("^trilinos@:13.2", when="@1.10: kernel_lib=tpetra")

    # Fortran 2003 bindings were included in version 1.7, previously they
    # required a separate package
    conflicts("+fortran", when="@:1.6")

    # older gcc's may produce incorrect SIMD code and fail
    # to compile some OpenMP statements
    conflicts("%gcc@:4.9.1")
    # gcc@10: Error: Rank mismatch between actual argument at (1)
    # and actual argument at (2) (scalar and rank-1)
    conflicts("%gcc@10:", when="@:1.9.0")

    # the phist repo came with it's own FindMPI.cmake before, which may cause some other
    # MPI installation to be used than the one spack wants.
    def patch(self):
        if self.spec.satisfies("@1.9.6:1.10.0"):
            filter_file("USE mpi", "use mpi_f08", "src/kernels/builtin/crsmat_module.F90")
            # filter_file('use mpi', 'use mpi_f08', -> Needs more fixes
            #            'fortran_bindings/phist_testing.F90')
            # These are not needed for the build but as a reminder to be consistent:
            filter_file("use mpi", "use mpi_f08", "fortran_bindings/test/core.F90")
            filter_file("use mpi", "use mpi_f08", "fortran_bindings/test/jada.F90")
            filter_file("use mpi", "use mpi_f08", "fortran_bindings/test/kernels.F90")

            if "^mpich" in self.spec and self.spec.satisfies("%gcc@:9"):
                raise InstallError("PR 26773: gcc<10 can't build phist>1.9.5 w/ ^mpich")
        if self.spec.satisfies("@:1.9.5"):
            # Tag '1.9.5' has moved to an older commit later without fixing the version:
            filter_file("VERSION_PATCH 4", "VERSION_PATCH 5", "CMakeLists.txt")
            force_remove("cmake/FindMPI.cmake")
        # mpiexec -n12 puts a lot of stress on a pod and gets stuck in a loop very often
        test = FileFilter("CMakeLists.txt")
        test.filter("1 2 3 12", "1 2 3")
        test.filter("12/", "6/")
        test.filter("TEST_DRIVERS_NUM_THREADS 6", "TEST_DRIVERS_NUM_THREADS 3")
        # Avoid finding external modules like:
        #    /opt/rocm/llvm/include/iso_fortran_env.mod
        filter_file(
            "use iso_fortran_env",
            "use, intrinsic :: iso_fortran_env",
            "drivers/matfuncs/matpde3d.F90",
        )

    def setup_build_environment(self, env):
        env.set("SPACK_SBANG", sbang.sbang_install_path())

    def cmake_args(self):
        spec = self.spec
        define = self.define

        if spec.satisfies("kernel_lib=builtin") and spec.satisfies("~mpi"):
            raise InstallError("~mpi not possible with kernel_lib=builtin!")

        kernel_lib = spec.variants["kernel_lib"].value
        outlev = spec.variants["outlev"].value

        lapacke_libs = (
            spec["lapack:c"].libs + spec["blas:c"].libs + find_system_libraries(["libm"])
        ).joined(";")
        lapacke_include_dir = spec["lapack:c"].headers.directories[0]

        args = [
            "-DCMAKE_FIND_DEBUG_MODE=On",
            "-DPHIST_USE_CCACHE=OFF",
            "-DPHIST_KERNEL_LIB=%s" % kernel_lib,
            "-DPHIST_OUTLEV=%s" % outlev,
            "-DTPL_LAPACKE_LIBRARIES=%s" % lapacke_libs,
            "-DTPL_LAPACKE_INCLUDE_DIRS=%s" % lapacke_include_dir,
            self.define_from_variant("PHIST_ENABLE_MPI", "mpi"),
            self.define_from_variant("PHIST_ENABLE_OPENMP", "openmp"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("PHIST_ENABLE_SCAMAC", "scamac"),
            "-DPHIST_USE_TRILINOS_TPLS:BOOL=%s" % ("ON" if "^trilinos" in spec else "OFF"),
            "-DPHIST_USE_SOLVER_TPLS:BOOL=%s"
            % ("ON" if "^trilinos+belos+anasazi" in spec else "OFF"),
            "-DPHIST_USE_PRECON_TPLS:BOOL=%s" % ("ON" if "^trilinos" in spec else "OFF"),
            self.define_from_variant("XSDK_ENABLE_Fortran", "fortran"),
            "-DXSDK_INDEX_SIZE=%s" % ("64" if "+int64" in spec else "32"),
            self.define_from_variant("PHIST_HOST_OPTIMIZE", "host"),
        ]
        # Force phist to use the MPI wrappers instead of raw compilers
        # (see issue #26002 and the comment in the trilinos package.py)
        if "+mpi" in spec:
            args.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    define("MPI_HOME", spec["mpi"].prefix),
                ]
            )

        # Workaround for non-compliant and possibly broken code needed for gcc@10:
        # MPI_Allreduce(localRes, res, 1, MPI_LOGICAL, MPI_LAND, map1%comm, ierr);
        # MPI_Allreduce(my_ierr,global_ierr,1,MPI_INTEGER,MPI_MAX,map1%comm,mpi_ierr)
        # Error: Type mismatch between actual argument at (1)
        # and actual argument at (2) (LOGICAL(4)/INTEGER(4)).

        if spec.satisfies("%gcc@10:"):
            args.append(define("CMAKE_Fortran_FLAGS", "-fallow-argument-mismatch"))

        return args

    def check(self):
        with working_dir(self.build_directory):
            # This affects all versions of phist with ^mpich with all gcc versions:
            if "^mpich" in self.spec:
                hint = "Expect tests to timeout with mpich. Should work with: ^openmpi."
                tty.warn("========================== %s =======================" % hint)
                try:
                    make("check")
                except spack.util.executable.ProcessError:
                    raise InstallError("run-test of phist ^mpich: Hint: " + hint)
            else:
                make("check")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        """run 'make test_install'"""
        # The build script of test_install expects the sources to be copied here:
        install_tree(
            join_path(self.stage.source_path, "exampleProjects"),
            join_path(self.stage.path, "exampleProjects"),
        )
        with working_dir(self.build_directory):
            make("test_install")

    @property
    def parallel(self):
        return self.spec.satisfies("@1.8:")
