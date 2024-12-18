# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Prmon(CMakePackage):
    """Standalone monitor for process resource consumption."""

    homepage = "https://github.com/HSF/prmon/"
    url = "https://github.com/HSF/prmon/archive/refs/tags/v3.0.1.zip"
    git = "https://github.com/HSF/prmon.git"

    maintainers("graeme-a-stewart", "amete", "vvolkl")

    license("Apache-2.0")

    version("main", branch="main")
    version("3.1.0", sha256="02f25f1ea82300c93e5af14137e366b31c8d615283768d5f3f98616a0d6e507c")
    version("3.0.2", sha256="ea9ff521689fecb8c395e35e9540be18c7ab37812354c4a5c0ba505e2ab467c1")
    version("3.0.0", sha256="fd6f4e3a95e055d265fbbaba08d680826cb4770eb8830cc987898d6504ac7474")
    version("2.2.1", sha256="7c95538a0ddcfc71b5c581979a5bb298873fdf16966fd6951aaa2b2639b08319")
    version("2.2.0", sha256="7b3b887c679279f0e666e8c8c58ca1a22a328b8b94ecff09e61795a6a83e8ce5")
    version("2.1.1", sha256="302d7a3fc5a403143d794e16dca1949e3d13e46cf9857dfaad4e374f4a468df2")
    version("1.1.1", sha256="a6e6486bbc4d6cddf73affe07d9ff7948a424c9a02b3cdd5bbe5c6cafa06af2e")

    variant("plot", default=False, description="Make use of plotting scripts")

    depends_on("nlohmann-json")
    depends_on("cmake@3.3:", type="build")
    depends_on("spdlog", when="@3.0.0:")
    depends_on("py-matplotlib", type="run", when="+plot")
    depends_on("py-numpy", type="run", when="+plot")
    depends_on("py-pandas", type="run", when="+plot")

    def cmake_args(self):
        args = [
            # googletest is fetched and built on the fly
            self.define("BUILD_GTESTS", self.run_tests),
            self.define("USE_EXTERNAL_NLOHMANN_JSON", True),
            self.define("USE_EXTERNAL_SPDLOG", True),
        ]
        return args

    def check(self):
        # some tests expect to run on an otherwise idle machine
        # so we need to make sure that they are not running in parallel
        with working_dir(self.build_directory):
            ctest(parallel=False)
