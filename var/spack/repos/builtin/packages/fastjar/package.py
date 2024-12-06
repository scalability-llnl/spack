# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastjar(AutotoolsPackage):
    """Fastjar is a version of Sun's 'jar' utility, written entirely in C."""

    homepage = "https://savannah.nongnu.org/projects/fastjar/"
    url = "http://download.savannah.gnu.org/releases/fastjar/fastjar-0.98.tar.gz"

    license("GPL-2.0")

    version("0.98", sha256="f156abc5de8658f22ee8f08d7a72c88f9409ebd8c7933e9466b0842afeb2f145")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
