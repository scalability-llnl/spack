# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXfun(RPackage):
    """Miscellaneous functions commonly used in other packages maintained by
    'Yihui Xie'."""

    homepage = "https://github.com/yihui/xfun"
    url      = "https://cloud.r-project.org/src/contrib/xfun_0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xfun"

    version('0.8', sha256='c2f8ecf8b57ddec02f9be7f417d9e22fc1ae2c7db8d70aa703fc62bf4a5c5416')
