# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Benchmark(CMakePackage):
    """A microbenchmark support library"""

    homepage = "https://github.com/google/benchmark"
    url = "https://github.com/google/benchmark/archive/v1.6.0.tar.gz"
    git = "https://github.com/google/benchmark.git"

    license("Apache-2.0")

    # first properly installed CMake config packages in
    # 1.2.0 release: https://github.com/google/benchmark/issues/363
    version("main", branch="main")
    version("1.8.5", sha256="d26789a2b46d8808a48a4556ee58ccc7c497fcd4c0af9b90197674a81e04798a")
    version("1.8.4", sha256="3e7059b6b11fb1bbe28e33e02519398ca94c1818874ebed18e504dc6f709be45")
    version("1.8.3", sha256="6bc180a57d23d4d9515519f92b0c83d61b05b5bab188961f36ac7b06b0d9e9ce")
    version("1.8.2", sha256="2aab2980d0376137f969d92848fbb68216abb07633034534fc8c65cc4e7a0e93")
    version("1.8.1", sha256="e9ff65cecfed4f60c893a1e8a1ba94221fad3b27075f2f80f47eb424b0f8c9bd")
    version("1.8.0", sha256="ea2e94c24ddf6594d15c711c06ccd4486434d9cf3eca954e2af8a20c88f9f172")
    version("1.7.1", sha256="6430e4092653380d9dc4ccb45a1e2dc9259d581f4866dc0759713126056bc1d7")
    version("1.7.0", sha256="3aff99169fa8bdee356eaa1f691e835a6e57b1efeadb8a0f9f228531158246ac")
    version("1.6.2", sha256="a9f77e6188c1cd4ebedfa7538bf5176d6acc72ead6f456919e5f464ef2f06158")
    version("1.6.1", sha256="6132883bc8c9b0df5375b16ab520fac1a85dc9e4cf5be59480448ece74b278d4")
    version("1.6.0", sha256="1f71c72ce08d2c1310011ea6436b31e39ccab8c2db94186d26657d41747c85d6")
    version("1.5.6", sha256="789f85b4810d13ff803834ea75999e41b326405d83d6a538baf01499eda96102")
    version("1.5.5", sha256="3bff5f237c317ddfd8d5a9b96b3eede7c0802e799db520d38ce756a2a46a18a0")
    version("1.5.4", sha256="e3adf8c98bb38a198822725c0fc6c0ae4711f16fbbf6aeb311d5ad11e5a081b5")
    version("1.5.0", sha256="3c6a165b6ecc948967a1ead710d4a181d7b0fbcaa183ef7ea84604994966221a")
    version("1.4.1", sha256="f8e525db3c42efc9c7f3bc5176a8fa893a9a9920bbd08cef30fb56a51854d60d")
    version("1.4.0", sha256="616f252f37d61b15037e3c2ef956905baf9c9eecfeab400cb3ad25bae714e214")
    version("1.3.0", sha256="f19559475a592cbd5ac48b61f6b9cedf87f0b6775d1443de54cfe8f53940b28d")
    version("1.2.0", sha256="3dcc90c158838e2ac4a7ad06af9e28eb5877cf28252a81e55eb3c836757d3070")
    version("1.1.0", sha256="e7334dd254434c6668e33a54c8f839194c7c61840d52f4b6258eee28e9f3b20e")
    version("1.0.0", sha256="d2206c263fc1a7803d4b10e164e0c225f6bcf0d5e5f20b87929f137dee247b54")

    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel", "Coverage"),
    )
    variant(
        "performance_counters",
        default=True,
        when="@1.5.4:",
        description="Enable performance counters provided by libpfm",
    )

    depends_on("cmake@2.8.11:", type="build", when="@:1.1.0")
    depends_on("cmake@2.8.12:", type="build", when="@1.2.0:1.4")
    depends_on("cmake@3.5.1:", type="build", when="@1.5.0:")
    depends_on("libpfm4", type=("build", "link"), when="+performance_counters")

    def cmake_args(self):
        # No need for testing for the install
        args = [
            self.define("BENCHMARK_ENABLE_TESTING", False),
            self.define_from_variant("BENCHMARK_ENABLE_LIBPFM", "performance_counters"),
        ]
        return args

    def patch(self):
        filter_file(
            r"add_cxx_compiler_flag..fstrict.aliasing.",
            r"##### add_cxx_compiler_flag(-fstrict-aliasing)",
            "CMakeLists.txt",
        )
        filter_file(
            r"add_cxx_compiler_flag..Werror",
            r"##### add_cxx_compiler_flag(-Werror",
            "CMakeLists.txt",
        )
