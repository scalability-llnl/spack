# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCodetools(RPackage):
    """Code analysis tools for R."""

    homepage = "https://cloud.r-project.org/package=codetools"
    url      = "https://cloud.r-project.org/src/contrib/codetools_0.2-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/codetools"

    version('0.2-18', sha256='1a9ea6b9792dbd1688078455929385acc3a5e4bef945c77bec1261fa4a084c28')
    version('0.2-16', sha256='c276757c3adabaf700f2ea25835892b09bc1bd438ebd17c805ea9073ed8a74b6')
    version('0.2-15', sha256='4e0798ed79281a614f8cdd199e25f2c1bd8f35ecec902b03016544bd7795fa40')
    version('0.2-14', sha256='270d603b89076081af8d2db0256927e55ffeed4c27309d50deea75b444253979')

    depends_on('r@2.1:', type=('build', 'run'))
