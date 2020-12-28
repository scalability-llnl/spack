# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGtable(RPackage):
    """Tools to make it easier to work with "tables" of 'grobs'."""

    homepage = "https://cloud.r-project.org/package=gtable"
    url      = "https://cloud.r-project.org/src/contrib/gtable_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gtable"

    version('0.3.0', sha256='fd386cc4610b1cc7627dac34dba8367f7efe114b968503027fb2e1265c67d6d3')
    version('0.2.0', sha256='801e4869830ff3da1d38e41f5a2296a54fc10a7419c6ffb108582850c701e76f')

    depends_on('r@3.0:', type=('build', 'run'))
