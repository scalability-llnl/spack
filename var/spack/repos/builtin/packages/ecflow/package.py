# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Ecflow(CMakePackage):
    """ecFlow is a work flow package that enables users to run a large number
    of programs (with dependencies on each other and on time) in a controlled
    environment.

    It provides tolerance for hardware and software failures, combined with
    good restart capabilities.
    """

    homepage = "https://confluence.ecmwf.int/display/ECFLOW/"
    url = "https://confluence.ecmwf.int/download/attachments/8650755/ecFlow-4.11.1-Source.tar.gz"

    maintainers("climbfuji", "AlexanderRichert-NOAA")

    version("5.11.4", sha256="4836a876277c9a65a47a3dc87cae116c3009699f8a25bab4e3afabf160bcf212")
    version("5.8.4", sha256="bc628556f8458c269a309e4c3b8d5a807fae7dfd415e27416fe9a3f544f88951")
    version("5.8.3", sha256="1d890008414017da578dbd5a95cb1b4d599f01d5a3bb3e0297fe94a87fbd81a6")
    version("4.13.0", sha256="c743896e0ec1d705edd2abf2ee5a47f4b6f7b1818d8c159b521bdff50a403e39")
    version("4.12.0", sha256="566b797e8d78e3eb93946b923ef540ac61f50d4a17c9203d263c4fd5c39ab1d1")
    version("4.11.1", sha256="b3bcc1255939f87b9ba18d802940e08c0cf6379ca6aeec1fef7bd169b0085d6c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("ssl", default=True, description="Enable SSL")
    variant(
        "static_boost", default=False, description="Use also static boost libraries when compiling"
    )
    variant("ui", default=False, description="Enable ecflow_ui")
    variant("pic", default=False, description="Enable position-independent code (PIC)")

    extends("python")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type="build")
    depends_on("py-pip", type="build")

    # v4: Boost-1.7X release not working well on serialization
    depends_on("boost@1.53:1.69+python", when="@:4")
    depends_on("boost@1.53:1.69+pic", when="@:4 +static_boost")
    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on("boost +filesystem")
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@:4")

    # Use newer boost with v5 up to 1.84.0 - https://github.com/spack/spack/issues/44116
    conflicts("boost@1.85:", when="@:5.11.4")
    depends_on(
        "boost@1.72:+chrono+date_time+exception+filesystem+program_options+python+regex+serialization+system+test+thread+timer",  # noqa
        when="@5:",
    )
    depends_on(
        "boost@1.72:+chrono+date_time+exception+filesystem+program_options+python+regex+serialization+system+test+thread+timer+pic",  # noqa
        when="@5: +static_boost",
    )

    depends_on("openssl@1:", when="@5:")
    depends_on("pkgconfig", type="build", when="+ssl ^openssl ~shared")
    depends_on("qt@5:", when="+ui")
    # Requirement to use the Python3_EXECUTABLE variable
    depends_on("cmake@3.16:", type="build")

    # https://github.com/JCSDA/spack-stack/issues/1001
    # https://github.com/JCSDA/spack-stack/issues/1009
    patch("ctsapi_cassert.patch", when="@5.11.4")
    patch("vfile_cassert.patch", when="@5.11.4")

    @when("@:4.13.0")
    def patch(self):
        version = str(self.spec["python"].version[:2])
        filter_file(
            r"REQUIRED COMPONENTS python3",
            rf"REQUIRED COMPONENTS python{version}",
            "Pyext/CMakeLists.txt",
        )

    @when("+ssl ^openssl~shared")
    def setup_build_environment(self, env):
        env.set("LIBS", self.spec["zlib"].libs.search_flags)

    def cmake_args(self):
        spec = self.spec
        boost_lib = spec["boost"].prefix.lib
        args = [
            self.define("Boost_PYTHON_LIBRARY_RELEASE", boost_lib),
            self.define_from_variant("ENABLE_UI", "ui"),
            self.define_from_variant("ENABLE_GUI", "ui"),
            self.define_from_variant("ENABLE_SSL", "ssl"),
            # https://jira.ecmwf.int/browse/SUP-2641#comment-208943
            self.define_from_variant("ENABLE_STATIC_BOOST_LIBS", "static_boost"),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]

        if spec.satisfies("+ssl ^openssl ~shared"):
            ssllibs = ";".join(spec["openssl"].libs + spec["zlib"].libs)
            args.append(self.define("OPENSSL_CRYPTO_LIBRARY", ssllibs))

        if self.spec.satisfies("@5.8.3:"):
            args.append("-DCMAKE_CXX_FLAGS=-DBOOST_NO_CXX98_FUNCTION_BASE")

        return args

    # A recursive link in the ecflow source code causes the binary cache
    # creation to fail. This file is only in the install tree if the
    # --source option is set when installing the package, but force_remove
    # acts like "rm -f" and won't abort if the file doesn't exist.
    @run_after("install")
    def remove_recursive_symlink_in_source_code(self):
        force_remove(join_path(self.prefix, "share/ecflow/src/cereal/cereal"))

    @when("+ssl ^openssl~shared")
    def patch(self):
        pkgconf = which("pkg-config")
        liblist_l = pkgconf("--libs-only-l", "--static", "openssl", output=str).split()
        liblist = " ".join([ll.replace("-l", "") for ll in liblist_l])
        for sdir in ["Client", "Server"]:
            filter_file(
                "(target_link_libraries.*pthread)",
                f"\\1 {liblist}",
                os.path.join(sdir, "CMakeLists.txt"),
            )
