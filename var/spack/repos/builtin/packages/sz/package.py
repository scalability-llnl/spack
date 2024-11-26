# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *


class Sz(CMakePackage, AutotoolsPackage):
    """Error-bounded Lossy Compressor for HPC Data"""

    homepage = "https://szcompressor.org"
    url = "https://github.com/szcompressor/SZ/releases/download/v2.1.11/SZ-2.1.11.tar.gz"
    git = "https://github.com/szcompressor/sz"
    maintainers("disheng222", "robertu94")

    tags = ["e4s"]

    version("master", branch="master")
    version("2.1.12.5", sha256="32a820daf6019156a777300389d2392e4498a5c9daffce7be754cd0a5ba8729c")
    version("2.1.12.4", sha256="4ae242e8821a96b7a4571bb5df6a3c78742d375f80cccbd5d46c4bac255b3c08")
    version("2.1.12.2", sha256="427e263e1fed1b0a56e13e0aff8e6a19c6d78d5f35dd16856876c70ab6066dc6")
    version("2.1.12", sha256="3712b2cd7170d1511569e48a208f02dfb72ecd7ad053c321e2880b9083e150de")
    version("2.1.11.1", sha256="e6fa5c969b012782b1e5e9fbd1cd7d1c0ace908d9ec982e78b2910ec5c2161ac")
    version("2.1.11", sha256="85b8ef99344a3317ba9ee63ca4b9d99a51d1832d4d8880e01c7c56b3a69cacc9")
    version(
        "2.1.10",
        sha256="3aba7619bdb5412218f162696f946c9d3a3df5acf128ddc685b21e45c11f6ae3",
        url="https://github.com/szcompressor/SZ/releases/download/v2.1.10/sz-2.1.10.tar.gz",
    )
    version("2.1.9", sha256="491724ff1c0eaaab5e1a7a28e36aba6da9dcbeddb29d8d21a6d1388383d4891e")
    version("2.1.8.3", sha256="be94f3c8ab03d6849c59a98e0ebf80816a6b8d07a1d762a4b285498acb2f3871")
    version("2.1.8.1", sha256="a27c9c9da16c9c4232c54813ba79178945f47609043f11501d49a171e47d3f46")
    version("2.1.8.0", sha256="8d6bceb59a03d52e601e29d9b35c21b146c248abae352f9a4828e91d8d26aa24")
    version("2.0.2.0", sha256="176c65b421bdec8e91010ffbc9c7bf7852c799972101d6b66d2a30d9702e59b0")
    version("1.4.13.5", sha256="b5e37bf3c377833eed0a7ca0471333c96cd2a82863abfc73893561aaba5f18b9")
    version("1.4.13.4", sha256="c99b95793c48469cac60e6cf82f921babf732ca8c50545a719e794886289432b")
    version("1.4.13.3", sha256="9d80390f09816bf01b7a817e07339030d596026b00179275616af55ed3c1af98")
    version("1.4.13.2", sha256="bc45329bf54876ed0f721998940855dbd5fda54379ef35dad8463325488ea4c6")
    version("1.4.13.0", sha256="baaa7fa740a47e152c319b8d7b9a69fe96b4fea5360621cdc96cb250635f946f")
    version("1.4.12.3", sha256="c1413e1c260fac7a48cb11c6dd705730525f134b9f9b244af59885d564ac7a6f")
    version("1.4.12.1", sha256="98289d75481a6e407e4027b5e23013ae83b4aed88b3f150327ea711322cd54b6")
    version("1.4.11.1", sha256="6cbc5b233a3663a166055f1874f17c96ba29aa5a496d352707ab508288baa65c")
    version("1.4.11.0", sha256="52ff03c688522ebe085caa7a5f73ace28d8eaf0eb9a161a34a9d90cc5672ff8c")
    version("1.4.10.0", sha256="cf23cf1ffd7c69c3d3128ae9c356b6acdc03a38f92c02db5d9bfc04f3fabc506")
    version("1.4.9.2", sha256="9dc785274d068d04c2836955fc93518a9797bfd409b46fea5733294b7c7c18f8")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+fortran")

    build_system(
        conditional("autotools", when="@:2.1.8.0"),
        conditional("cmake", when="@2.1.8.1:"),
        default="cmake",
    )

    variant("openmp", default=False, description="build the multithreaded version using openmp")
    variant("examples", default=False, description="build examples")
    variant("python", default=False, description="builds the python wrapper")
    variant("netcdf", default=False, description="build the netcdf reader")
    variant("hdf5", default=False, description="build the hdf5 filter")
    variant("pastri", default=False, description="build the pastri mode")
    variant("time_compression", default=False, description="build the time based compression mode")
    variant("random_access", default=False, description="build the random access compression mode")
    variant("fortran", default=False, description="Enable fortran compilation")
    variant("shared", default=True, description="build shared versions of the libraries")
    variant("stats", default=False, description="build profiling statistics for compression")

    # Part of latest sources don't support -O3 optimization
    # with Fujitsu compiler.
    patch("fix_optimization.patch", when="@2.0.2.0:%fj")

    depends_on("zlib-api")
    depends_on("zstd")

    extends("python", when="+python")
    depends_on("python@3:", when="+python", type=("build", "link", "run"))
    depends_on("swig@3.12:", when="+python", type="build")
    depends_on("py-numpy", when="+python", type=("build", "link", "run"))
    depends_on("hdf5", when="+hdf5")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("cmake@3.13:", type="build")
    depends_on("cunit", type="test")

    conflicts("%clang@15:", when="@:2.1.12.4+hdf5")

    patch("ctags-only-if-requested.patch", when="@2.1.8.1:2.1.8.3")

    # Windows requires numerous commits that only exist on master at the moment
    conflicts("platform=windows", when="@:2.1.12.5")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi"):
                flags.append("-Wno-error=implicit-function-declaration")
        return (flags, None, None)

    def setup_run_environment(self, env):
        if "+hdf5" in self.spec:
            env.prepend_path("HDF5_PLUGIN_PATH", self.prefix.lib64)

    def test_2d_float(self):
        """Run simple 2D compression/decompression"""
        test_data_dir = self.test_suite.current_test_data_dir

        exe = which(self.prefix.bin.sz)
        if exe is None:
            raise SkipTest(f"sz is not installed for version {self.version}")

        with working_dir(test_data_dir):
            filename = "testfloat_8_8_128.dat"
            orifile = test_data_dir.join(filename)
            with test_part(
                self, "test_2d_float_compression", purpose="testing 2D compression of sz"
            ):
                options = ["-z", "-f", "-i", orifile, "-M", "REL", "-R", "1E-3", "-2", "8", "1024"]
                exe(*options)

            filename = "testfloat_8_8_128.dat.sz"
            decfile = test_data_dir.join(filename)

            with test_part(
                self, "test_2d_float_decompression", purpose="testing 2D decompression of sz"
            ):
                options = ["-x", "-f", "-i", orifile, "-s", decfile, "-2", "8", "1024", "-a"]
                exe(*options)

    def test_3d_float(self):
        """Run simple 3D compression/decompression"""
        test_data_dir = self.test_suite.current_test_data_dir

        exe = which(self.prefix.bin.sz)
        if exe is None:
            raise SkipTest(f"sz is not installed for version {self.version}")

        with working_dir(test_data_dir):
            filename = "testfloat_8_8_128.dat"
            orifile = test_data_dir.join(filename)
            with test_part(
                self, "test_3d_float_compression", purpose="testing 3D compression of sz"
            ):
                options = [
                    "-z",
                    "-f",
                    "-i",
                    orifile,
                    "-M",
                    "REL",
                    "-R",
                    "1E-3",
                    "-3",
                    "8",
                    "8",
                    "128",
                ]
                exe(*options)

            filename = "testfloat_8_8_128.dat.sz"
            decfile = test_data_dir.join(filename)
            with test_part(
                self, "test_3d_float_decompression", purpose="testing 3D decompression of sz"
            ):
                options = ["-x", "-f", "-i", orifile, "-s", decfile, "-3", "8", "8", "128", "-a"]
                exe(*options)


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    build_directory = "."

    def configure_args(self):
        return self.enable_or_disable("fortran")

    @run_before("build")
    def make_clean(self):
        # at least the v2.0.2.0 tarball contains object files
        # which need to be cleaned out
        make("clean")


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        result = [
            self.define_from_variant("BUILD_NETCDF_READER", "netcdf"),
            self.define_from_variant("BUILD_HDF5_FILTER", "hdf5"),
            self.define_from_variant("BUILD_PASTRI", "pastri"),
            self.define_from_variant("BUILD_TIMECPR", "time_compression"),
            self.define_from_variant("BUILD_RANDOMACCESS", "random_access"),
            self.define_from_variant("BUILD_FORTRAN", "fortran"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_STATS", "stats"),
            self.define("BUILD_TESTS", self.pkg.run_tests),
            self.define_from_variant("BUILD_PYTHON_WRAPPER", "python"),
            self.define_from_variant("BUILD_OPENMP", "openmp"),
            self.define_from_variant("BUILD_SZ_EXAMPLES", "examples"),
        ]

        if "+python" in self.spec:
            result.append(self.define("SZ_PYTHON_SITELIB", python_platlib))

        return result
