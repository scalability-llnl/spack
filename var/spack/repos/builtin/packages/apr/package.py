# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Apr(AutotoolsPackage):
    """Apache portable runtime."""

    homepage  = 'https://apr.apache.org/'
    url       = 'https://archive.apache.org/dist/apr/apr-1.7.0.tar.gz'

    version('1.7.0', sha256='48e9dbf45ae3fdc7b491259ffb6ccf7d63049ffacbc1c0977cced095e4c2d5a2')
    version('1.6.2', sha256='4fc24506c968c5faf57614f5d0aebe0e9d0b90afa47a883e1a1ca94f15f4a42e')
    version('1.5.2', sha256='1af06e1720a58851d90694a984af18355b65bb0d047be03ec7d659c746d6dbdb')

    patch('missing_includes.patch', when='@1.7.0')

    depends_on('libuuid', type='link')
