# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CyrusSasl(AutotoolsPackage):
    """This is the Cyrus SASL API implementation. It can be used on the
    client or server side to provide authentication and authorization
    services."""

    homepage = "https://github.com/cyrusimap/cyrus-sasl"
    url = "https://github.com/cyrusimap/cyrus-sasl/archive/cyrus-sasl-2.1.27.tar.gz"

    license("custom")

    version("2.1.28", sha256="3e38933a30b9ce183a5488b4f6a5937a702549cde0d3287903d80968ad4ec341")
    version("2.1.27", sha256="b564d773803dc4cff42d2bdc04c80f2b105897a724c247817d4e4a99dd6b9976")
    version("2.1.26", sha256="7c14d1b5bd1434adf2dd79f70538617e6aa2a7bde447454b90b84ac5c4d034ba")
    version("2.1.25", sha256="8bfd4fa4def54c760e5061f2a74c278384c3b9807f02c4b07dab68b5894cc7c1")
    version("2.1.24", sha256="1df15c492f7ecb90be49531a347b3df21b041c2e0325dcc4fc5a6e98384c40dd")
    version("2.1.23", sha256="b1ec43f62d68446a6a5879925c63d94e26089c5a46cd83e061dd685d014c7d1f")

    # ensure include time.h, https://github.com/cyrusimap/cyrus-sasl/pull/709
    patch(
        "https://github.com/cyrusimap/cyrus-sasl/commit/266f0acf7f5e029afbb3e263437039e50cd6c262.patch?full_index=1",
        sha256="819342fe68475ac1690136ff4ce9b73c028f433ae150898add36f724a8e2274b",
        when="@2.1.27:2.1.28",
    )
    conflicts("%gcc@14:", when="@:2.1.26")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("groff", type="build")
