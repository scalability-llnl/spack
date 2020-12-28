# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pixz(AutotoolsPackage):
    """Pixz (pronounced pixie) is a parallel, indexing version of xz. """

    homepage = "http://www.github.com/vasi/pixz"
    url      = "https://github.com/vasi/pixz/releases/download/v1.0.6/pixz-1.0.6.tar.xz"

    version('1.0.6', sha256='02c50746b134fa1b1aae41fcc314d7c6f1919b3d48bcdea01bf11769f83f72e8')

    depends_on('xz')
    depends_on('libarchive')
