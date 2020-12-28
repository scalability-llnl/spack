# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHwriter(RPackage):
    """Easy-to-use and versatile functions to
    output R objects in HTML format."""

    homepage = "https://cloud.r-project.org/package=hwriter"
    url      = "https://cloud.r-project.org/src/contrib/hwriter_1.3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/hwriter"

    version('1.3.2', sha256='6b3531d2e7a239be9d6e3a1aa3256b2745eb68aa0bdffd2076d36552d0d7322b')

    depends_on('r@2.6.0:', type=('build', 'run'))
