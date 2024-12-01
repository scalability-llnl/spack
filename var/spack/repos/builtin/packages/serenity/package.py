# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Serenity(CMakePackage):
    """Subsystem focused quantum chemistry code Serenity"""

    homepage = "https://www.uni-muenster.de/Chemie.oc/neugebauer/softwareAKN.html"
    url = "https://github.com/qcserenity/serenity/archive/refs/tags/1.4.0.tar.gz"
    git = "https://github.com/qcserenity/serenity.git"

    license("LGPL-3.0-only")

    version("master", branch="master")
    version("1.6.1", sha256="cc04b13c2e8a010d07389b2fed98981deacf085778d5375b3b6e89b967c3a5e6")
    version("1.4.0", sha256="c7a87fc8e6f8ca21685a27e08d09d49824d9a1e9947fc6abb40d20fbba0cc6e8")

    depends_on("cxx", type="build")  # generated

    variant("blas", default=True, description="Use BLAS library with Eigen")
    variant("lapack", default=True, description="Use Lapack library with Eigen")
    variant("python", default=False, description="Build Python bindings")
    variant("prefer_xcfun", default=True, description="Prefer XCFun instead of LibXC")
    variant(
        "laplace_minimax",
        default=False,
        description="Download and use Laplace-Minimax",
        when="@1.6.1:",
    )

    depends_on("blas", when="+blas")
    depends_on("cmake@3.12:", type="build")
    depends_on("boost+system+filesystem+program_options cxxstd=17 @1.65.0:")
    depends_on("eigen@3:")
    depends_on("googletest@1.8.1:", type="test", when="@1.4.0")
    depends_on("googletest@1.13.0:", type="test", when="@1.6.1:")
    depends_on("hdf5@1.10.1:+hl+cxx")
    depends_on("lapack", when="+lapack")
    depends_on("libecpint")
    depends_on("libxc@6.1.0", when="@1.6.1:")
    depends_on("libxc@5.0.0", when="@1.4.0")
    depends_on("pkgconfig", type="build")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-pybind11", when="+python", type="build")
    depends_on("serenity-libint")
    depends_on("xcfun")

    extends("python", when="+python")

    patch(
        "https://github.com/qcserenity/serenity/commit/af9f76d013e240d971337a467a03640cb9aabfb7.patch?full_index=1",
        sha256="45cce5e4d47b681891e78725b2cf5031d306337a5c7b8e62cd4891beb4a7b8b6",
        when="@1.6.1:",
    )

    def patch(self):
        filter_file(
            "include(CMakeParseArguments)",
            'message(FATAL_ERROR "Tried to download a dependency")',
            "cmake/DownloadProject.cmake",
            string=True,
        )

        if self.spec.satisfies(":@1.4"):
            filter_file(
                "find_package(GTest 1.8.1 QUIET)",
                "find_package(GTest REQUIRED)",
                "cmake/ImportGTest.cmake",
                string=True,
            )

            filter_file(
                "find_package(GMock 1.8.1 QUIET)",
                "return()",
                "cmake/ImportGTest.cmake",
                string=True,
            )

            filter_file(
                "function(import_libecpint)",
                "function(import_libecpint)\n"
                "find_package(ecpint CONFIG REQUIRED)\n"
                "add_library(ecpint INTERFACE IMPORTED)\n"
                "target_link_libraries(ecpint INTERFACE ECPINT::ecpint)\n",
                "cmake/ImportLibecpint.cmake",
                string=True,
            )

            filter_file(
                "function(import_libint)",
                "function(import_libint)\n"
                "find_package(Libint2 CONFIG REQUIRED)\n"
                "add_library(libint2-static INTERFACE IMPORTED)\n"
                "target_link_libraries(libint2-static INTERFACE Libint2::libint2)\n",
                "cmake/ImportLibint.cmake",
                string=True,
            )

            filter_file(
                "function(import_libxc)",
                "function(import_libxc)\n"
                "find_package(PkgConfig QUIET)\n"
                "pkg_check_modules(pc_libxc libxc)\n"
                "if(pc_libxc_FOUND)\n"
                "add_library(xc INTERFACE IMPORTED)\n"
                "target_link_libraries(xc INTERFACE ${pc_libxc_LINK_LIBRARIES})\n"
                "target_include_directories(xc INTERFACE ${pc_libxc_INCLUDE_DIRS})\n"
                'message("XC: included ${pc_libxc_LINK_LIBRARIES} ${pc_libxc_INCLUDE_DIRS}")\n'
                "endif()",
                "cmake/ImportLibxc.cmake",
                string=True,
            )

            filter_file(
                "function(import_pybind11)",
                "function(import_pybind11)\nfind_package(pybind11 REQUIRED)",
                "cmake/ImportPybind11.cmake",
                string=True,
            )

            filter_file(
                "function(import_xcfun)",
                "function(import_xcfun)\n"
                "find_package(XCFun CONFIG REQUIRED)\n"
                "add_library(xcfun INTERFACE IMPORTED)\n"
                "target_link_libraries(xcfun INTERFACE XCFun::xcfun)\n",
                "cmake/ImportXCFun.cmake",
                string=True,
            )
        else:
            filter_file(
                "find_package(GTest QUIET)",
                "find_package(GTest REQUIRED)",
                "cmake/ImportGTest.cmake",
                string=True,
            )

            filter_file(
                "find_package(GMock QUIET)", "return()", "cmake/ImportGTest.cmake", string=True
            )

    def cmake_args(self):
        args = [
            self.define("SERENITY_ENABLE_TESTS", self.run_tests),
            self.define_from_variant("SERENITY_PYTHON_BINDINGS", "python"),
            self.define("SERENITY_MARCH", ""),
            self.define_from_variant("SERENITY_PREFER_XCFUN", "prefer_xcfun"),
            self.define("SERENITY_USE_XCFUN", True),
            self.define("SERENITY_USE_LIBXC", True),
            self.define(
                "SERENITY_USE_INTEL_MKL", self.spec["lapack"].libs.names[0].startswith("mkl")
            ),
            self.define_from_variant("SERENITY_USE_LAPACK", "lapack"),
            self.define_from_variant("SERENITY_USE_BLAS", "blas"),
            self.define("SERENITY_USAGE_FROM_SOURCE", False),
            self.define("Libint2_DIR", self.spec["serenity-libint"].prefix.lib.cmake.libint2),
            self.define("XCFun_DIR", self.spec["xcfun"].prefix.share.XCFun),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("BOOST_ROOT", self.spec["boost"].prefix),
            self.define("BOOST_LIBRARY_DIR", self.spec["boost"].libs.directories[0]),
            self.define("BOOST_INCLUDE_DIR", self.spec["boost"].headers.directories[0]),
            self.define("BOOST_NO_SYSTEM_PATHS", True),
            self.define("Boost_NO_BOOST_CMAKE", True),
        ]
        if self.spec.satisfies("@1.6.1:"):
            args += [
                self.define("SERENITY_DOWNLOAD_DEPENDENCIES", False),
                self.define_from_variant("SERENITY_USE_LAPLACE_MINIMAX", "laplace_minimax"),
            ]
        if "+python" in self.spec:
            args.append(self.define("PYTHON_EXECUTABLE", self.spec["python"].command.path))
        return args

    def setup_run_environment(self, env):
        # set up environment like if we sourced dev/templates/serenity.sh
        env.set("SERENITY_HOME", self.prefix)
        env.set("SERENITY_BIN", self.prefix.bin)
        env.set("SERENITY_RESOURCES", join_path(self.prefix.share, "serenity/data/"))
        env.prepend_path("PYTHONPATH", self.prefix.lib)
