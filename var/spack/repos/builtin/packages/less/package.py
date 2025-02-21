# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Less(AutotoolsPackage):
    """The less utility is a text file browser that resembles more, but
    has more capabilities.  Less allows you to move backwards in the
    file aswell as forwards."""

    homepage = "https://www.greenwoodsoftware.com/less/"
    url = "https://www.greenwoodsoftware.com/less/less-551.zip"
    list_url = "https://www.greenwoodsoftware.com/less/download.html"

    depends_on("ncurses")

    license("GPL-3.0-or-later OR BSD-2-Clause", checked_by="wdconinc")

    depends_on("c", type="build")

    version("668", sha256="dbc0de59ea9c50e1e8927e6b077858db3a84954e767909bc599e6e6f602c5717")
    version("661", sha256="a900e3916738bf8c1a0a2a059810f1c59b8271ac8bb46898c6e921ea6aefd757")
    version("643", sha256="3bb417c4b909dfcb0adafc371ab87f0b22e8b15f463ec299d156c495fc9aa196")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-46663
        version("590", sha256="69056021c365b16504cf5bd3864436a5e50cb2f98b76cd68b99b457064139375")
        version("551", sha256="2630db16ef188e88b513b3cc24daa9a798c45643cc7da06e549c9c00cfd84244")
        version("530", sha256="8c1652ba88a726314aa2616d1c896ca8fe9a30253a5a67bc21d444e79a6c6bc3")
