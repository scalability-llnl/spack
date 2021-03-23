# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Poke(AutotoolsPackage, GNUMirrorPackage):
    """"The extensible editor for structured binary data"""
    homepage = "http://www.jemarch.net/poke.html"
    gnu_mirror_path = 'poke/poke-1.0.tar.gz'

    maintainers = ['ChristianTackeGSI']

    version('1.0', sha256='de930b8700c0772b3c2cd0d0ca35f50fd3d77bdf82c6251eb516b49e8ca25b0a')

    depends_on('pkgconf')
    depends_on('readline')
    depends_on('bdw-gc')
    depends_on('json-c')

    build_directory = 'spack-build'
