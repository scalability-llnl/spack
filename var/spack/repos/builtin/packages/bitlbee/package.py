# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bitlbee(AutotoolsPackage):
    """An IRC to other chat networks gateway."""

    homepage = "https://www.bitlbee.org/"
    url = "https://github.com/bitlbee/bitlbee/archive/3.5.1.tar.gz"

    license("GPL-2.0-or-later")

    version("3.6-1", sha256="81c6357fe08a8941221472e3790e2b351e3a8a41f9af0cf35395fdadbc8ac6cb")
    version("3.6", sha256="6ec3a1054eaa98eaaabe6159cb4912cfd6286f71adcfa970419b273b38fdfe0c")
    version("3.5-2", sha256="cdcf3ed829d1905b73687b6aa189bbfaf9194f886d9fc7156646827dc0384fdb")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("gnutls")
    depends_on("libgcrypt")
