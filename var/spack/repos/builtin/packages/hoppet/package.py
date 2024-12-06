# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hoppet(AutotoolsPackage):
    """A Fortran 95 package for carrying out QCD DGLAP evolution and other
    common manipulations of parton distribution functions (PDFs)."""

    homepage = "https://hoppet.hepforge.org/"
    url = "https://github.com/gavinsalam/hoppet/archive/refs/tags/hoppet-1.2.0.tar.gz"

    tags = ["hep"]
    maintainers("haralmha")

    version("1.2.0", sha256="6e00eb56a4f922d03dfceba7b389a3aaf51f277afa46d7b634d661e0797e8898")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
