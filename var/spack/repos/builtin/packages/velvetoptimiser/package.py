# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Velvetoptimiser(Package):
    """Automatically optimise three of Velvet's assembly parameters."""

    homepage = "https://github.com/tseemann/VelvetOptimiser"
    url = "https://github.com/tseemann/VelvetOptimiser/archive/2.2.6.tar.gz"

    license("GPL-2.0-or-later")

    version("2.2.6", sha256="b407db61b58ed983760b80a3a40c8f8a355851ecfab3e61a551bed29bf5b40b3")

    depends_on("velvet@1.1:", type="run")
    depends_on("perl@5.8.8:", type="run")
    depends_on("perl-bioperl@1.4:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
