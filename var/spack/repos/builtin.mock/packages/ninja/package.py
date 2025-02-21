# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ninja(Package):
    """Dummy Ninja Package"""

    homepage = "https://ninja-build.org/"
    url = "https://github.com/ninja-build/ninja/archive/v1.7.2.tar.gz"

    version("1.10.2", sha256="ce35865411f0490368a8fc383f29071de6690cbadc27704734978221f25e2bed")

    def setup_dependent_package(self, module, dspec):
        module.ninja = Executable(self.spec.prefix.bin.ninja)
