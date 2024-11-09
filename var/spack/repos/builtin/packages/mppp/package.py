# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mppp(CMakePackage):
    """mp++ is a C++11/14/17/20 library for multiprecision arithmetic"""

    # URL for package's homepage.
    homepage = "https://bluescarni.github.io/mppp/index.html"
    url = "https://github.com/bluescarni/mppp/archive/refs/tags/v1.0.1.tar.gz"

    # List of GitHub accounts to notify when the package is updated.
    maintainers("bluescarni", "agseaton")

    # SPDX identifier of the project's license.
    license("MPL-2.0")

    version("1.0.1", sha256="90e8758bad2d9ebec04305d9cc394168de7bd563acc290e273dd68467e07de07")
    version("1.0.0", sha256="e58b1a5fb8bdf095261eeb0861c3f46f96c71c4b043d19700e73ce3e4e639268")
    version("0.27", sha256="a1e04f6605b3242d4361742159cf5ab273162fd7c105c2743a9bebcf44c846c3")
    version("0.26", sha256="4dbfa68802d9a1365eda884f085418afc147d01b7a928e8333e4dcc1c3b3ce9e")
    version("0.25", sha256="3e6142acd5c6d71405537311b0c800b6fa27a009a46af538ad07b7e6a115f95d")
    version("0.24", sha256="c84cbe38545b7f3f20688791e0a7ce4020830ed84ab6a109ab13a208745be9dc")
    version("0.23", sha256="76f4ee484afae4dbe00f4b0bf91063e4d5dc3eb2bbf5d34ecf174821965d5910")
    version("0.22", sha256="92e34a393c7b6e61daec6a26827a2b73b9b61d961ab37bcabbf051cc7ff19ad2")
    version("0.21", sha256="49a05fc6874a800cb42a3ac16eb46a50583f0b59d3b54008c58af766186a8c69")
    version("0.20", sha256="c736daeaac30e38e1c09a19d249209ad49f8ec92ab1315a8fb9a47cc1f54e607")

    depends_on("cxx", type="build")  # generated

    variant(
        "mpfr",
        default=True,
        description=(
            "Enable features relying on GNU MPFR library. Used in the"
            " implementation of the real class and for providing "
            "support for the long double type in integer and "
            "rational"
        ),
    )
    variant(
        "mpc",
        default=True,
        when="+mpfr",
        description=(
            "Enable features relying on the GNU MPC library. Used in "
            "the implementation of the complex class."
        ),
    )
    variant(
        "quadmath",
        default=False,
        description=(
            "Enable features relying on the GNU quadmath library. "
            "Used in the implementation of the real128 and complex128"
            " classes."
        ),
    )
    variant(
        "serialization",
        default=False,
        when="@0.22:",
        description="Enable support for serialization via the Boost.serialization library",
    )
    variant(
        "fmt",
        default=True,
        when="@0.27:",
        description="Enable support for formatting via the fmt library",
    )
    variant("tests", default=False, description="Build the test suite")
    variant(
        "benchmarks",
        default=False,
        when="+serialization +fmt",
        description="Build the benchmarking suite",
    )
    variant(
        "static",
        default=False,
        description="build mp++ as a static library, instead of a dynamic library",
    )

    # Dependencies
    depends_on("cmake@3.8:", type="build")

    # Required dependencies
    depends_on("gmp@5:")

    # Optional dependencies
    depends_on("mpfr@3:", when="+mpfr")
    depends_on("mpc", when="+mpc")
    depends_on("gcc", when="+quadmath")
    depends_on("boost@1.69: +serialization", when="+serialization")
    depends_on("fmt@6.2:", when="+fmt")

    def cmake_args(self):
        args = [
            self.define_from_variant("MPPP_WITH_MPFR", "mpfr"),
            self.define_from_variant("MPPP_WITH_MPC", "mpc"),
            self.define_from_variant("MPPP_WITH_QUADMATH", "quadmath"),
            self.define_from_variant("MPPP_WITH_BOOST_S11N", "serialization"),
            self.define_from_variant("MPPP_WITH_FMT", "fmt"),
            self.define_from_variant("MPPP_BUILD_TESTS", "tests"),
            self.define_from_variant("MPPP_BUILD_BENCHMARKS", "benchmarks"),
            self.define_from_variant("MPPP_BUILD_STATIC_LIBRARY", "static"),
            self.define_from_variant("MPPP_ENABLE_IPO", "ipo"),
        ]
        return args
