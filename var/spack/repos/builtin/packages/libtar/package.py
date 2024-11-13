# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtar(AutotoolsPackage):
    """libtar is a library for manipulating tar files from within C
    programs."""

    homepage = "https://repo.or.cz/libtar.git"
    url = "https://github.com/tklauser/libtar/archive/v1.2.20.tar.gz"

    version("1.2.20", sha256="3152fc61cf03c82efbf99645596efdadba297eac3e85a52ae189902a072c9a16")
    version("1.2.19", sha256="5fea7152106b1b8cda109da27f505439865dd196da94f503fab18264591ddf64")
    version("1.2.18", sha256="a5ac82dae9677b5b74333ed63043b9699c7ef561e2eacf301188c277952d4b7d")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
