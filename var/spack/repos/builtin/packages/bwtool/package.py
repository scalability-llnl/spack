# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bwtool(AutotoolsPackage):
    """bwtool is a command-line utility for bigWig files."""

    homepage = "https://github.com/CRG-Barcelona/bwtool"
    url = "https://github.com/CRG-Barcelona/bwtool/archive/1.0.tar.gz"

    version("1.0", sha256="2e177573602c129e1d37e07288bdc04bef14d2c25c39636aea8c9a359400594a")

    depends_on("c", type="build")  # generated

    depends_on("libbeato")
