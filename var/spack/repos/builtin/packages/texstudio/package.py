# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Texstudio(QMakePackage):
    """TeXstudio is a fully featured LaTeX editor, whose goal is to make
    writing LaTeX documents as easy and comfortable as possible."""

    homepage = "https://www.texstudio.org"
    url = "https://github.com/texstudio-org/texstudio/archive/2.12.16.tar.gz"
    git = "https://github.com/texstudio-org/texstudio.git"

    license("GPL-3.0-or-later")

    version("master", branch="master")
    version("3.0.1", sha256="0a2a7d266fecdfa3ea4a454fd66833a54590e610f880c6a97644cdcfc2116191")
    version("3.0.0", sha256="c1f704f84b2007621c5f8ec7fd3b4cf96693f98fd25724ee8fe9c3dccdc7ab2a")

    version("2.12.16", sha256="a14b8912bfd15d982cfbe5f00deed37ca85fb6e38d3aa0c2dac23b4ecaab0984")
    version("2.12.14", sha256="61df71f368bbf21f865645534f63840fd48dbd2996d6d0188aa26d3b647fede0")
    version("2.12.12", sha256="5978daa806c616f9a1eea231bb613f0bc1037d7d2435ee5ca6b14fe88a2caa8c")
    version("2.12.10", sha256="92cf9cbb536e58a5929611fa40438cd9d7ea6880022cd3c5de0483fd15d3df0b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "poppler",
        default=True,
        description="Compile with Poppler library for internal pdf preview",
    )

    # Base dependencies
    depends_on("poppler+qt", when="+poppler")
    # There is a known issue with QT 5.10
    # See https://github.com/texstudio-org/texstudio/wiki/Compiling
    depends_on("qt@4.4.4:5.9,5.11.0:")

    conflicts("target=aarch64:", when="@:2.12.22")

    def qmake_args(self):
        args = ["PREFIX={0}".format(self.prefix)]

        if self.spec.satisfies("+poppler"):
            args.append("INCLUDEPATH+={0}".format(self.spec["poppler"].prefix.include))
            args.append("LIBS+={0}".format(self.spec["poppler"].libs.search_flags))
        else:
            args.append("NO_POPPLER_PREVIEW=true")

        return args
