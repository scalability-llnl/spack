# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnrm(AutotoolsPackage):
    """Libnrm, the application instrumentation library for the Node
    Resource Manager(NRM)."""

    homepage = "https://xgitlab.cels.anl.gov/argo/libnrm"
    url = "https://www.mcs.anl.gov/research/projects/argo/downloads/libnrm-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version("0.1.0", sha256="f849ada384025fa41251acc2a43aa335e0cb1b9cd1c8ab8b9d1808a036ae551e")

    depends_on("c", type="build")  # generated

    tags = ["e4s"]

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libzmq")
    depends_on("mpi")
