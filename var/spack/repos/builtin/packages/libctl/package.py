# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libctl(AutotoolsPackage):
    """libctl is a free Guile-based library implementing flexible
    control files for scientific simulations."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Libctl"
    git = "https://github.com/NanoComp/libctl.git"
    url = "https://github.com/NanoComp/libctl/releases/download/v4.2.0/libctl-4.2.0.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("4.5.1", sha256="fcfeb2f13dda05b560f0ec6872757d9318fdfe8f4bc587eb2053a29ba328ae25")
    version("4.5.0", sha256="621e46a238c4d5e8ce0866183f8e04abac6e1a94d90932af0d56ee61370ea153")
    version("4.2.0", sha256="0341ad6ea260ecda2efb3d4b679abb3d05ca6211792381979b036177a9291975")
    version(
        "3.2.2",
        sha256="8abd8b58bc60e84e16d25b56f71020e0cb24d75b28bc5db86d50028197c7efbc",
        url="http://ab-initio.mit.edu/libctl/libctl-3.2.2.tar.gz",
    )

    depends_on("c", type="build")  # generated

    depends_on("guile")

    def configure_args(self):
        spec = self.spec

        return [
            "--enable-shared",
            "GUILE={0}".format(join_path(spec["guile"].prefix.bin, "guile")),
            "GUILE_CONFIG={0}".format(join_path(spec["guile"].prefix.bin, "guile-config")),
            "LIBS=-lm",
        ]
