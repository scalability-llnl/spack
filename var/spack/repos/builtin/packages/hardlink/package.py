# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hardlink(MakefilePackage):
    """A simple command-line utility that implements directory hardlinks"""

    homepage = "https://github.com/selkhateeb/hardlink"
    url = "https://github.com/selkhateeb/hardlink/archive/v0.1.1.tar.gz"

    version("0.1.1", sha256="5876554e6dafb6627a94670ac33e750a7efeb3a5fbde5ede3e145cdb5131d1ba")
    version("0.1", sha256="72f8a07b0dfe30a77da576b8dff5998c5f7e054052382fd61ac46157a5e039db")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install-homebrew")
