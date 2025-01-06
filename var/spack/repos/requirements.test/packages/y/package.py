# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Y(Package):
    version("2.5")
    version("2.4")
    version("2.3", deprecated=True)

    variant("shared", default=True, description="Build shared libraries")

    depends_on("c", type="build")
