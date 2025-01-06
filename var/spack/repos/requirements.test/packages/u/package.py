# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class U(Package):
    version("1.1")
    version("1.0")

    depends_on("c", type="build")
