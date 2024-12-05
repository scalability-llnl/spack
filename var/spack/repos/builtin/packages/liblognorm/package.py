# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblognorm(AutotoolsPackage):
    """Liblognorm is a fast-samples based normalization library."""

    homepage = "https://www.liblognorm.com/"
    url = "https://github.com/rsyslog/liblognorm/archive/v2.0.6.tar.gz"

    license("LGPL-2.1-or-later AND Apache-2.0")

    version("2.0.6", sha256="594ea3318ef419cb7f21cf81c513db35a838b32207999a11a82b709da9ff9a2b")
    version("2.0.5", sha256="dd779b6992de37995555e1d54caf0716a694765efc65480eed2c713105ab46fe")
    version("2.0.4", sha256="af4d7d8ce11fb99514169f288163f87cb9ade1cb79595656d96b51b2482c493d")
    version("2.0.3", sha256="fac2a6a5adbeb63d06a63ab2e398b3fac8625d0ea69db68f1d81196897a9d687")
    version("2.0.2", sha256="bdd08e9837e8fcca5029ec12c9fb9f16593313f9d743625bab062250e0daa5d8")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("libestr")
    depends_on("libfastjson")
