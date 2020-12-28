# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJpeg(RPackage):
    """This package provides an easy and simple way to read, write and display
    bitmap images stored in the JPEG format. It can read and write both files
    and in-memory raw vectors."""

    homepage = "http://www.rforge.net/jpeg/"
    url      = "https://cloud.r-project.org/src/contrib/jpeg_0.1-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/jpeg"

    version('0.1-8', sha256='d032befeb3a414cefdbf70ba29a6c01541c54387cc0a1a98a4022d86cbe60a16')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on('jpeg')
