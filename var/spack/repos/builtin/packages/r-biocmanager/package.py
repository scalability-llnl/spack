# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocmanager(RPackage):
    """BiocManager: Access the Bioconductor Project Package Repository"""

    homepage = "https://cloud.r-project.org/package=BiocManager"
    url      = "https://cloud.r-project.org/src/contrib/BiocManager_1.30.10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/BiocManager"

    version('1.30.10', sha256='f3b7a412b42be0ab8df5fcd9bf981876ba9e5c55bc5faaca7af7ede3b6d0c90e')
