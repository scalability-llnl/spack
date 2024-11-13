# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack.package import *


class RangeV3(CMakePackage):
    """Range v3 forms the basis of a proposal to add range support to the
    standard library (N4128: Ranges for the Standard Library). It also will
    be the reference implementation for an upcoming Technical
    Specification. These are the first steps toward turning ranges into an
    international standard."""

    homepage = "https://github.com/ericniebler/range-v3"
    url = "https://github.com/ericniebler/range-v3/archive/0.3.6.tar.gz"
    git = "https://github.com/ericniebler/range-v3.git"
    maintainers("greenc-FNAL")

    license("BSL-1.0")

    version("master", branch="master")
    version("0.12.0", sha256="015adb2300a98edfceaf0725beec3337f542af4915cec4d0b89fa0886f4ba9cb")
    version("0.11.0", sha256="376376615dbba43d3bef75aa590931431ecb49eb36d07bb726a19f680c75e20c")
    version("0.10.0", sha256="5a1cd44e7315d0e8dcb1eee4df6802221456a9d1dbeac53da02ac7bd4ea150cd")
    version("0.5.0", sha256="32e30b3be042246030f31d40394115b751431d9d2b4e0f6d58834b2fd5594280")
    version("0.4.0", sha256="5dbc878b7dfc500fb04b6b9f99d63993a2731ea34b0a4b8d5f670a5a71a18e39")
    version("0.3.7", sha256="e6b0fb33bfd07ec32d54bcddd3e8d62e995a3cf0b64b34788ec264da62581207")
    version("0.3.6", sha256="ce6e80c6b018ca0e03df8c54a34e1fd04282ac1b068cd39e902e2e5201ac117f")
    version("0.3.5", sha256="0a0094b450fe17e1454468bef5b6bf60e73ef100aebe1663daf6fbdf2c353836")
    version("0.3.0", sha256="cc29fbed5b06b11e7f9a732f7e1211483ebbd3cfe29d86e40c93209014790d74")
    version("0.2.6", sha256="b1b448ead59bd726248bcb607b4a47335a00bed1c74630e09d550da3ff72d02c")
    version("0.2.5", sha256="4125089da83dec3f0ed676066f0cf583fe55dd9270bc62f1736907f57656ca7e")
    version("0.2.4", sha256="6fc4f9e80ee8eb22302db45c5648c665817aeeeee7f99b7effdf6a38a1be9a75")
    version("0.2.3", sha256="214a3f0ea70d479ca58f0af8938de49a9ed476564213431ab3b8e02a849b8098")
    version("0.2.2", sha256="01a7bee222570a55a79c84a54b2997ed718dac06f43a82122ff0150a11477f9d")
    version("0.2.1", sha256="25d5e3dad8052d668873e960bd78f068bebfba3bd28a278f805ea386f9438790")
    version("0.2.0", sha256="49b1a62a7a36dab582521c8034d8e736a8922af664d007c1529d3162b1294331")

    depends_on("cxx", type="build")  # generated

    # Note that as of 0.3.6 range is a header-only library so it is not
    # necessary to match standards with packages using this
    # one. Eventually range-v3 will be obsoleted by the C++ standard.
    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("doc", default=False, description="Build and install documentation.")

    variant("examples", default=False, description="Build and install examples.")

    variant("perf", default=False, description="Build performance benchmarks")

    # Known compiler conflicts. Your favorite compiler may also conflict
    # depending on its C++ standard support.
    conflicts("%clang@:3.6.1")
    conflicts("%clang@:3.9", when="@0.11.0:")
    conflicts("%gcc@:4.9.0")
    conflicts("%gcc@:5.2.0", when="cxxstd=14")
    conflicts("%gcc@:5", when="cxxstd=17")

    depends_on("cmake@3.6:", type="build")
    depends_on("doxygen+graphviz", type="build", when="+doc")
    depends_on(
        "boost+date_time+program_options@1.59.0: cxxstd=14",
        type="build",
        when="+examples cxxstd=14",
    )
    depends_on(
        "boost+date_time+program_options@1.59.0: cxxstd=17",
        type="build",
        when="+examples cxxstd=17",
    )

    # Fix reported upstream issue
    # https://github.com/ericniebler/range-v3/issues/1196 per PR
    # https://github.com/ericniebler/range-v3/pull/1202.
    patch("fix-is_trivial.patch", level=1, when="@0.5.0")

    # Some -Wno-... options unknown to GCC were being checked as OK to
    # use but causing problems during the build. Patch from
    # https://github.com/ericniebler/range-v3/commit/0c20dbf05973368339aeae0c4e106560e2dcf76b#diff-acb9169b4ccbac494ced5140d285a015
    patch("gcc-compile-opt-check.patch", level=1, when="@0.5.0%gcc")

    def _remove_cmake_subdir(self, subdir):
        filter_file(
            r"^(\s*add_subdirectory\s*\(\s*{0}\s*\))".format(subdir), r"#\1", "CMakeLists.txt"
        )

    # Deal with variant choices for versions that don't have applicable
    # CMake switches.
    def patch(self):
        spec = self.spec
        if spec.satisfies("@:0.3.0"):
            if not self.run_tests:
                self._remove_cmake_subdir("test")
            if "+examples" not in spec:
                self._remove_cmake_subdir("example")
            if "+perf" not in spec:
                self._remove_cmake_subdir("perf")
        if spec.satisfies("@:0.3.6~doc"):
            self._remove_cmake_subdir("doc")

    def cmake_args(self):
        spec = self.spec
        cxxstd = self.spec.variants["cxxstd"].value

        on_or_off = lambda opt: "ON" if "+" + opt in spec else "OFF"

        args = ["-DRANGES_CXX_STD={0}".format(cxxstd)]

        if spec.satisfies("@0.3.7:"):
            args.append("-DRANGE_V3_DOCS=" + on_or_off("doc"))

        if spec.satisfies("@0.3.6:"):
            args.append("-DRANGE_V3_TESTS=" + ("ON" if self.run_tests else "OFF"))
            args.append("-DRANGE_V3_EXAMPLES=" + on_or_off("examples"))
            args.append("-DRANGE_V3_PERF=" + on_or_off("perf"))
        elif spec.satisfies("@0.3.1:"):
            args.append("-DRANGE_V3_NO_TESTING=" + ("OFF" if self.run_tests else "ON"))
            args.append("-DRANGE_V3_NO_EXAMPLE=" + ("OFF" if "+examples" in spec else "ON"))
            args.append("-DRANGE_V3_NO_PERF=" + ("OFF" if "+perf" in spec else "ON"))
        else:
            # Older versions don't have the right switches. See patch() above.
            pass

        if not self.run_tests:
            args.append("-DRANGE_V3_NO_HEADER_CHECK=ON")

        if "+examples" in spec:
            args.append(
                "-DRANGES_BUILD_CALENDAR_EXAMPLE=" + ("ON" if cxxstd in ["14", "17"] else "OFF")
            )

        return args

    @property
    def build_targets(self):
        spec = self.spec
        targets = []
        if "+doc" in spec:
            targets.extend(["all", "doc"])
        return targets

    def _copy_and_clean_dirs(self, subdir):
        install_tree(subdir, os.path.join(self.prefix, subdir))
        with working_dir(self.build_directory):
            install_tree(subdir, os.path.join(self.prefix, subdir))
        with working_dir(os.path.join(self.prefix, subdir)):
            shutil.rmtree("CMakeFiles")
            for f in ("cmake_install.cmake", "CTestTestfile.cmake", "Makefile", "CMakeLists.txt"):
                if os.path.exists(f):
                    os.remove(f)

    @run_after("install")
    def install_extra(self):
        spec = self.spec

        # Install docs.
        if "+doc" in spec:
            with working_dir(self.build_directory):
                install_tree(os.path.join("doc", "html"), os.path.join(self.prefix, "doc", "html"))

        # Install examples.
        if "+examples" in spec:
            self._copy_and_clean_dirs("example")

        # Install performance benchmarks.
        if "+perf" in spec:
            self._copy_and_clean_dirs("perf")
