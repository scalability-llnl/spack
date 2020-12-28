# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHttpcode(RPackage):
    """httpcode: 'HTTP' Status Code Helper"""

    homepage = "https://github.com/sckott/httpcode"
    url      = "https://cloud.r-project.org/src/contrib/httpcode_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/httpcode"

    version('0.2.0', sha256='fbc1853db742a2cc1df11285cf27ce2ea43bc0ba5f7d393ee96c7e0ee328681a')
