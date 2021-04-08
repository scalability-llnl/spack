# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scantailor(CMakePackage):
    """Scan Tailor is an interactive post-processing tool for scanned pages. It
    performs operations such as page splitting, deskewing, adding/removing
    borders, and others. You give it raw scans, and you get pages ready to be
    printed or assembled into a PDF or DJVU file. Scanning, optical character
    recognition, and assembling multi-page documents are out of scope of this
    project."""

    homepage = "http://www.scantailor.org"
    url = "https://github.com/trufanov-nok/scantailor/archive/0.2.7.tar.gz"

    version(
        "0.2.7",
        sha256="0262079c15a0068412edfb7d6c2ed03159dc71eada4e31e48ac500f924254eca",
    )

    depends_on("qt@5.14.2")
    depends_on("libjpeg")
    depends_on("zlib")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("boost@1.35:")
    depends_on("libxrender")
