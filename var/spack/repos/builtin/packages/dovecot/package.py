# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dovecot(AutotoolsPackage):
    """Dovecot mail server."""

    homepage = "https://www.dovecot.org/"
    url      = "https://dovecot.org/releases/2.3/dovecot-2.3.11.3.tar.gz"

    version('2.3.11.3', sha256='d3d9ea9010277f57eb5b9f4166a5d2ba539b172bd6d5a2b2529a6db524baafdc')

    depends_on('pkgconfig', type='build')
    depends_on('gettext',    type='build')
    depends_on('pandoc',     type='build', when='+pandoc')

    variant('pandoc', default=False, description="Build with pandoc")

    def setup_build_environment(self, env):
        if '+pandoc' in self.spec:
            env.prepend_path('PANDOC', 'True')
        else:
            env.prepend_path('PANDOC', 'False')
