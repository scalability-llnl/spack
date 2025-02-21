# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openmpi(Package):
    version("4.1.1")

    variant("internal-hwloc", default=False)
    variant("fabrics", values=any_combination_of("psm", "mxm"))

    depends_on("hwloc", when="~internal-hwloc")
