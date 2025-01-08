# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPoorman(RPackage):
    """A Poor Man's Dependency Free Recreation of 'dplyr'.

    A replication of key functionality from 'dplyr' and the wider 'tidyverse'
    using only 'base'."""

    cran = "poorman"

    license("MIT")

    version("0.2.7", sha256="089418293cdfde3b46bf53e891a3a8ad924d953a1a7e5ae981de54ebde62b4aa")
    version("0.2.6", sha256="328e0a3e610f17e845d95cd9c0803e0367d6f5835706e8b0ed921fc500983774")
    version("0.2.5", sha256="b92b30ce0f4f02c4fa4a4e90673ef2e0ed8de9b9080dd064506581989fcc0716")

    depends_on("r@3.5:", type=("build", "run"))
    depends_on("r@3.3:", type=("build", "run"), when="@0.2.6:")
