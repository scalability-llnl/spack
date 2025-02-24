# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DependsOnOpenmpi(Package):
    """For testing concretization of packages that use
    `spack external read-cray-manifest`"""

    depends_on("openmpi")

    version("1.0")
    version("0.9")
