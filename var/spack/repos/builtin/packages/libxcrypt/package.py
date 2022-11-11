# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxcrypt(AutotoolsPackage):
    """libxcrypt is a modern library for one-way hashing of passwords."""

    homepage = "https://github.com/besser82/libxcrypt"
    url = "https://github.com/besser82/libxcrypt/releases/download/v4.4.30/libxcrypt-4.4.30.tar.xz"

    def url_for_version(self, version):
        if version <= Version("4.4.17"):
            return "https://github.com/besser82/libxcrypt/archive/v{}.tar.gz".format(version)
        return "https://github.com/besser82/libxcrypt/releases/download/v{}/libxcrypt-{}.tar.xz".format(
            version, version
        )

    version("4.4.30", sha256="b3667f0ba85daad6af246ba4090fbe53163ad93c8b6a2a1257d22a78bb7ceeba")
    version("4.4.17", sha256="7665168d0409574a03f7b484682e68334764c29c21ca5df438955a381384ca07")
    version("4.4.16", sha256="a98f65b8baffa2b5ba68ee53c10c0a328166ef4116bce3baece190c8ce01f375")
    version("4.4.15", sha256="8bcdef03bc65f9dbda742e56820435b6f13eea59fb903765141c6467f4655e5a")

    patch("truncating-conversion.patch", when="@4.4.30")

    def configure_args(self):
        # Disable test dependency on Python (Python itself depends on libxcrypt).
        return ["ac_cv_path_python3_passlib=not found"]

    with when("@:4.4.17"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")
        depends_on("m4", type="build")
