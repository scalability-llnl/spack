# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IsoCodes(AutotoolsPackage):
    """ISO-codes provides lists of various ISO standards"""

    homepage = "https://salsa.debian.org/iso-codes-team/iso-codes"
    url = "https://deb.debian.org/debian/pool/main/i/iso-codes/iso-codes_4.3.orig.tar.xz"

    license("LGPL-2.1-or-later")

    version("4.16.0", sha256="d37ff1b2b76e63926e8043b42e0ff806bb4e41e2a57d93c9d4ec99c06b409530")
    version("4.15.0", sha256="3d50750bf1d62d83b6085f5815ceb8392df34266a15f16bcf8d4cf7eb15d245c")
    version("4.13.0", sha256="2d4d0e5c02327f52cf7c029202da72f2074348472c26904b7104d2be3e0750ef")
    version("4.3", sha256="643eb83b2d714e8650ed7112706968d057bf5b101ba71c8ef219e20f1737b141")

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("gettext", type="build")
    depends_on("python@3:", type="build")
