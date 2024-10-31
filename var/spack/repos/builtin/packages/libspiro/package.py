# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libspiro(AutotoolsPackage):
    """Spiro is the creation of Raph Levien. It simplifies the drawing of
    beautiful curves."""

    homepage = "https://github.com/fontforge/"
    url = "https://github.com/fontforge/libspiro/archive/20200505.tar.gz"

    license("GPL-3.0-or-later")

    version("20221101", sha256="d5d8af0648e33fe2344c41824823974a32c4e880c4ae9d846ec4414836a421c4")
    version("20200505", sha256="00be530b5c0ea9274baadf6c05521f0b192d4c3c1db636ac8b08efd44aaea8f5")
    version("20190731", sha256="24c7d1ccc7c7fe44ff10c376aa9f96e20e505f417ee72b63dc91a9b34eeac354")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
