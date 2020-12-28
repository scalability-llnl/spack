# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPopgenome(RPackage):
    """PopGenome is an efficient Swiss army knife for population genetics data
       analysis, able to process individual loci, large sets of loci, or whole
       genomes."""

    homepage = "https://popgenome.weebly.com"
    url      = "https://cloud.r-project.org/src/contrib/PopGenome_2.6.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/PopGenome"

    version('2.7.1', sha256='a84903b151528fa026ccaba42ada22cd89babbc1824afd40269b7204e488a5fa')
    version('2.6.1', sha256='7a2922ed505fa801117a153e479d246bcf4854b91c6ab0241acc620a9d779b1c')

    depends_on('r@2.14.2:', type=('build', 'run'))
    depends_on('r-ff', type=('build', 'run'))
