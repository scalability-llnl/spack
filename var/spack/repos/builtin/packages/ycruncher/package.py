# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ycruncher(Package):
    """
    y-cruncher is a program that can compute Pi and other constants to
    trillions of digits. It is the first of its kind that is multi-threaded
    and scalable to multi-core systems
    """

    homepage = "http://www.numberworld.org/y-cruncher/"
    url = "http://www.numberworld.org/y-cruncher/y-cruncher%20v0.7.10.9513-static.tar.xz"
    maintainers("saqibkh")

    version(
        "0.7.10.9513", sha256="292006496bba83bf0f8c354ceb1c2ea571f0c67b9fe46297701a8d387773db1b"
    )

    depends_on("autoconf")

    def install(self, spec, prefix):
        install_tree(".", prefix)
