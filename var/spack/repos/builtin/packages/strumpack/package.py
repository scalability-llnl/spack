# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *
from spack.util.environment import set_env
from spack.util.executable import ProcessError


class Strumpack(CMakePackage, CudaPackage, ROCmPackage):
    """STRUMPACK -- STRUctured Matrix PACKage - provides linear solvers
    for sparse matrices and for dense rank-structured matrices, i.e.,
    matrices that exhibit some kind of low-rank property. It provides a
    distributed memory fully algebraic sparse solver and
    preconditioner. The preconditioner is mostly aimed at large sparse
    linear systems which result from the discretization of a partial
    differential equation, but is not limited to any particular type of
    problem. STRUMPACK also provides preconditioned GMRES and BiCGStab
    iterative solvers."""

    homepage = "http://portal.nersc.gov/project/sparse/strumpack"
    url = "https://github.com/pghysels/STRUMPACK/archive/refs/tags/v7.1.3.tar.gz"
    git = "https://github.com/pghysels/STRUMPACK.git"

    tags = ["e4s"]

    maintainers("pghysels")

    test_requires_compiler = True

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")
    version("7.2.0", sha256="6988c00c3213f13e53d75fb474102358f4fecf07a4b4304b7123d86fdc784639")
    version("7.1.3", sha256="c951f38ee7af20da3ff46429e38fcebd57fb6f12619b2c56040d6da5096abcb0")
    version("7.1.2", sha256="262a0193fa1682d0eaa90363f739e0be7a778d5deeb80e4d4ae12446082a39cc")
    version("7.1.1", sha256="56481a22955c2eeb40932777233fc227347743c75683d996cb598617dd2a8635")
    version("7.1.0", sha256="a3e80e0530ea1cc6b62c22699cfe5f02f81794321f225440f0e08bceed69c241")
    version("7.0.1", sha256="ddbf9c0509eaf0f8a4c70f59508787336a05eeacc8322f156117d8ce59a70a60")
    version("7.0.0", sha256="18f7a0d75cc5cfdb7bbb6112a2bdda7a50fbcaefa2d8bab001f902bdf62e69e3")
    version("6.3.1", sha256="3f1de435aeb850c06d841655c3bc426565eb0cc0a7314b76586c2c709b03fb61")
    version("6.3.0", sha256="47dec831684894b7ed77c66b8a23e172b388c83580cfaf91f921564fa0b46d41")
    version("6.2.1", sha256="52d63ab8f565266a9b1b5f3596afd00fc3b70296179b53a1e5b99405defeca22")
    version("6.2.0", sha256="d8443fc66b399b8f2615ad9dd0e599c2e2b6836620cca5d9c4d7a9cde9c5a860")
    version("6.1.0", sha256="219ec7360594172464aafa6ecac1fd161097db6fb9ee35af5c1ca61531f4f5c4")
    version("6.0.0", sha256="fcea150b68172d5a4ec2c02f9cce0b7305919b86871c9cf34a9f65b1567d58b7")
    version("5.1.1", sha256="6cf4eaae5beb9bd377f2abce9e4da9fd3e95bf086ae2f04554fad6dd561c28b9")
    version("5.0.0", sha256="bdfd1620ff7158d96055059be04ee49466ebaca8213a2fdab33e2d4571019a49")
    version("4.0.0", sha256="a3629f1f139865c74916f8f69318f53af6319e7f8ec54e85c16466fd7d256938")
    version("3.3.0", sha256="499fd3b58656b4b6495496920e5372895861ebf15328be8a7a9354e06c734bc7")
    version("3.2.0", sha256="34d93e1b2a3b8908ef89804b7e08c5a884cbbc0b2c9f139061627c0d2de282c1")
    version("3.1.1", sha256="c1c3446ee023f7b24baa97b24907735e89ce4ae9f5ef516645dfe390165d1778")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("mpi", default=True, description="Use MPI")
    variant(
        "openmp", default=True, description="Enable thread parallellism via tasking with OpenMP"
    )
    variant("parmetis", default=True, description="Enable use of ParMetis")
    variant("scotch", default=False, description="Enable use of Scotch")
    variant("butterflypack", default=True, description="Enable use of ButterflyPACK")
    variant("zfp", default=True, description="Build with support for compression using ZFP")
    variant("c_interface", default=True, description="Enable C interface")
    variant("count_flops", default=False, description="Build with flop counters")
    variant("task_timers", default=False, description="Build with timers for internal routines")
    variant("slate", default=True, description="Build with SLATE support")
    variant("magma", default=False, description="Build with MAGMA support")

    depends_on("cmake@3.11:", when="@:6.2.9", type="build")
    depends_on("cmake@3.17:", when="@6.3.0:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("openblas threads=openmp", when="^[virtuals=blas] openblas")
    depends_on("scalapack", when="+mpi")
    depends_on("metis")
    depends_on("parmetis", when="+parmetis")
    depends_on("scotch~metis", when="+scotch")
    depends_on("scotch~metis+mpi", when="+scotch+mpi")
    depends_on("butterflypack@1.1.0", when="@3.3.0:3.9 +butterflypack+mpi")
    depends_on("butterflypack@1.2.0:", when="@4.0.0: +butterflypack+mpi")
    depends_on("butterflypack@2.1.0:", when="@6.3.0: +butterflypack+mpi")
    depends_on("cuda", when="@4.0.0: +cuda")
    depends_on("zfp@0.5.5", when="@:7.0.1 +zfp")
    depends_on("zfp", when="@7.0.2: +zfp")
    depends_on("hipblas", when="+rocm")
    depends_on("hipsparse", type="link", when="@7.0.1: +rocm")
    depends_on("rocsolver", when="+rocm")
    depends_on("rocthrust", when="+rocm")
    depends_on("slate", when="+slate")
    depends_on("magma+cuda", when="+magma+cuda")
    depends_on("magma+rocm", when="+magma+rocm")
    depends_on("slate+cuda", when="+cuda+slate")
    depends_on("slate+rocm", when="+rocm+slate")
    for val in ROCmPackage.amdgpu_targets:
        depends_on(
            "slate amdgpu_target={0}".format(val), when="+slate amdgpu_target={0}".format(val)
        )

    conflicts("+parmetis", when="~mpi")
    conflicts("+butterflypack", when="~mpi")
    conflicts("+butterflypack", when="@:3.2.0")
    conflicts("+zfp", when="@:3.9")
    conflicts("+cuda", when="@:3.9")
    conflicts("+rocm", when="@:5.0")
    conflicts("+rocm", when="+cuda")
    conflicts("+slate", when="@:5.1.1")
    conflicts("+slate", when="~mpi")
    conflicts("+magma", when="~rocm~cuda")

    patch("intel-19-compile.patch", when="@3.1.1")
    patch("shared-rocm.patch", when="@5.1.1")

    # https://github.com/pghysels/STRUMPACK/commit/e4b110b2d823c51a90575b77ec1531c699097a9f
    patch("strumpack-7.0.1-mpich-hipcc.patch", when="@7.0.1 +rocm ^mpich")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("STRUMPACK_USE_MPI", "mpi"),
            self.define_from_variant("STRUMPACK_USE_OPENMP", "openmp"),
            self.define_from_variant("STRUMPACK_USE_CUDA", "cuda"),
            self.define_from_variant("STRUMPACK_USE_HIP", "rocm"),
            self.define_from_variant("TPL_ENABLE_PARMETIS", "parmetis"),
            self.define_from_variant("TPL_ENABLE_SCOTCH", "scotch"),
            self.define_from_variant("TPL_ENABLE_BPACK", "butterflypack"),
            self.define_from_variant("TPL_ENABLE_MAGMA", "magma"),
            self.define_from_variant("STRUMPACK_COUNT_FLOPS", "count_flops"),
            self.define_from_variant("STRUMPACK_TASK_TIMERS", "task_timers"),
            "-DTPL_BLAS_LIBRARIES=%s" % spec["blas"].libs.joined(";"),
            "-DTPL_LAPACK_LIBRARIES=%s" % spec["lapack"].libs.joined(";"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        if "+mpi" in spec:
            args.append("-DTPL_SCALAPACK_LIBRARIES=%s" % spec["scalapack"].libs.joined(";"))

        if spec.satisfies("@:3.9"):
            if "+mpi" in spec:
                args.extend(
                    [
                        "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                        "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
                        "-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc,
                    ]
                )
            args.extend([self.define_from_variant("STRUMPACK_C_INTERFACE", "c_interface")])

        # Workaround for linking issue on Mac:
        if spec.satisfies("%apple-clang +mpi"):
            args.append("-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc)

        if "+cuda" in spec:
            args.extend(
                [
                    "-DCUDA_TOOLKIT_ROOT_DIR={0}".format(spec["cuda"].prefix),
                    "-DCMAKE_CUDA_HOST_COMPILER={0}".format(env["SPACK_CXX"]),
                ]
            )
            cuda_archs = spec.variants["cuda_arch"].value
            if "none" not in cuda_archs:
                args.append("-DCUDA_NVCC_FLAGS={0}".format(" ".join(self.cuda_flags(cuda_archs))))

        if "+rocm" in spec:
            args.append("-DCMAKE_CXX_COMPILER={0}".format(spec["hip"].hipcc))
            args.append("-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix))
            rocm_archs = spec.variants["amdgpu_target"].value
            hipcc_flags = []
            if spec.satisfies("@7.0.1: +rocm"):
                hipcc_flags.append("-std=c++14")
            if "none" not in rocm_archs:
                hipcc_flags.append("--amdgpu-target={0}".format(",".join(rocm_archs)))
            args.append("-DHIP_HIPCC_FLAGS={0}".format(" ".join(hipcc_flags)))

        if "%cce" in spec:
            # Assume the proper Cray CCE module (cce) is loaded:
            craylibs_var = "CRAYLIBS_" + str(spec.target.family).upper()
            craylibs_path = env.get(craylibs_var, None)
            if not craylibs_path:
                raise InstallError(
                    f"The environment variable {craylibs_var} is not defined.\n"
                    "\tMake sure the 'cce' module is in the compiler spec."
                )
            env.setdefault("LDFLAGS", "")
            env["LDFLAGS"] += " -Wl,-rpath," + craylibs_path

        return args

    test_src_dir = "test"

    @property
    def test_data_dir(self):
        """Return the stand-alone test data directory."""
        add_sparse = not self.spec.satisfies("@:5.1.1")
        return join_path("examples", "sparse" if add_sparse else "", "data")

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.test_data_dir, self.test_src_dir])

    def _test_example(self, test_prog, test_cmd, pre_args=[]):
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        cmake_filename = join_path(test_dir, "CMakeLists.txt")
        with open(cmake_filename, "w") as mkfile:
            mkfile.write("cmake_minimum_required(VERSION 3.15)\n")
            mkfile.write("project(StrumpackSmokeTest LANGUAGES CXX)\n")
            mkfile.write("find_package(STRUMPACK REQUIRED)\n")
            mkfile.write("add_executable({0} {0}.cpp)\n".format(test_prog))
            mkfile.write(
                "target_link_libraries({0} ".format(test_prog) + "PRIVATE STRUMPACK::strumpack)\n"
            )

        with working_dir(test_dir):
            opts = self.builder.std_cmake_args + self.cmake_args() + ["."]
            cmake = self.spec["cmake"].command
            cmake(*opts)

            make = which("make")
            make(test_prog)

            with set_env(OMP_NUM_THREADS="1"):
                exe = which(test_cmd)
                test_args = pre_args + [join_path("..", self.test_data_dir, "pde900.mtx")]
                exe(*test_args)

    def test_sparse_seq(self):
        """Run sequential test_sparse"""
        test_exe = "test_sparse_seq"
        self._test_example(test_exe, test_exe)

    def test_sparse_mpi(self):
        """Run parallel test_sparse"""
        if "+mpi" not in self.spec:
            raise SkipTest("Package must be installed with '+mpi'")
        test_exe_mpi = "test_sparse_mpi"
        mpi_args = ["-n", "1", test_exe_mpi]

        mpi_bin = self.spec["mpi"].prefix.bin
        mpiexe_list = ["srun", mpi_bin.mpirun, mpi_bin.mpiexec]
        for exe in mpiexe_list:
            tty.info(f"Attempting to build and launch with {os.path.basename(exe)}")
            try:
                args = ["--immediate=30"] + mpi_args if exe == "srun" else mpi_args
                self._test_example(test_exe_mpi, exe, args)
                return
            except (Exception, ProcessError) as err:
                tty.info(f"Skipping {exe}: {str(err)}")

        assert False, "No MPI executable was found"

    def check(self):
        """Skip the builtin testsuite, use the stand-alone tests instead."""
        pass
