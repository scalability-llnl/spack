# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastme(AutotoolsPackage):
    """FastME is a distance based phylogeny reconstruction program that
    works on distance matrices and, as of v2.0, sequence data."""

    homepage = "http://www.atgc-montpellier.fr/fastme/"
    url = "https://gite.lirmm.fr/atgc/FastME/repository/v2.1.5.1/archive.tar.gz"

    version("2.1.5.1", sha256="1059dcbd320bf4d6dd9328c582dd3d24283295026530fcfb26dbdbe068e3cd1d")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    force_autoreconf = True
