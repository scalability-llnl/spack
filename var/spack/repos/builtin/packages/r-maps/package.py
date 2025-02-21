# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMaps(RPackage):
    """Draw Geographical Maps.

    Display of maps. Projection code and larger maps are in separate packages
    ('mapproj' and 'mapdata')."""

    cran = "maps"

    license("GPL-2.0-only")

    version("3.4.2", sha256="53e57b889f1779cfd4a116a8ed3eded7ed29a73a1b9506248772a389c8404b0c")
    version("3.4.1", sha256="e693a5218ed8122e92d73a98a475d9016f2293c7852c8048677daa7649086400")
    version("3.4.0", sha256="7918ccb2393ca19589d4c4e77d9ebe863dc6317ebfc1ff41869dbfaf439f5747")
    version("3.3.0", sha256="199afe19a4edcef966ae79ef802f5dcc15a022f9c357fcb8cae8925fe8bd2216")
    version("3.2.0", sha256="437abeb4fa4ad4a36af6165d319634b89bfc6bf2b1827ca86c478d56d670e714")
    version("3.1.1", sha256="972260e5ce9519ecc09b18e5d7a28e01bed313fadbccd7b06c571af349cb4d2a")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.4.0:")
