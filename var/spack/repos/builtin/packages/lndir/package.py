# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lndir(AutotoolsPackage, XorgPackage):
    """lndir - create a shadow directory of symbolic links to another
    directory tree."""

    homepage = "https://gitlab.freedesktop.org/xorg/util/lndir"
    xorg_mirror_path = "util/lndir-1.0.3.tar.gz"

    version("1.0.5", sha256="2be863f59e6833955b11295c43d79ab32464a8706d29072171cd8da95922a7a2")
    version("1.0.4", sha256="b448b49a55d0750acfc3fd992c2511b21838ec2cea870d109bb9fdca2ac028da")
    version("1.0.3", sha256="95b2d26fb3cbe702f828146c7a4c7c48001d2da52b062580227b7b68180be902")

    depends_on("c", type="build")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
