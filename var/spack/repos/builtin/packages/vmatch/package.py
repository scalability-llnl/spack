# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vmatch(Package):
    """Vmatch is a versatile software tool for efficiently solving large scale
    sequence matching tasks"""

    homepage = "http://www.vmatch.de/"
    url = "http://www.vmatch.de/distributions/vmatch-2.3.0-Linux_x86_64-64bit.tar.gz"

    version("2.3.0", sha256="5e18d0dddf04e86dad193fcdde6e48f3901365932634125602d8808f35acf979")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
