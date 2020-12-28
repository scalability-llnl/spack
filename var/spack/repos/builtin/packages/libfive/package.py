# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfive(CMakePackage):
    """libfive is a software library and set of tools for solid modeling."""

    homepage = "https://libfive.com"
    git      = "https://github.com/libfive/libfive.git"

    # https://libfive.com/download/ recommends working from the master branch
    version('master', branch='master')

    depends_on('pkgconfig', type='build')
    depends_on('cmake@3.3:', type='build')
    depends_on('boost@1.65:')
    depends_on('eigen@3.3.0:')
    depends_on('libpng')
    depends_on('qt@5.7:')
    depends_on('guile@2.2.1:')
