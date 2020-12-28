# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRappdirs(RPackage):
    """An easy way to determine which directories on the users computer
    you should use to save data, caches and logs. A port of Python's
    'Appdirs' to R."""

    homepage = "https://cloud.r-project.org/package=rappdirs"
    url      = "https://cloud.r-project.org/src/contrib/rappdirs_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rappdirs"

    version('0.3.1', sha256='2fd891ec16d28862f65bb57e4a78f77a597930abb59380e757afd8b6c6d3264a')

    depends_on('r@2.14:', type=('build', 'run'))
