# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shocklibs(Package):
    """The lib for shock: An object store for scientific data."""

    homepage = "https://github.com/MG-RAST/Shock"
    url = "https://github.com/MG-RAST/Shock/archive/v0.9.24.tar.gz"

    license("BSD-2-Clause")

    version("0.9.29", sha256="81c61f22b869b9923065ee57f9bcf62d95bf266887b09486f6c8e6aa07aa2c0a")
    version("0.9.24", sha256="465d06f33df2570eaf3ffd535a38fc464084ac95a2f145ead5c71f34beeb0a35")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        install_tree("libs", prefix.libs)
