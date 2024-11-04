# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Googletest(CMakePackage):
    """Google test framework for C++.  Also called gtest."""

    homepage = "https://github.com/google/googletest"
    url = "https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz"
    git = "https://github.com/google/googletest"

    maintainers("sethrj")

    version("main", branch="main")
    version("1.14.0", sha256="8ad598c73ad796e0d8280b082cebd82a630d73e73cd3c70057938a6501bba5d7")
    version("1.13.0", sha256="ad7fdba11ea011c1d925b3289cf4af2c66a352e18d4c7264392fead75e919363")
    version("1.12.1", sha256="81964fe578e9bd7c94dfdb09c8e4d6e6759e19967e397dbea48d1c10e45d0df2")
    version("1.12.0", sha256="2a4f11dce6188b256f3650061525d0fe352069e5c162452818efbbf8d0b5fe1c")
    version("1.11.0", sha256="b4870bf121ff7795ba20d20bcdd8627b8e088f2d1dab299a031c1034eddc93d5")
    version("1.10.0", sha256="9dc9157a9a1551ec7a7e43daea9a694a0bb5fb8bec81235d8a1e6ef64c716dcb")
    version("1.8.1", sha256="9bf1fe5182a604b4135edc1a425ae356c9ad15e9b23f9f12a02e80184c3a249c")
    version("1.8.0", sha256="58a6f4277ca2bc8565222b3bbd58a177609e9c488e8a72649359ba51450db7d8")
    version("1.7.0", sha256="f73a6546fdf9fce9ff93a5015e0333a8af3062a152a9ad6bcb772c96687016cc")
    version("1.6.0", sha256="5fbc058e5b662b9c86d93ac76fefb58eec89cbf26144b49669a38ecb62758447")

    depends_on("cxx", type="build")  # generated

    variant("gmock", default=True, when="@1.8:", description="Build with gmock")
    variant("pthreads", default=True, description="Build multithreaded version with pthreads")
    variant("shared", default=True, description="Build shared libraries (DLLs)")

    variant(
        "cxxstd",
        default="11",
        values=("98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building",
    )
    conflicts("cxxstd=98", when="@1.9:")
    conflicts("cxxstd=11", when="@1.13:")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        args.append(self.define("gtest_disable_pthreads", not spec.satisfies("+pthreads")))
        if spec.satisfies("@1.8:"):
            # New style (contains both Google Mock and Google Test)
            args.append(self.define("BUILD_GTEST", True))
            args.append(self.define_from_variant("BUILD_GMOCK", "gmock"))

        return args

    @when("@:1.7.0")
    def install(self, spec, prefix):
        """Make the install targets"""
        with working_dir(self.build_directory):
            # Google Test doesn't have a make install
            # We have to do our own install here.
            install_tree(join_path(self.stage.source_path, "include"), prefix.include)

            mkdirp(prefix.lib)
            if spec.satisfies("+shared"):
                install("libgtest.{0}".format(dso_suffix), prefix.lib)
                install("libgtest_main.{0}".format(dso_suffix), prefix.lib)
            else:
                install("libgtest.a", prefix.lib)
                install("libgtest_main.a", prefix.lib)

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)

    def url_for_version(self, version):
        """googletest has changed how they publish releases on github. Up until,
        including version 1.12.1 they were tagged as `release-<version>`.
        Afterwards things switched to the format `v<version>`. Additionally,
        newer versions are available from `archive/refs/tags/<tagname>.tar.gz`,
        while versions up to, and including, 1.8.0 are available only from
        `archive/release-<version>.tar.gz`
        """
        if version <= Version("1.8.0"):
            return f"{self.git}/archive/release-{version}.tar.gz"

        tagname = f"release-{version}"
        if version >= Version("1.13"):
            tagname = f"v{version}"

        return f"{self.git}/archive/refs/tags/{tagname}.tar.gz"
