##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import sys
import subprocess


class NodeJs(Package):
    """Node.js is a JavaScript runtime built on Chrome's V8 JavaScript
    engine."""

    homepage = "https://nodejs.org/"
    url      = "https://nodejs.org/dist/v6.3.0/node-v6.3.0.tar.gz"

    version('7.3.0', '16f516a8433cd1d87ea8898b090432e7')
    version('6.9.3', '5054239f6357c7650beb6e591f205741')

    # variant('bash-completion', default=False, description='Build with bash-completion support for npm')  # NOQA: ignore=E501
    variant('debug',           default=False, description='Include debugger support')
    variant('doc',             default=False, description='Compile with documentation')
    variant('icu4c',           default=False, description='Build with support for all locales instead of just English')
    variant('openssl',         default=True,  description='Build with Spacks OpenSSL instead of the bundled version')
    variant('zlib',            default=True,  description='Build with Spacks zlib instead of the bundled version')

    # depends_on('libtool',         type='build') # if sys.platform != 'darwin'
    depends_on('pkg-config',      type='build')
    depends_on('python@2.7:',     type='build')
    # depends_on('bash-completion', when="+bash-completion")
    depends_on('icu4c',           when='+icu4c')
    depends_on('openssl',         when='+openssl')

    def url_for_version(self, version):
        _url_str = 'https://nodejs.org/dist/v{version}/node-v{version}.tar.gz'
        return _url_str.format(version=version)

    def install(self, spec, prefix):
        options = []
        options.extend(['--prefix={0}'.format(prefix)])

        # Note: npm is updated more regularly than node.js, so we build the
        #       package instead of using the bundled version
        options.extend(['--without-npm'])

        # On OSX, the system libtool must be used
        # So, we ensure that this is the case by...
        if sys.platform == 'darwin':
            result_which = subprocess.check_output(["which", "libtool"])
            result_whereis = subprocess.check_output(["whereis", "libtool"])
            assert result_which == result_whereis, (
                'On OSX the system libtool must be used. Please'
                '(temporarily) remove \n %s or its link to libtool from'
                'path')

        # TODO: Add bash-completion

        if '+debug' in spec:
            options.extend(['--debug'])

        if '+openssl' in spec:
            options.extend([
                '--shared-openssl',
                '--shared-openssl-includes=%s' % spec['openssl'].prefix.include,  # NOQA: ignore=E501
                '--shared-openssl-libpath=%s' % spec['openssl'].prefix.lib,
            ])

        if '+zlib' in spec:
            options.extend([
                '--shared-zlib',
                '--shared-zlib-includes=%s' % spec['zlib'].prefix.include,
                '--shared-zlib-libpath=%s' % spec['zlib'].prefix.lib,
            ])

        if '+icu4c' in spec:
            options.extend(['--with-intl=full-icu'])
        # else:
        #     options.extend(['--with-intl=system-icu'])

        configure(*options)

        if self.run_tests:
            make('test')
            make('test-addons')

        if '+doc' in spec:
            make('doc')

        make('install')
