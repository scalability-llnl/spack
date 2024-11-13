# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pslib(AutotoolsPackage):
    """C-library to create PostScript files on the fly."""

    homepage = "https://pslib.sourceforge.net/"
    url = "https://sourceforge.net/projects/pslib/files/pslib/0.4.5/pslib-0.4.5.tar.gz"

    license("GPL-2.0-only")

    version("0.4.5", sha256="7a33928982b281660206bb3749a4a563e3ac987eea64f41696f212df345212be")

    depends_on("c", type="build")  # generated

    depends_on("jpeg")
    depends_on("libpng")
