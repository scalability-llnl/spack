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


class EnvironmentModules(Package):
    """The Environment Modules package provides for the dynamic
    modification of a user's environment via modulefiles."""

    homepage = "https://sourceforge.net/p/modules/wiki/Home/"
    url      = "http://prdownloads.sourceforge.net/modules/modules-3.2.10.tar.gz"

    version('3.2.10', '8b097fdcb90c514d7540bb55a3cb90fb')

    # Dependencies:
    depends_on('tcl', type=alldeps)

    def install(self, spec, prefix):
        tcl_spec = spec['tcl']

        # See: https://sourceforge.net/p/modules/bugs/62/
        CPPFLAGS = ['-DUSE_INTERP_ERRORLINE']
        config_args = [
            "--without-tclx",
            "--with-tclx-ver=0.0",
            "--prefix=%s" % prefix,
            # It looks for tclConfig.sh
            "--with-tcl=%s" % join_path(tcl_spec.prefix, 'lib'),
            "--with-tcl-ver=%d.%d" % (tcl_spec.version.version[
                                      0], tcl_spec.version.version[1]),
            '--disable-debug',
            '--disable-dependency-tracking',
            '--disable-silent-rules',
            '--disable-versioning',
            '--datarootdir=%s' % prefix.share,
            'CPPFLAGS=%s' % ' '.join(CPPFLAGS)
        ]

        configure(*config_args)
        make()
        make('install')
