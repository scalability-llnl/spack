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

    # NOTE: if you update the versions here, also see py-warpx
    version("develop", branch="development")
    version("24.10", sha256="1fe3a86bf820a2ecef853cdcd9427fba4e0cb1efb05326da7dc9dbf94551202f")
    version(
        "24.08",
        sha256="8da1f2967f613a65a295260260aa4f081ac1d1b7c1d6987d294e02b86099df08",
        deprecated=True,
    )
    version(
        "23.08",
        sha256="67695ff04b83d1823ea621c19488e54ebaf268532b0e5eb4ea8ad293d7ab3ddc",
        deprecated=True,
    )
    version(
        "23.07",
        sha256="511633f94c0d0205013609bde5bbf92a29c2e69f6e69b461b80d09dc25602945",
        deprecated=True,
    )
    version(
        "23.06",
        sha256="75fcac949220c44dce04de581860c9a2caa31a0eee8aa7d49455fa5fc928514b",
        deprecated=True,
    )
    version(
        "23.05",
        sha256="34306a98fdb1f5f44ab4fb92f35966bfccdcf1680a722aa773af2b59a3060d73",
        deprecated=True,
    )
    version(
        "23.04",
        sha256="e5b285c73e13a0d922eba5d83760c168d4fd388e54a519830003b2e692dab823",
        deprecated=True,
    )
    version(
        "23.03",
        sha256="e1274aaa2a2c83d599d61c6e4c426db4ed5d4c5dc61a2002715783a6c4843718",
        deprecated=True,
    )
    version(
        "23.02",
        sha256="a6c63ebc38cbd224422259a814be501ac79a3b734dab7f59500b6957cddaaac1",
        deprecated=True,
    )
    version(
        "23.01",
        sha256="e853d01c20ea00c8ddedfa82a31a11d9d91a7f418d37d7f064cf8a241ea4da0c",
        deprecated=True,
    )
    version(
        "22.12",
        sha256="96019902cd6ea444a1ae515e8853048e9074822c168021e4ec1687adc72ef062",
        deprecated=True,
    )
    version(
        "22.11",
        sha256="528f65958f2f9e60a094e54eede698e871ccefc89fa103fe2a6f22e4a059515e",
        deprecated=True,
    )
    version(
        "22.10",
        sha256="3cbbbbb4d79f806b15e81c3d0e4a4401d1d03d925154682a3060efebd3b6ca3e",
        deprecated=True,
    )
    version(
        "22.09",
        sha256="dbef1318248c86c860cc47f7e18bbb0397818e3acdfb459e48075004bdaedea3",
        deprecated=True,
    )
    version(
        "22.08",
        sha256="5ff7fd628e8bf615c1107e6c51bc55926f3ef2a076985444b889d292fecf56d4",
        deprecated=True,
    )
    version(
        "22.07",
        sha256="0286adc788136cb78033cb1678d38d36e42265bcfd3d0c361a9bcc2cfcdf241b",
        deprecated=True,
    )
    version(
        "22.06",
        sha256="e78398e215d3fc6bc5984f5d1c2ddeac290dcbc8a8e9d196e828ef6299187db9",
        deprecated=True,
    )
    version(
        "22.05",
        sha256="2fa69e6a4db36459b67bf663e8fbf56191f6c8c25dc76301dbd02a36f9b50479",
        deprecated=True,
    )
    version(
        "22.04",
        sha256="9234d12e28b323cb250d3d2cefee0b36246bd8a1d1eb48e386f41977251c028f",
        deprecated=True,
    )
    version(
        "22.03",
        sha256="ddbef760c8000f2f827dfb097ca3359e7aecbea8766bec5c3a91ee28d3641564",
        deprecated=True,
    )
    version(
        "22.02",
        sha256="d74b593d6f396e037970c5fbe10c2e5d71d557a99c97d40e4255226bc6c26e42",
        deprecated=True,
    )
    version(
        "22.01",
        sha256="e465ffadabb7dc360c63c4d3862dc08082b5b0e77923d3fb05570408748b0d28",
        deprecated=True,
    )
    # 22.01+ requires C++17 or newer
    version(
        "21.12",
        sha256="847c98aac20c73d94c823378803c82be9a14139f1c14ea483757229b452ce4c1",
        deprecated=True,
    )
    version(
        "21.11",
        sha256="ce60377771c732033a77351cd3500b24b5d14b54a5adc7a622767b9251c10d0b",
        deprecated=True,
    )
    version(
        "21.10",
        sha256="d372c573f0360094d5982d64eceeb0149d6620eb75e8fdbfdc6777f3328fb454",
        deprecated=True,
    )
    version(
        "21.09",
        sha256="861a65f11846541c803564db133c8678b9e8779e69902ef1637b21399d257eab",
        deprecated=True,
    )
    version(
        "21.08",
        sha256="6128a32cfd075bc63d08eebea6d4f62d33ce0570f4fd72330a71023ceacccc86",
        deprecated=True,
    )
    version(
        "21.07",
        sha256="a8740316d813c365715f7471201499905798b50bd94950d33f1bd91478d49561",
        deprecated=True,
    )
    version(
        "21.06",
        sha256="a26039dc4061da45e779dd5002467c67a533fc08d30841e01e7abb3a890fbe30",
        deprecated=True,
    )
    version(
        "21.05",
        sha256="f835f0ae6c5702550d23191aa0bb0722f981abb1460410e3d8952bc3d945a9fc",
        deprecated=True,
    )
    version(
        "21.04",
        sha256="51d2d8b4542eada96216e8b128c0545c4b7527addc2038efebe586c32c4020a0",
        deprecated=True,
    )
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
        default="3",
        values=("1", "2", "3", "rz"),
        multi=False,
        description="Number of spatial dimensions",
        when="@:23.05",
    )
    variant(
        "dims",
        default="1,2,rz,3",
        values=("1", "2", "3", "rz"),
        multi=True,
        description="Number of spatial dimensions",
        when="@23.06:",
    )
    variant("eb", default=True, description="Embedded boundary support", when="@24.10:")
    variant("eb", default=False, description="Embedded boundary support", when="@:24.09")
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

    for v in ["24.10", "24.08", "develop"]:
        depends_on(
            f"amrex@{v} build_system=cmake +linear_solvers +pic +particles +shared +tiny_profile",
            when=f"@{v}",
            type=("build", "link"),
        )
        depends_on("py-amrex@{0}".format(v), when="@{0} +python".format(v), type=("build", "run"))

    depends_on("boost@1.66.0: +math", when="+qedtablegen")
    depends_on("cmake@3.15.0:", type="build")
    depends_on("cmake@3.18.0:", type="build", when="@22.01:")
    depends_on("cmake@3.20.0:", type="build", when="@22.08:")
    depends_on("cmake@3.24.0:", type="build", when="@24.09:")
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
    depends_on("py-pybind11@2.12.0:", when="@24.04: +python", type=("build", "link"))
    depends_on("sensei@4.0.0:", when="@22.07: +sensei")
    with when("compute=cuda"):
        depends_on("amrex +cuda")
        depends_on("cuda@9.2.88:")
        depends_on("cuda@11.0:", when="@22.01:")
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
        depends_on("openpmd-api@0.13.1:")
        depends_on("openpmd-api@0.14.2:", when="@21.09:")
        depends_on("openpmd-api@0.15.1:", when="@23.05:")
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
        depends_on("py-picmistandard@0.28.0", type=("build", "run"), when="@23.11:24.07")
        depends_on("py-picmistandard@0.29.0", type=("build", "run"), when="@24.08")
        depends_on("py-picmistandard@0.30.0", type=("build", "run"), when="@24.09:")
        depends_on("py-pip@23:", type="build")
        depends_on("py-setuptools@42:", type="build")
        depends_on("py-pybind11@2.12.0:", type=("build", "link"))
        depends_on("py-wheel@0.40:", type="build")

    conflicts("+python", when="@:24.04", msg="Python bindings only supported in 24.04+")
    conflicts("dims=1", when="@:21.12", msg="WarpX 1D support starts in 22.01+")
    conflicts("~qed +qedtablegen", msg="WarpX PICSAR QED table generation needs +qed")
    conflicts(
        "compute=sycl",
        when="+fft",
        msg="WarpX spectral solvers are not yet tested with SYCL " '(use "warpx ~fft")',
    )
    conflicts("+sensei", when="@:22.06", msg="WarpX supports SENSEI 4.0+ with 22.07 and newer")

    # The symbolic aliases for our +lib target were missing in the install
    # location
    # https://github.com/ECP-WarpX/WarpX/pull/2626
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/2626.patch?full_index=1",
        sha256="a431d4664049d6dcb6454166d6a948d8069322a111816ca5ce01553800607544",
        when="@21.12",
    )

    # Workaround for AMReX<=22.06 no-MPI Gather
    # https://github.com/ECP-WarpX/WarpX/pull/3134
    # https://github.com/AMReX-Codes/amrex/pull/2793
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/3134.patch?full_index=1",
        sha256="b786ce64a3c2c2b96ff2e635f0ee48532e4ae7ad9637dbf03f11c0768c290690",
        when="@22.02:22.05",
    )

    # Forgot to install ABLASTR library
    # https://github.com/ECP-WarpX/WarpX/pull/3141
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/3141.patch?full_index=1",
        sha256="dab6fb44556ee1fd466a4cb0e20f89bde1ce445c9a51a2c0f59d1740863b5e7d",
        when="@22.04,22.05",
    )

    # Fix failing 1D CUDA build
    # https://github.com/ECP-WarpX/WarpX/pull/3162
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/3162.patch?full_index=1",
        sha256="0ae573d1390ed8063f84e3402d30d34e522e65dc5dfeea3d07e165127ab373e9",
        when="@22.06",
    )

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

        if spec.satisfies("@24.08:"):
            args.append("-DWarpX_amrex_internal=OFF")
            args.append(self.define_from_variant("WarpX_FFT", "fft"))
        else:
            args.append(self.define_from_variant("WarpX_PSATD", "fft"))

        # FindMPI needs an extra hint sometimes, particularly on cray systems
        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))

        if "+openpmd" in spec:
            args.append("-DWarpX_openpmd_internal=OFF")

        if "+python" in spec:
            if spec.satisfies("@24.08:"):
                args.append("-DWarpX_pyamrex_internal=OFF")
                args.append("-DWarpX_pybind11_internal=OFF")
                args.append(self.define_from_variant("WarpX_PYTHON_IPO", "python_ipo"))

        # Work-around for SENSEI 4.0: wrong install location for CMake config
        #   https://github.com/SENSEI-insitu/SENSEI/issues/79
        if "+sensei" in spec:
            args.append(self.define("SENSEI_DIR", spec["sensei"].prefix.lib.cmake))

        # WarpX uses CCache by default, interfering with Spack wrappers
        ccache_var = "CCACHE_PROGRAM" if spec.satisfies("@:24.01") else "WarpX_CCACHE"
        args.append(self.define(ccache_var, False))

        return args

    phases = ("cmake", "build", "install", "pip_install_nodeps")
    build_targets = ["all"]
    with when("+python"):
        build_targets += ["pip_wheel"]

    def pip_install_nodeps(self, spec, prefix):
        """Install everything from build directory."""
        pip = spec["python"].command
        pip.add_default_arg("-m", "pip")

        args = PythonPipBuilder.std_args(self) + [
            f"--prefix={prefix}",
            "--find-links=warpx-whl",
            "pywarpx",
        ]

        with working_dir(self.build_directory):
            pip(*args)

        # todo: from PythonPipBuilder
        # ....execute_install_time_tests()

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
        if spec.satisfies("@:24.09"):
            inputs_nD = {"1": "inputs_1d", "2": "inputs_2d", "3": "inputs_3d", "rz": "inputs_rz"}
            if spec.satisfies("@:21.12"):
                inputs_nD["rz"] = "inputs_2d_rz"
        else:
            inputs_nD = {
                "1": "inputs_test_1d_laser_acceleration",
                "2": "inputs_base_2d",
                "3": "inputs_base_3d",
                "rz": "inputs_base_rz",
            }
        inputs = join_path(examples_dir, inputs_nD[dim])

        cli_args = [inputs, "max_step=50", "diag1.intervals=10"]
        # test openPMD output if compiled in
        if "+openpmd" in spec:
            cli_args.append("diag1.format=openpmd")
            # RZ: New openPMD thetaMode output
            if dim == "rz" and spec.satisfies("@22.04:"):
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
        if self.spec.satisfies("@:23.05") and not dim.isdigit():
            dim_arg = dim_arg.upper()
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
