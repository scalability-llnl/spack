# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRprojroot(RPackage):
    """Robust, reliable and flexible paths to files below a project root.
    The 'root' of a project is defined as a directory that matches a
    certain criterion, e.g., it contains a certain regular file."""

    homepage = "https://cloud.r-project.org/package=rprojroot"
    url      = "https://cloud.r-project.org/src/contrib/rprojroot_1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rprojroot"

    version('1.3-2', sha256='df5665834941d8b0e377a8810a04f98552201678300f168de5f58a587b73238b')
    version('1.2', sha256='28b4d235ce67314528a0c1cc7e98faed42437b42e07fca18a59a80fdc3eefeb9')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-backports', type=('build', 'run'))
