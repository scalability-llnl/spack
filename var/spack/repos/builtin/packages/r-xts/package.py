# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RXts(RPackage):
    """eXtensible Time Series

    Provide for uniform handling of R's different time-based data classes by
    extending zoo, maximizing native format information preservation and
    allowing for user level customization and extension, while simplifying
    cross-class interoperability."""

    homepage = "http://r-forge.r-project.org/projects/xts/"
    url      = "https://cloud.r-project.org/src/contrib/xts_0.11-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xts"

    version('0.12.1', sha256='d680584af946fc30be0b2046e838cff7b3a65e00df1eadba325ca5e96f3dca2c')
    version('0.11-2', sha256='12772f6a66aab5b84b0665c470f11a3d8d8a992955c027261cfe8e6077ee13b8')
    version('0.9-7', sha256='f11f7cb98f4b92b7f6632a2151257914130880c267736ef5a264b5dc2dfb7098')

    depends_on('r-zoo@1.7-12:', type=('build', 'run'))
