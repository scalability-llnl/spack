# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiomUtils(RPackage):
    """Provides utilities to facilitate import, export and computation with
    the BIOM (Biological Observation Matrix) format (http://biom-format.org).
    """

    homepage = "https://github.com/braithwaite/BIOM.utils/"
    url      = "https://cloud.r-project.org/src/contrib/BIOM.utils_0.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/biom/"

    version('0.9', sha256='e7024469fb38e275aa78fbfcce15b9a7661317f632a7e9b8124695e076839375')

    depends_on('r@3:', type=('build', 'run'))
