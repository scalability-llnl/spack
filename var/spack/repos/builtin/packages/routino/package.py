# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Routino(MakefilePackage):
    """Routino is an application for finding a route between two points using
    the dataset of topographical information collected by
    http://www.OpenStreetMap.org."""

    homepage = "https://www.routino.org"
    url      = "https://www.routino.org/download/routino-3.2.tgz"

    version('3.2', sha256='e2a431eaffbafab630835966d342e4ae25d5edb94c8ed419200e1ffb50bc7552')

    depends_on('zlib')
    depends_on('bzip2')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile.conf')
        makefile.filter('prefix=.*', 'prefix={0}'.format(prefix))
