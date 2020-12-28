# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xqilla(AutotoolsPackage, SourceforgePackage):
    """XQilla is an XQuery and XPath 2 library and command line utility
    written in C++, implemented on top of the Xerces-C library."""

    homepage = "http://xqilla.sourceforge.net/HomePage"
    sourceforge_mirror_path = "xqilla/XQilla-2.3.3.tar.gz"

    version('2.3.3', sha256='8f76b9b4f966f315acc2a8e104e426d8a76ba4ea3441b0ecfdd1e39195674fd6')

    variant('debug', default=False, description='Build a debugging version.')
    variant('shared', default=True, description='Build shared libraries.')

    depends_on('xerces-c')

    def configure_args(self):
        args = ['--with-xerces={0}'.format(self.spec['xerces-c'].prefix)]

        if '+shared' in self.spec:
            args.extend(['--enable-shared=yes',
                         '--enable-static=no'])
        else:
            args.extend(['--enable-shared=no',
                         '--enable-static=yes',
                         '--with-pic'])

        if '+debug' in self.spec:
            args.append('--enable-debug')

        return args
