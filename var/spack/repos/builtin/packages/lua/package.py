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
import os

class Lua(Package):
    """ The Lua programming language interpreter and library """
    homepage = "http://www.lua.org"
    url      = "http://www.lua.org/ftp/lua-5.1.5.tar.gz"

    version('5.3.2', '33278c2ab5ee3c1a875be8d55c1ca2a1')
    version('5.3.1', '797adacada8d85761c079390ff1d9961')
    version('5.3.0', 'a1b0a7e92d0c85bbff7a8d27bf29f8af')
    version('5.2.4', '913fdb32207046b273fdb17aad70be13')
    version('5.2.3', 'dc7f94ec6ff15c985d2d6ad0f1b35654')
    version('5.2.2', 'efbb645e897eae37cad4344ce8b0a614')
    version('5.2.1', 'ae08f641b45d737d12d30291a5e5f6e3')
    version('5.2.0', 'f1ea831f397214bae8a265995ab1a93e')
    version('5.1.5', '2e115fe26e435e33b0d5c022e4490567')
    version('5.1.4', 'd0870f2de55d59c1c8419f36e8fac150')
    version('5.1.3', 'a70a8dfaa150e047866dc01a46272599')

    depends_on('ncurses')
    depends_on('readline')

    def install(self, spec, prefix):
        if spec.satisfies("=darwin-i686") or spec.satisfies("=darwin-x86_64"):
            target = 'macosx'
        else:
            target = 'linux'
        make('INSTALL_TOP=%s' % prefix,
             'MYLDFLAGS=-L%s -lncurses' % spec['ncurses'].prefix.lib,
             target)
        make('INSTALL_TOP=%s' % prefix,
             'MYLDFLAGS=-L%s -lncurses' % spec['ncurses'].prefix.lib,
             'install')
