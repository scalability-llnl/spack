# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class K8(Package):
    """K8 is a Javascript shell based on Google's V8 Javascript engine."""

    homepage = "https://github.com/attractivechaos/k8"
    url = "https://github.com/attractivechaos/k8/releases/download/v0.2.4/k8-0.2.4.tar.bz2"

    version("0.2.4", sha256="da8a99c7f1ce7f0cb23ff07ce10510e770686b906d5431442a5439743c0b3c47")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="run")

    def install(self, spec, prefix):
        if sys.platform == "darwin":
            os.rename("k8-Darwin", "k8")

        if sys.platform != "darwin":
            os.rename("k8-Linux", "k8")
        install_tree(".", prefix.bin)
