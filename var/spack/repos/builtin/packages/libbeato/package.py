# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libbeato(AutotoolsPackage):
    """libbeato is a C library containing routines for various uses in Genomics,
    and includes a copy of the freeware portion of the C library
    from UCSC's Genome Browser Group."""

    homepage = "https://github.com/CRG-Barcelona/libbeato"
    git = "https://github.com/CRG-Barcelona/libbeato.git"

    license("GPL-3.0-or-later")

    version("master", branch="master")

    depends_on("c", type="build")  # generated
