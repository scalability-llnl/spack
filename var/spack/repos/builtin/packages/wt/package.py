# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Wt(CMakePackage):
    """Wt, C++ Web Toolkit.

    Wt is a C++ library for developing web applications."""

    homepage = "https://www.webtoolkit.eu/wt"
    url = "https://github.com/emweb/wt/archive/3.3.7.tar.gz"
    git = "https://github.com/emweb/wt.git"

    version("master", branch="master")
    version("3.3.7", sha256="054af8d62a7c158df62adc174a6a57610868470a07e7192ee7ce60a18552851d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # wt builds in parallel, but requires more than 5 GByte RAM per -j <njob>
    # which most machines do not provide and crash the build
    parallel = False

    variant(
        "openssl",
        default=True,
        description="SSL and WebSockets support in the built-in httpd, "
        "the HTTP(S) client, and additional cryptographic "
        "hashes in the authentication module",
    )
    variant("libharu", default=True, description="painting to PDF")
    # variant('graphicsmagick', default=True,
    #         description='painting to PNG, GIF')
    variant("sqlite", default=False, description="create SQLite3 DBO")
    variant("mariadb", default=False, description="create MariaDB/MySQL DBO")
    variant("postgresql", default=False, description="create PostgreSQL DBO")
    # variant('firebird', default=False, description='create Firebird DBO')
    variant(
        "pango",
        default=True,
        description="improved font support in PDF and raster image " "painting",
    )
    variant("zlib", default=True, description="compression in the built-in httpd")
    # variant('fastcgi', default=False,
    #         description='FastCGI connector via libfcgi++')

    depends_on("pkgconfig", type="build")
    depends_on("boost@1.46.1:1.65")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("openssl", when="+openssl")
    depends_on("libharu", when="+libharu")
    depends_on("sqlite", when="+sqlite")
    depends_on("mariadb", when="+mariadb")
    depends_on("postgresql", when="+postgresql")
    depends_on("pango", when="+pango")
    depends_on("zlib-api", when="+zlib")

    def cmake_args(self):
        cmake_args = [
            "-DBUILD_EXAMPLES:BOOL=OFF",
            "-DCONNECTOR_FCGI:BOOL=OFF",
            "-DENABLE_OPENGL:BOOL=OFF",
            "-DENABLE_QT4:BOOL=OFF",
        ]
        cmake_args.extend(
            [
                self.define_from_variant("ENABLE_SSL", "openssl"),
                self.define_from_variant("ENABLE_HARU", "libharu"),
                self.define_from_variant("ENABLE_PANGO", "pango"),
                self.define_from_variant("ENABLE_SQLITE", "sqlite"),
                self.define_from_variant("ENABLE_MYSQL", "mariadb"),
                self.define_from_variant("ENABLE_POSTGRES", "postgresql"),
            ]
        )
        return cmake_args
