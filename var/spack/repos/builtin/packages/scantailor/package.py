# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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

    homepage = "https://www.scantailor.org"
    url = "https://github.com/trufanov-nok/scantailor/archive/0.2.7.tar.gz"

    version(
        "0.2.7",
        sha256="3e27647621d43638888a268902f8fa098b06a70a5da5d0623b1c11220a367910",
    )

    depends_on("qt@5:")
    depends_on("libjpeg")
    depends_on("zlib")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("boost@1.35:")
    depends_on("libxrender")
