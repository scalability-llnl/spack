# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTiff(RPackage):
    """This package provides an easy and simple way to read, write and
       display bitmap images stored in the TIFF format. It can read and
       write both files and in-memory raw vectors."""

    homepage = "http://www.rforge.net/tiff/"
    url      = "https://cloud.r-project.org/src/contrib/tiff_0.1-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tiff"

    version('0.1-5', sha256='9514e6a9926fcddc29ce1dd12b1072ad8265900373f738de687ef4a1f9124e2b')

    depends_on('r@2.9.0:', type=('build', 'run'))
    depends_on("jpeg")
    depends_on("libtiff")
