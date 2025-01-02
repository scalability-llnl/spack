# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class V(Package):
    version("4.1")
    version("4.0")

    depends_on("y")

    depends_on("c", type="build")
