# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class SagaGis(AutotoolsPackage):
    """
    SAGA is a GIS for Automated Geoscientific Analyses and has been designed
    for an easy and effective implementation of spatial algorithms. It offers
    a comprehensive, growing set of geoscientific methods and provides an
    easily approachable user interface with many visualisation options
    """
    homepage    = "http://saga-gis.org/"
    url         = "https://sourceforge.net/projects/saga-gis/files/SAGA%20-%205/SAGA%20-%205.0.0/saga-5.0.0.tar.gz"
    git         = "git://git.code.sf.net/p/saga-gis/code"

    version('develop',  branch='master')
    version('7.0.0',    branch='release-7.0.0', preferred=True)
    version('6.4.0',    branch='release-6.4.0')
    version('6.3.0',    branch='release-6.3.0')
    version('6.2.0',    branch='release-6.2.0')
    version('6.1.0',    branch='release-6.1.0')
    version('6.0.0',    branch='release-6.0.0')
    version('5.0.1',    branch='release-5-0-1')
    version('5.0.0',    branch='release-5.0.0')
    version('4.1.0',    branch='release-4.1.0')
    version('4.0.0',    branch='release-4.0.0')
    version('4.0.0',    branch='release-4.0.0')
    version('3.0.0',    branch='release-3.0.0')
    version('2.3-lts',  branch='release-2-3-lts')
    version('2.3.1',    branch='release-2-3-1')
    version('2.3.0',    branch='release-2-3-0')

    variant('gui',      default=True,   description='Build GUI and interactive SAGA tools')
    variant('odbc',     default=True,   description='Build with ODBC support')
    variant('triangle', default=True,   description='Build with triangle.c non free for commercial use otherwise use qhull')
    variant('libfire',  default=True,   description='Build with libfire (non free for commercial usage)')
    variant('openmp',   default=True,   description='Build with OpenMP enabled')
    variant('python',   default=False,  description='Build Python extension')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # FIXME unnecessary dependency on python3 because of implicit python3
    # dependency through meson by a dependency of wx/gtkplus
    depends_on('python@3:')

    depends_on('wx')
    depends_on('gdal')
    depends_on('proj')

    depends_on('unixodbc', when='+odbc')
    depends_on('qhull', when='~triangle')
    depends_on('swig', type='build', when='+python')

    configure_directory = "saga-gis"

    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        args = []
        if self.spec.satisfies('@5:'):
            if '~gui' in self.spec:
                args.append('--disable-gui')

            if '~odbc' in self.spec:
                args.append('--disable-odbc')

            if '~triangle' in self.spec:
                args.append('--disable-triangle')

            if '~libfire' in self.spec:
                args.append('--disable-libfire')

            if '~openmp' in self.spec:
                args.append('--disable-openmp')

            if '+python' in self.spec:
                args.append('--enable-python')

        return args
