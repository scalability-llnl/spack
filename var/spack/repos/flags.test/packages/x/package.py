# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class X(Package):
    version("1.1")
    version("1.0")

    variant("activatemultiflag", default=False)
    depends_on('y cflags="-d1"', when="~activatemultiflag")
    depends_on('y cflags="-d1 -d2"', when="+activatemultiflag")

    depends_on("c", type="build")
