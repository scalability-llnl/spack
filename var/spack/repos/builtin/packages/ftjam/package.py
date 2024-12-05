# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftjam(AutotoolsPackage):
    """Jam is a small open-source build tool that
    can be used as a replacement for Make."""

    homepage = "https://freetype.org/jam/"
    url = "https://sourceforge.net/projects/freetype/files/ftjam/2.5.2/ftjam-2.5.2.tar.gz"

    version("2.5.2", sha256="a5d456f65477d77936e1726f5f803a2e6def18a6c6fccf5ea8528926c136abc8")

    depends_on("c", type="build")  # generated

    depends_on("bison")
