# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack.package import *
from spack.util.executable import which_string


class Ninja(Package):
    """Ninja is a small build system with a focus on speed. It differs from
    other build systems in two major respects: it is designed to have its input
    files generated by a higher-level build system, and it is designed to run
    builds as fast as possible."""

    homepage = "https://ninja-build.org/"
    url = "https://github.com/ninja-build/ninja/archive/v1.7.2.tar.gz"
    git = "https://github.com/ninja-build/ninja.git"

    tags = ["build-tools", "e4s", "windows"]

    executables = ["^ninja$"]

    license("Apache-2.0")

    version("kitware", branch="features-for-fortran", git="https://github.com/Kitware/ninja.git")
    version("master", branch="master")
    version("1.12.0", sha256="8b2c86cd483dc7fcb7975c5ec7329135d210099a89bc7db0590a07b0bbfe49a5")
    version("1.11.1", sha256="31747ae633213f1eda3842686f83c2aa1412e0f5691d1c14dbbcc67fe7400cea")
    version("1.11.0", sha256="3c6ba2e66400fe3f1ae83deb4b235faf3137ec20bd5b08c29bfc368db143e4c6")
    version("1.10.2", sha256="ce35865411f0490368a8fc383f29071de6690cbadc27704734978221f25e2bed")
    version("1.10.1", sha256="a6b6f7ac360d4aabd54e299cc1d8fa7b234cd81b9401693da21221c62569a23e")
    version("1.10.0", sha256="3810318b08489435f8efc19c05525e80a993af5a55baa0dfeae0465a9d45f99f")
    version("1.9.0", sha256="5d7ec75828f8d3fd1a0c2f31b5b0cea780cdfe1031359228c428c1a48bfcd5b9")
    version("1.8.2", sha256="86b8700c3d0880c2b44c2ff67ce42774aaf8c28cbf57725cb881569288c1c6f4")
    version("1.7.2", sha256="2edda0a5421ace3cf428309211270772dd35a91af60c96f93f90df6bc41b16d9")
    version("1.6.0", sha256="b43e88fb068fe4d92a3dfd9eb4d19755dae5c33415db2e9b7b61b4659009cde7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "re2c", default=not sys.platform == "win32", description="Enable buidling Ninja with re2c"
    )

    depends_on("python", type="build")
    depends_on("re2c@0.11.3:", type="build", when="+re2c")

    phases = ["configure", "install"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        return output.strip()

    def configure(self, spec, prefix):
        python("configure.py", "--bootstrap")

    @run_after("configure")
    @on_package_attributes(run_tests=True)
    def configure_test(self):
        ninja = Executable("./ninja")
        ninja(f"-j{make_jobs}", "ninja_test")
        ninja_test = Executable("./ninja_test")
        ninja_test()

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.misc)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        name = "ninja"
        if sys.platform == "win32":
            name = name + ".exe"
        install(name, prefix.bin)
        install_tree("misc", prefix.misc)

        if sys.platform == "win32":
            return
        # Some distros like Fedora install a 'ninja-build' executable
        # instead of 'ninja'. Install both for uniformity.
        with working_dir(prefix.bin):
            symlink("ninja", "ninja-build")

    def setup_dependent_package(self, module, dspec):
        name = "ninja"

        module.ninja = MakeExecutable(
            which_string(name, path=[self.spec.prefix.bin], required=True),
            determine_number_of_jobs(parallel=dspec.package.parallel),
            supports_jobserver=self.spec.version == ver("kitware"),
        )
