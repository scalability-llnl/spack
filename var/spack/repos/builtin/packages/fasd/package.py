# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fasd(MakefilePackage):
    """Fasd (pronounced similar to "fast") is a command-line productivity
    booster. Fasd offers quick access to files and directories for POSIX shells.
    """

    homepage = "https://github.com/clvv/fasd"
    url = "https://github.com/clvv/fasd/archive/refs/tags/1.0.1.tar.gz"
    git = "https://github.com/clvv/fasd.git"

    license("MIT")

    version("1.0.1", sha256="88efdfbbed8df408699a14fa6c567450bf86480f5ff3dde42d0b3e1dee731f65")

    def install(self, spec, prefix):
        make("PREFIX={0}".format(prefix), "install")
