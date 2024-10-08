# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Warpx(CMakePackage, PythonExtension):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.

    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid GPU/OpenMP/MPI parallelization and load balancing capabilities.
    """

    homepage = "https://ecp-warpx.github.io"
    url = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/24.10.tar.gz"
    git = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers("ax3l", "dpgrote", "EZoni", "RemiLehe")
    tags = ["e4s", "ecp"]

    license("BSD-3-Clause-LBNL")

    version("develop", branch="development")
    version("24.10", sha256="1fe3a86bf820a2ecef853cdcd9427fba4e0cb1efb05326da7dc9dbf94551202f")
    # 22.01+ requires C++17 or newer
    # 20.01+ requires C++14 or newer

    variant("app", default=True, description="Build the WarpX executable application")
    variant("ascent", default=False, description="Enable Ascent in situ visualization")
    variant(
        "catalyst",
        default=False,
        description="Enable Catalyst2 in situ visualization",
        when="@24.09:",
    )
    variant("sensei", default=False, description="Enable SENSEI in situ visualization")
    variant(
        "compute",
        default="omp",
        values=("omp", "cuda", "hip", "sycl", "noacc"),
        multi=False,
        description="On-node, accelerated computing backend",
    )
    variant(
        "dims",
        default="1,2,rz,3",
        values=("1", "2", "3", "rz"),
        multi=True,
        description="Number of spatial dimensions",
    )
    variant("eb", default=True, description="Embedded boundary support")
    # Spack defaults to False but pybind11 defaults to True (and IPO is highly
    # encouraged to be used)
    variant(
        "python_ipo",
        default=True,
        description="CMake interprocedural optimization for Python bindings (recommended)",
    )
    variant("lib", default=True, description="Build WarpX as a shared library")
    variant("mpi", default=True, description="Enable MPI support")
    variant(
        "mpithreadmultiple",
        default=True,
        description="MPI thread-multiple support, i.e. for async_io",
    )
    variant("openpmd", default=True, description="Enable openPMD I/O")
    variant(
        "precision",
        default="double",
        values=("single", "double"),
        multi=False,
        description="Floating point precision (single/double)",
    )
    variant("fft", default=True, description="Enable support for FFT-based solvers")
    variant("python", default=False, description="Enable Python bindings")
    variant("qed", default=True, description="Enable QED support")
    variant("qedtablegen", default=False, description="QED table generation support")
    variant("shared", default=True, description="Build a shared version of the library")
    variant("tprof", default=True, description="Enable tiny profiling features")

    depends_on("cxx", type="build")

    for v in ["24.10", "develop"]:
        depends_on(
            f"amrex@{v} build_system=cmake +linear_solvers +pic +particles +shared +tiny_profile",
            when=f"@{v}",
            type=("build", "link"),
        )
        depends_on("py-amrex@{0}".format(v), when="@{0} +python".format(v), type=("build", "run"))

    depends_on("boost@1.66.0: +math", when="+qedtablegen")
    depends_on("cmake@3.24.0:", type="build")
    with when("+ascent"):
        depends_on("ascent", when="+ascent")
        depends_on("ascent +cuda", when="+ascent compute=cuda")
        depends_on("ascent +mpi", when="+ascent +mpi")
        depends_on("amrex +ascent +conduit")
    with when("+catalyst"):
        depends_on("libcatalyst@2.0: +conduit")
        depends_on("libcatalyst +mpi", when="+mpi")
        depends_on("amrex +catalyst +conduit")
    with when("dims=1"):
        depends_on("amrex dimensions=1")
    with when("dims=2"):
        depends_on("amrex dimensions=2")
    with when("dims=rz"):
        depends_on("amrex dimensions=2")
    with when("dims=3"):
        depends_on("amrex dimensions=3")
    with when("+eb"):
        depends_on("amrex +eb")
    depends_on("mpi", when="+mpi")
    with when("+mpi"):
        depends_on("amrex +mpi")
        depends_on("py-amrex +mpi", when="+python")
    with when("~mpi"):
        depends_on("amrex ~mpi")
        depends_on("py-amrex ~mpi", when="~python")
    with when("precision=single"):
        depends_on("amrex precision=single")
    with when("precision=double"):
        depends_on("amrex precision=double")
    depends_on("py-pybind11@2.12.0:", when="+python", type=("build", "link"))
    depends_on("sensei@4.0.0:", when="+sensei")
    with when("compute=cuda"):
        depends_on("amrex +cuda")
        depends_on("cuda@11.0:")
    with when("compute=hip"):
        depends_on("amrex +rocm")
        depends_on("rocfft", when="+fft")
        depends_on("rocprim")
        depends_on("rocrand")
    with when("compute=noacc"):
        depends_on("amrex ~cuda ~openmp ~rocm ~sycl")
        with when("+fft"):
            depends_on("fftw@3: ~mpi", when="~mpi")
            depends_on("fftw@3: +mpi", when="+mpi")
            depends_on("pkgconfig", type="build")
    with when("compute=omp"):
        depends_on("amrex +openmp")
        depends_on("llvm-openmp", when="%apple-clang")
        with when("+fft"):
            depends_on("fftw@3: +openmp")
            depends_on("fftw ~mpi", when="~mpi")
            depends_on("fftw +mpi", when="+mpi")
            depends_on("pkgconfig", type="build")
    with when("+fft dims=rz"):
        depends_on("lapackpp")
        depends_on("blaspp")
        depends_on("blaspp +cuda", when="compute=cuda")
    with when("+openpmd"):
        depends_on("openpmd-api@0.15.1:")
        depends_on("openpmd-api ~mpi", when="~mpi")
        depends_on("openpmd-api +mpi", when="+mpi")

    # Python bindings
    # note: in Spack, we only need the cmake package, not py-cmake
    with when("+python"):
        extends("python")
        depends_on("python@3.8:", type=("build", "run"))
        depends_on("py-numpy@1.15.0:", type=("build", "run"))
        depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
        depends_on("py-periodictable@1.5:1", type=("build", "run"))
        depends_on("py-picmistandard@0.30.0", type=("build", "run"), when="@24.09:")
        depends_on("py-pip@23:", type="build")
        depends_on("py-setuptools@42:", type="build")
        depends_on("py-pybind11@2.12.0:", type=("build", "link"))
        depends_on("py-wheel@0.40:", type="build")

    conflicts("~qed +qedtablegen", msg="WarpX PICSAR QED table generation needs +qed")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DCMAKE_INSTALL_LIBDIR=lib",
            # variants
            self.define_from_variant("WarpX_APP", "app"),
            self.define_from_variant("WarpX_ASCENT", "ascent"),
            self.define_from_variant("WarpX_CATALYST", "catalyst"),
            self.define_from_variant("WarpX_SENSEI", "sensei"),
            "-DWarpX_COMPUTE={0}".format(spec.variants["compute"].value.upper()),
            "-DWarpX_DIMS={0}".format(";".join(spec.variants["dims"].value).upper()),
            self.define_from_variant("WarpX_EB", "eb"),
            self.define_from_variant("WarpX_LIB", "lib"),
            self.define_from_variant("WarpX_MPI", "mpi"),
            self.define_from_variant("WarpX_MPI_THREAD_MULTIPLE", "mpithreadmultiple"),
            self.define_from_variant("WarpX_OPENPMD", "openpmd"),
            "-DWarpX_PRECISION={0}".format(spec.variants["precision"].value.upper()),
            self.define_from_variant("WarpX_PYTHON", "python"),
            self.define_from_variant("WarpX_QED", "qed"),
            self.define_from_variant("WarpX_QED_TABLE_GEN", "qedtablegen"),
        ]

        args.append("-DWarpX_amrex_internal=OFF")
        args.append(self.define_from_variant("WarpX_FFT", "fft"))

        # FindMPI needs an extra hint sometimes, particularly on cray systems
        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))

        if "+openpmd" in spec:
            args.append("-DWarpX_openpmd_internal=OFF")

        if "+python" in spec:
            pip_args = PythonPipBuilder.std_args(self)
            pip_args_install_index = pip_args.index("install")
            pip_args_before_install = pip_args[:pip_args_install_index]
            pip_args_after_install = pip_args[pip_args_install_index + 1 :] + [
                f"--prefix={self.prefix}"
            ]

            args.append("-DWarpX_pyamrex_internal=OFF")
            args.append("-DWarpX_pybind11_internal=OFF")
            args.append(self.define_from_variant("WarpX_PYTHON_IPO", "python_ipo"))
            # Additional parameters to pass to `pip`
            args.append('-DPY_PIP_OPTIONS="' + " ".join(pip_args_before_install) + '"'),
            # Additional parameters to pass to `pip install`
            args.append('-DPY_PIP_INSTALL_OPTIONS="' + " ".join(pip_args_after_install) + '"'),

        # Work-around for SENSEI 4.0: wrong install location for CMake config
        #   https://github.com/SENSEI-insitu/SENSEI/issues/79
        if "+sensei" in spec:
            args.append(self.define("SENSEI_DIR", spec["sensei"].prefix.lib.cmake))

        # WarpX uses CCache by default, interfering with Spack wrappers
        args.append(self.define("WarpX_CCACHE", False))

        return args

    phases = ("cmake", "build", "install")
    build_targets = ["all"]
    with when("+python"):
        build_targets += ["pip_wheel", "pip_install_nodeps"]

    @property
    def libs(self):
        libsuffix = {"1": "1d", "2": "2d", "3": "3d", "rz": "rz"}
        libs = []
        for dim in self.spec.variants["dims"].value:
            libs += find_libraries(
                ["libwarpx." + libsuffix[dim]], root=self.prefix, recursive=True, shared=True
            )
            libs += find_libraries(
                ["libablastr"],
                root=self.prefix,
                recursive=True,
                shared=self.spec.variants["shared"],
            )
        return libs

    # WarpX has many examples to serve as a suitable smoke check. One
    # that is typical was chosen here
    examples_src_dir = "Examples/Physics_applications/laser_acceleration/"

    def _get_input_options(self, dim, post_install):
        spec = self.spec
        examples_dir = join_path(
            install_test_root(self) if post_install else self.stage.source_path,
            self.examples_src_dir,
        )
        inputs_nD = {
            "1": "inputs_base_1d",
            "2": "inputs_base_2d",
            "3": "inputs_base_3d",
            "rz": "inputs_base_rz",
        }
        if spec.satisfies("@:24.10"):
            inputs_nD["1"] = "inputs_test_1d_laser_acceleration"
        inputs = join_path(examples_dir, inputs_nD[dim])

        cli_args = [inputs, "max_step=50", "diag1.intervals=10"]
        # test openPMD output if compiled in
        if "+openpmd" in spec:
            cli_args.append("diag1.format=openpmd")
            # RZ: thetaMode output uses different variables
            if dim == "rz":
                cli_args.append("diag1.fields_to_plot=Er Et Ez Br Bt Bz jr jt jz rho")
        return cli_args

    def check(self):
        """Checks after the build phase"""
        spec = self.spec
        if "+app" not in spec:
            print("WarpX check skipped: requires variant +app")
            return

        with working_dir("spack-check", create=True):
            for dim in spec.variants["dims"].value:
                cli_args = self._get_input_options(dim, False)
                exe_nD = {"1": "warpx.1d", "2": "warpx.2d", "3": "warpx.3d", "rz": "warpx.rz"}
                warpx = Executable(join_path(self.build_directory, "bin/" + exe_nD[dim]))
                warpx(*cli_args)

    @run_after("install")
    def copy_test_sources(self):
        """Copy the example input files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.examples_src_dir])

    # TODO: remove installed static ablastr lib
    #       (if build as static lib - Spack default is shared)
    #    @run_after("install")
    #    def remove_unwanted_library(self):
    #        ... libablastr_{1d,2d,3d,rz}.a ...

    def run_warpx(self, dim):
        """Perform smoke tests on the installed package."""
        if "+app" not in self.spec:
            raise SkipTest("Package must be installed with +app")
        if dim not in self.spec.variants["dims"].value:
            raise SkipTest(f"Package must be installed with {dim} in dims")
        dim_arg = f"{dim}d" if dim.isdigit() else dim
        exe = find(self.prefix.bin, f"warpx.{dim_arg}.*", recursive=False)[0]
        cli_args = self._get_input_options(dim, True)
        warpx = which(exe)
        warpx(*cli_args)

    def test_warpx_1d(self):
        """Run warpx 1d test"""
        self.run_warpx("1")

    def test_warpx_2d(self):
        """Run warpx 2d test"""
        self.run_warpx("2")

    def test_warpx_3d(self):
        """Run warpx 3d test"""
        self.run_warpx("3")

    def test_warpx_rz(self):
        """Run warpx rz test"""
        self.run_warpx("rz")
