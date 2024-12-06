# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librttopo(AutotoolsPackage):
    """
    The RT Topology Library exposes an API to create and manage standard \
    (ISO 13249 aka SQL/MM) topologies using user-provided data stores.
    """

    homepage = "https://git.osgeo.org/gitea/rttopo"
    url = "https://git.osgeo.org/gitea/rttopo/librttopo/archive/librttopo-1.1.0.tar.gz"
    git = "https://git.osgeo.org/gitea/rttopo/librttopo.git"

    license("GPL-2.0-or-later")

    version("1.1.0", sha256="2e2fcabb48193a712a6c76ac9a9be2a53f82e32f91a2bc834d9f1b4fa9cd879f")

    depends_on("c", type="build")  # generated

    depends_on("geos")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
