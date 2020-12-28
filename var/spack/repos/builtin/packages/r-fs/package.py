# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFs(RPackage):
    """A cross-platform interface to file system operations, built on top of
    the 'libuv' C library."""

    homepage = "http://fs.r-lib.org/"
    url      = "https://cloud.r-project.org/src/contrib/fs_1.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/fs"

    version('1.3.1', sha256='d6934dca8f835d8173e3fb9fd4d5e2740c8c04348dd2bcc57df1b711facb46bc')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('gmake', type='build')
