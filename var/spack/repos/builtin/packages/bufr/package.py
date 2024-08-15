# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Bufr(CMakePackage):
    """The NOAA bufr library contains subroutines, functions and other
    utilities that can be used to read (decode) and write (encode)
    data in BUFR, which is a WMO standard format for the exchange of
    meteorological data. This is part of the NCEPLIBS project.
    The library also includes a Python interface.
    """

    homepage = "https://noaa-emc.github.io/NCEPLIBS-bufr"
    url = "https://github.com/NOAA-EMC/NCEPLIBS-bufr/archive/refs/tags/v12.1.0.tar.gz"
    git = "https://github.com/NOAA-EMC/NCEPLIBS-bufr"

    maintainers("AlexanderRichert-NOAA", "edwardhartnett", "Hang-Lei-NOAA", "jbathegit")

    version("develop", branch="develop")
    version("12.1.0", sha256="b5eae61b50d4132b2933b6e6dfc607e5392727cdc4f46ec7a94a19109d91dcf3")
    version("12.0.1", sha256="525f26238dba6511a453fc71cecc05f59e4800a603de2abbbbfb8cbb5adf5708")
    version("12.0.0", sha256="d01c02ea8e100e51fd150ff1c4a1192ca54538474acb1b7f7a36e8aeab76ee75")
    version("11.7.1", sha256="6533ce6eaa6b02c0cb5424cfbc086ab120ccebac3894980a4daafd4dfadd71f8")
    version("11.7.0", sha256="6a76ae8e7682bbc790321bf80c2f9417775c5b01a5c4f10763df92e01b20b9ca")
    version("11.6.0", sha256="af4c04e0b394aa9b5f411ec5c8055888619c724768b3094727e8bb7d3ea34a54")
    version("11.5.0", sha256="d154839e29ef1fe82e58cf20232e9f8a4f0610f0e8b6a394b7ca052e58f97f43")
    version("11.4.0", sha256="946482405e675b99e8e0c221d137768f246076f5e9ba92eed6cae47fb68b7a26")

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    # Patch to not add "-c" to ranlib flags when using llvm-ranlib on Apple systems
    patch("cmakelists-apple-llvm-ranlib.patch", when="@11.5.0:11.6.0")
    # C test does not explicity link to -lm causing DSO error when building shared libs
    patch("c-tests-libm.patch", when="@11.5.0:11.7.0")
    # Patch to identify Python version correctly
    patch("python-version.patch", when="@11.5:12.0.0 +python")

    variant("python", default=False, description="Enable Python interface")
    variant("shared", default=True, description="Build shared libraries", when="@11.5:")
    variant("test_files", default="none", description="Path to test files")
    variant("utils", default=True, description="Build utilities", when="@12.1:")

    extends("python", when="+python")

    depends_on("python@3:", type=("build", "run"), when="+python")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-pip", type="build", when="+python")
    depends_on("py-wheel", type="build", when="+python")

    conflicts("%oneapi@:2024.1", msg="Requires oneapi 2024.2 or later")

    def url_for_version(self, version):
        pre = "bufr_" if version < Version("12.0.1") else ""
        return (
            f"https://github.com/NOAA-EMC/NCEPLIBS-bufr/archive/refs/tags/{pre}v{version}.tar.gz"
        )

    # Need to make the lines shorter at least on some systems
    def patch(self):
        with when("@:11.7.1"):
            filter_file("_lenslmax 120", "_lenslmax 60", "CMakeLists.txt")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_PYTHON", "python"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("BUILD_TESTS", self.run_tests),
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("BUILD_UTILS", "utils"),
        ]

        if not self.spec.satisfies("test_files=none"):
            args.append(self.define_from_variant("TEST_FILE_DIR", "test_files"))

        return args

    def flag_handler(self, name, flags):
        """
        On macOS if a library built with the ar utility contains objects
        with Fortran module data but no executable functions,
        the symbols corresponding to the module data may not be resolved
        when an object referencing them is linked against the library.
        You can work around this by compiling with option -fno-common.
        """
        fc = self.compiler.fc
        if self.spec.satisfies("platform=darwin"):
            if name == "fflags":
                if "ifort" in fc or "gfortran" in fc:
                    flags.append("-fno-common")

        # Bufr inserts a path into source code which may be longer than 132
        if name == "fflags" and "gfortran" in fc:
            flags.append("-ffree-line-length-none")

        # Inject flags into CMake build
        return (None, None, flags)

    def _setup_bufr_environment(self, env, suffix):
        libname = "libbufr_{0}".format(suffix)
        shared = True if "+shared" in self.spec else False
        # Bufr has _DA (dynamic allocation) libs in versions <= 11.5.0
        append = "" if self.spec.satisfies("@11.5.0:") else "_DA"
        lib = find_libraries(libname + append, root=self.prefix, shared=shared, recursive=True)
        lib_envname = "BUFR_LIB{0}".format(suffix) + append
        inc_envname = "BUFR_INC{0}".format(suffix) + append
        include_dir = "{0}_{1}".format(self.prefix.include.bufr, suffix)

        env.set(lib_envname, lib[0])
        env.set(inc_envname, include_dir)

        if self.spec.satisfies("+python"):
            pyver = self.spec["python"].version.up_to(2)
            pydir = join_path(os.path.dirname(lib[0]), f"python{pyver}", "site-packages")
            env.prepend_path("PYTHONPATH", pydir)

    def setup_run_environment(self, env):
        suffixes = ["4"]
        if not self.spec.satisfies("@12:"):
            suffixes += ["8", "d"]
        for suffix in suffixes:
            self._setup_bufr_environment(env, suffix)

    def check(self):
        with working_dir(self.builder.build_directory):
            make("test")
