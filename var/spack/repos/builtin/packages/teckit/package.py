# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Teckit(AutotoolsPackage):
    """TECkit is a low-level toolkit intended to be used by applications for
    conversions between text encodings. For example, it can be used when
    importing legacy text into a Unicode-based application.

    The primary component of TECkit is a library: the TECkit engine. The engine
    relies on mapping tables in a specific, documented binary format. The
    TECkit compiler creates these tables from plain-text, human-readable
    descriptions."""

    maintainers("rountree")
    homepage = "https://scripts.sil.org/cms/scripts/page.php?cat_id=TECkit"
    git = "https://github.com/silnrsi/teckit.git"

    license("CPL-1.0")

    version("2.5.11", commit="fea17dbf17266387c96f74fd9c0ce44d065f0f50")
    version("2.5.10", commit="1c510d4de7ff844207b1273e856fd27a15b3486d")
    version("2.5.9", commit="e2434cef98d59487514450304513efb42c376365")
    version("2.5.8", commit="f7838e4e61329ae8e1a788a3d35f7865c68c4da5")
    version("2.5.7", commit="50c7346dc3c887b16b26c3ff269fd4cfc9f8a892")
    version("2.5.6", commit="41c20be2793e1afcbb8de6339af89d1eeab84fe8")
    version("2.5.5", commit="2733fd9895819e3697257550cc39b8e419c1ee7e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def configure_args(self):
        args = ["--with-system-zlib"]
        return args

    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("./autogen.sh")
