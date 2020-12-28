# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCodetools(RPackage):
    """Code analysis tools for R."""

    homepage = "https://cloud.r-project.org/package=codetools"
    url      = "https://cloud.r-project.org/src/contrib/codetools_0.2-15.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/codetools"

    version('0.2-16', sha256='f67a66175cb5d8882457d1e9b91ea2f16813d554fa74f80c1fd6e17cf1877501')
    version('0.2-15', sha256='4e0798ed79281a614f8cdd199e25f2c1bd8f35ecec902b03016544bd7795fa40')
    version('0.2-14', sha256='270d603b89076081af8d2db0256927e55ffeed4c27309d50deea75b444253979')

    depends_on('r@2.1:', type=('build', 'run'))
