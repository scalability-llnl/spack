# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPcapp(RPackage):
    """Provides functions for robust PCA by projection pursuit."""

    homepage = "https://cloud.r-project.org/package=pcaPP"
    url      = "https://cloud.r-project.org/src/contrib/pcaPP_1.9-72.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pcaPP"

    version('1.9-73', sha256='ca4566b0babfbe83ef9418283b08a12b3420dc362f93c6562f265df7926b53fc')
    version('1.9-72.1', sha256='a9e39ee15a650930c07672092f9f0c431807869b68b5471037eb7290a4d65bd5')
    version('1.9-72', sha256='58bd0bfb5931aecd734801654bac95f28dab6d30fd043c66c5b719b497104844')
    version('1.9-70', sha256='359e2b376b8b7e2de68b0f33f772d99ecbe9a94f8f460574ac2e3c07513c96d5')
    version('1.9-61', sha256='7dc395e159ff1a56135baaf0b1bea40f871c30f6dadd38992f4ccdfc4e88dc29')
    version('1.9-60', sha256='9a4b471957ac39ed7c860e3165bf8e099b5b55cf814654adb58f9d19df2718e7')
    version('1.9-50', sha256='137637314fba6e11883c63b0475d8e50aa7f363e064baa1e70245f7692565b56')

    depends_on('r-mvtnorm', type=('build', 'run'))
