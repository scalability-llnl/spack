# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmbim(AutotoolsPackage):
    """Libmbim is a glib-based library for talking to WWAN modems and
    devices which speak the Mobile Interface Broadband Model (MBIM)
    protocol."""

    homepage = "https://github.com/linux-mobile-broadband/libmbim/"
    url = "https://github.com/linux-mobile-broadband/libmbim/archive/1.20.4.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("1.20.4", sha256="edb56afb862a7756dc097086d8fa791c93332f6f1daf27759eff6ddc99a0f50d")
    version("1.18.0", sha256="47003bfdf78bf32009a1d917f30c063079fa5bd4afc739d6d8ec356070b270df")
    version("1.16.2", sha256="06b7a9e8430c6ab213d96c71a71469aefc86deb52cffd5e4f75121d9a79545e2")
    version("1.16.0", sha256="d123426678f415c2ac4544534ed8a9ff54d133c2ba8c982ce667b793e54f8e99")
    version("1.14.4", sha256="4b2e8723ea50b2e1d22695850c40abb9f7bcb713ea3b9f91f2c350aaa6ae8d1c")
    version("1.14.2", sha256="bf161c4f78327f8422fd6a820e7e5571d99b719af45429e581bfd6a1585fe4a8")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("glib@:2.62.0")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
