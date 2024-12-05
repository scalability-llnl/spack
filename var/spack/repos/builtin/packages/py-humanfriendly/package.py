# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyHumanfriendly(PythonPackage):
    """Human friendly output for text interfaces using Python"""

    homepage = "https://humanfriendly.readthedocs.io/"
    pypi = "humanfriendly/humanfriendly-8.1.tar.gz"
    git = "https://github.com/xolox/python-humanfriendly.git"

    license("MIT")

    version("10.0", sha256="6b0b831ce8f15f7300721aa49829fc4e83921a9a301cc7f606be6686a2288ddc")
    version("8.2", sha256="bf52ec91244819c780341a3438d5d7b09f431d3f113a475147ac9b7b167a3d12")
    version("8.1", sha256="25c2108a45cfd1e8fbe9cdb30b825d34ef5d5675c8e11e4775c9aedbfb0bdee2")
    version("4.18", sha256="33ee8ceb63f1db61cce8b5c800c531e1a61023ac5488ccde2ba574a85be00a85")

    depends_on("py-setuptools", type="build")
