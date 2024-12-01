# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class MongoCDriver(AutotoolsPackage, CMakePackage):
    """libmongoc is a client library written in C for MongoDB."""

    homepage = "https://github.com/mongodb/mongo-c-driver"
    url = "https://github.com/mongodb/mongo-c-driver/archive/refs/tags/1.25.0.tar.gz"

    maintainers("michaelkuhn")

    license("Apache-2.0")

    version("1.27.2", sha256="a53010803e2df097a2ea756be6ece34c8f52cda2c18e6ea21115097b75f5d4bf")
    version("1.24.4", sha256="2f4a3e8943bfe3b8672c2053f88cf74acc8494dc98a45445f727901eee141544")
    version("1.23.3", sha256="c8f951d4f965d455f37ae2e10b72914736fc0f25c4ffc14afc3cbadd1a574ef6")
    version("1.21.0", sha256="840ff79480070f98870743fbb332e2c10dd021b6b9c952d08010efdda4d70ee4")
    version("1.17.6", sha256="8644deec7ae585e8d12566978f2017181e883f303a028b5b3ccb83c91248b150")
    version("1.17.5", sha256="4b15b7e73a8b0621493e4368dc2de8a74af381823ae8f391da3d75d227ba16be")
    version("1.17.0", sha256="90aa23a3f92be0a076fe0b903b68276a7973d4e472929943069f503d5ab50cb9")
    version("1.16.2", sha256="0a722180e5b5c86c415b9256d753b2d5552901dc5d95c9f022072c3cd336887e")
    version("1.9.5", sha256="4a4bd0b0375450250a3da50c050b84b9ba8950ce32e16555714e75ebae0b8019")
    version("1.9.4", sha256="910c2f1b2e3df4d0ea39c2f242160028f90fcb8201f05339a730ec4ba70811fb")
    version("1.9.3", sha256="c2c94ef63aaa09efabcbadc4ac3c8740faa102266bdd2559d550f1955b824398")
    version("1.9.1", sha256="91951444d34581deeaff46cc2985c68805754f618a20ac369b761ce9b621c4cd")
    version("1.8.1", sha256="87d87b7581018cde7edff85f522d43d9c0a226df26fa53b77ca1613a3aca8233")
    version("1.8.0", sha256="1b53883b4cbf08e7d77ad7ab7a02deca90b1719c67f9ad132b47e60d0206ea4e")
    version("1.7.0", sha256="48a0dbd44fef2124b51cf501f06be269b1a39452303b880b37473a6030c6e023")
    version("1.6.3", sha256="82df03de117a3ccf563b9eccfd2e5365df8f215a36dea7446d439969033ced7b")
    version("1.6.2", sha256="7ec27e9be4da2bf9e4b316374f8c29f816f0a0f019b984411777e9681e17f70e")
    version(
        "1.6.1",
        sha256="1bdfb27944c6da8e56da209a5d56efac70df1f8c4ca4498b46f75bf3f9360898",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("ssl", default=True, description="Enable SSL support.")
    variant("snappy", default=True, description="Enable Snappy support.")
    variant("zlib", default=True, description="Enable zlib support.")
    variant("zstd", default=True, description="Enable zstd support.")

    patch(
        "https://github.com/mongodb/mongo-c-driver/pull/466.patch?full_index=1",
        sha256="d8802d91226c176ba46d5b82413757121331d556a3a3d57ab65b70e175cab296",
        when="@1.8.1",
    )

    with when("build_system=cmake"):
        depends_on("cmake@3.1:", type="build")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build", when="@1.8.1")
        depends_on("automake", type="build", when="@1.8.1")
        depends_on("libtool", type="build", when="@1.8.1")

    build_system(
        conditional("cmake", when="@1.10:"),
        conditional("autotools", when="@:1.9"),
        default="cmake",
    )

    def url_for_version(self, version):
        if version >= Version("1.25.0"):
            return f"https://github.com/mongodb/mongo-c-driver/archive/refs/tags/{version}.tar.gz"
        if version >= Version("1.10.0"):
            return f"https://github.com/mongodb/mongo-c-driver/releases/download/{version}/mongo-c-driver-{version}.tar.gz"
        else:
            return f"https://github.com/mongodb/libbson/releases/download/{version}/libbson-{version}.tar.gz"

    depends_on("pkgconfig", type="build")

    # When updating mongo-c-driver, libbson has to be kept in sync.
    depends_on("libbson@1.27", when="@1.27")
    depends_on("libbson@1.24", when="@1.24")
    depends_on("libbson@1.23", when="@1.23")
    depends_on("libbson@1.21", when="@1.21")
    depends_on("libbson@1.17", when="@1.17")
    depends_on("libbson@1.16", when="@1.16")
    depends_on("libbson@1.9", when="@1.9")
    depends_on("libbson@1.8", when="@1.8")
    depends_on("libbson@1.7", when="@1.7")
    depends_on("libbson@1.6", when="@1.6")

    depends_on("openssl", when="+ssl")
    depends_on("snappy", when="+snappy")
    depends_on("zlib-api", when="+zlib")
    depends_on("zstd", when="+zstd")

    @property
    def force_autoreconf(self):
        # Run autoreconf due to build system patch
        return self.spec.satisfies("@1.8.1")


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("ENABLE_AUTOMATIC_INIT_AND_CLEANUP", False),
            self.define("ENABLE_MONGOC", True),
            self.define("MONGO_USE_CCACHE", False),
            self.define("MONGO_USE_LLD", False),
            self.define_from_variant("ENABLE_SNAPPY", "snappy"),
            self.define_from_variant("ENABLE_ZSTD", "zstd"),
        ]

        if self.spec.satisfies("@1.24:"):
            args.append(self.define("USE_SYSTEM_LIBBSON", True))
        else:
            args.append(self.define("ENABLE_BSON", "SYSTEM"))

        if self.spec.satisfies("+ssl"):
            args.append(self.define("ENABLE_SSL", "OPENSSL"))
        else:
            args.append(self.define("ENABLE_SSL", False))

        if self.spec.satisfies("+zlib"):
            args.append(self.define("ENABLE_ZLIB", "SYSTEM"))
        else:
            args.append(self.define("ENABLE_ZLIB", False))

        return args


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec

        args = ["--disable-automatic-init-and-cleanup", "--with-libbson=system"]

        if "+ssl" in spec:
            args.append("--enable-ssl=openssl")
        else:
            args.append("--enable-ssl=no")

        if spec.satisfies("@1.7.0:"):
            # --with-{snappy,zlib}=system are broken for versions < 1.8.1
            if "+snappy" not in spec:
                args.append("--with-snappy=no")
            elif spec.satisfies("@1.8.1:"):
                args.append("--with-snappy=system")

            if "+zlib" not in spec:
                args.append("--with-zlib=no")
            elif spec.satisfies("@1.8.1:"):
                args.append("--with-zlib=system")

        return args
