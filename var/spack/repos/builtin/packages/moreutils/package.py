# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Moreutils(MakefilePackage):
    """Additional Unix utilities. This is a growing collection of the Unix
    tools that nobody thought to write long ago, when Unix was young."""

    homepage = "https://joeyh.name/code/moreutils"
    url      = "https://deb.debian.org/debian/pool/main/m/moreutils/moreutils_0.63.orig.tar.xz"

    maintainers = ['matthiasdiener']

    version('0.63', sha256='01f0b331e07e62c70d58c2dabbb68f5c4ddae4ee6f2d8f070fd1e316108af72c')

    depends_on('perl', type='build')
    depends_on('docbook-xsl', type='build')
    depends_on('libxml2', type='build')

    def edit(self, spec, prefix):
        isutf8_makefile = FileFilter('is_utf8/Makefile')
        isutf8_makefile.filter('CC = .*', '')

        env['DOCBOOKXSL'] = spec['docbook-xsl'].prefix
        env['PREFIX'] = self.prefix
