# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MountPointAttributes(AutotoolsPackage):
    """Library to turn expensive, non-scalable file system calls into simple
       string comparison operations."""

    homepage = "https://github.com/LLNL/MountPointAttributes"
    url = 'https://github.com/LLNL/MountPointAttributes/files/2270601/mountpointattr-1.1.tar.gz'
    git = "https://github.com/LLNL/MountPointAttributes.git"
    maintainers = ['lee218llnl']

    version('master', branch='master')
    version('1.1.1', sha256='397de583a99e60aae8b4485d3decac6e23f50c658a6353fea149d6dd50d3ecee', url="https://github.com/LLNL/MountPointAttributes/releases/download/v1.1.1/mountpointattr-1.1.1.tar.gz")
    version('1.1', sha256='bff84c75c47b74ea09b6cff949dd699b185ddba0463cb1ff39ab138003c96e02')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')

    patch('mpa_type_conversion.patch', when='@1.1')
