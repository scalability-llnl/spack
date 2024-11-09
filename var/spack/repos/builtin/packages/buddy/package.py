# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Buddy(AutotoolsPackage):
    """A Binary Decision Diagram library."""

    homepage = "https://sourceforge.net/projects/buddy/"
    url = "https://sourceforge.net/projects/buddy/files/buddy/BuDDy%202.4/buddy-2.4.tar.gz"
    list_url = "https://sourceforge.net/projects/buddy/files/buddy"
    list_depth = 1

    version("2.4", sha256="d3df80a6a669d9ae408cb46012ff17bd33d855529d20f3a7e563d0d913358836")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def configure_args(self):
        if platform.machine() == "aarch64":
            config_args = ["--build=aarch64-unknown-linux-gnu"]
            return config_args
