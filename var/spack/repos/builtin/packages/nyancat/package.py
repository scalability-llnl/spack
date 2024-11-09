# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Nyancat(MakefilePackage):
    """Nyancat in your terminal, rendered through ANSI escape sequences."""

    homepage = "https://nyancat.dakko.us/"
    url = "https://github.com/klange/nyancat/archive/1.5.1.tar.gz"

    license("NCSA")

    version("1.5.2", sha256="88cdcaa9c7134503dd0364a97fa860da3381a09cb555c3aae9918360827c2032")
    version("1.5.1", sha256="c948c769d230b4e41385173540ae8ab1f36176de689b6e2d6ed3500e9179b50a")
    version("1.5.0", sha256="9ae4f740060b77bba815d8d4e97712d822bd0812a118b88b7fd6b4136a971bce")
    version("1.4.5", sha256="b26d752b95088be9d5caa73daea884572c0fc836ba55f0062e4d975301c4c661")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(
            r"install src/nyancat /usr/bin/\${package}",
            "install src/nyancat {0}/{1}".format(prefix.bin, "${package}"),
        )
        makefile.filter(
            "gzip -9 -c < nyancat.1 > /usr/share/man/man1/nyancat.1.gz",
            "gzip -9 -c < {1}.1 > {0}/{1}.1.gz".format(prefix.man.man1, "${package}"),
        )
        mkdirp(prefix.bin)
        mkdirp(prefix.man.man1)
