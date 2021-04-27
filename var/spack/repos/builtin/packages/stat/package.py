# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Stat(AutotoolsPackage):
    """Library to create, manipulate, and export graphs Graphlib."""

    homepage = "http://paradyn.org/STAT/STAT.html"
    url      = "https://github.com/LLNL/STAT/archive/v2.0.0.tar.gz"
    git      = "https://github.com/llnl/stat.git"
    maintainers = ['lee218llnl']

    version('develop', branch='develop')
    version('4.1.0', sha256='1d5b00afd563cf3bd9dd40818c44a03d7d4b13356216881513c058566c3b0080',
            url='https://github.com/LLNL/STAT/files/6193568/stat-4.1.0.tar.gz')
    version('4.0.2', sha256='9ece10dde8e1579c9db469ac8d2391b26e59498c0947dbb271c2d01d7ef0a65d',
            url='https://github.com/LLNL/STAT/releases/download/v4.0.2/stat-4.0.2.tar.gz')
    version('4.0.1', sha256='ae3fbd6946003fb16233d82d40285780a9a802da5fe30d09adb8a8b2a2cc4ad6',
            url='https://github.com/LLNL/STAT/files/2489327/stat-4.0.1.tar.gz')
    version('4.0.0', sha256='1c4f62686645f6dc1d9ef890acc9c2839c150789dc220718775878feb41bdabf',
            url='https://github.com/LLNL/STAT/releases/download/v4.0.0/stat-4.0.0.tar.gz')
    version('3.0.1', sha256='540916ffb92026ca7aa825a2320095a89b9b4fd3426ee7657b44ac710618947e',
            url='https://github.com/LLNL/STAT/files/911503/stat-3.0.1.zip',
            deprecated=True)
    version('3.0.0', sha256='b95cac82989e273e566f16ba17a75526374ee8e0ef066a411977e1935967df57',
            url='https://github.com/LLNL/STAT/releases/download/v3.0.0/STAT-3.0.0.tar.gz',
            deprecated=True)
    version('2.2.0', sha256='ed4732bfbe942ca8e29342f24f48e0c295989b0639a548febe7a1c1390ae1993',
            deprecated=True)
    version('2.1.0', sha256='497ed2bd1127cb2e97b32a30a4f62b6b298d18f3313c0278dd908c6ecba64f43',
            deprecated=True)
    version('2.0.0', sha256='b19587c2166b5d4d3a89a0ec5433ac61335aa7ad5cfa5a3b4406f5ea6c0bf0ac',
            deprecated=True)

    # TODO: dysect requires Dyninst patch for version 3.0.0b
    variant('dysect', default=False, description="enable DySectAPI")
    variant('examples', default=False, description="enable examples")
    variant('fgfs', default=True, description="enable file broadcasting")
    variant('gui', default=True, description="enable GUI")

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('dyninst', when='~dysect')
    depends_on('dyninst@:9.99', when='@:4.0.1')
    depends_on('dyninst@8.2.1+stat_dysect', when='+dysect')
    # we depend on fgfs@master to avoid seg faults with fgfs 1.1
    depends_on('fast-global-file-status@master', when='+fgfs')
    depends_on('graphlib@2.0.0', when='@2.0.0:2.2.0')
    depends_on('graphlib@3.0.0', when='@3:')
    depends_on('graphviz', type=('build', 'link', 'run'))
    # we depend on mpa@master for bug fixes since launchmon 1.0.2
    depends_on('launchmon@master')
    depends_on('mrnet')
    depends_on('python')
    depends_on('python@:2.8', when='@:4.0.0')
    depends_on('py-pygtk', type=('build', 'run'), when='@:4.0.0 +gui')
    depends_on('py-enum34', type=('run'), when='@:4.0.0')
    depends_on('py-xdot@1.0', when='@4.0.1: +gui')
    depends_on('swig')
    depends_on('mpi', when='+examples')
    depends_on('boost')

    patch('configure_mpicxx.patch', when='@2.1.0')

    # No Mac support due to dependencies like dyninst, elf etc.
    conflicts('platform=darwin', msg='macOS is not supported')

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-launchmon=%s"   % spec['launchmon'].prefix,
            "--with-mrnet=%s"       % spec['mrnet'].prefix,
            "--with-graphlib=%s"    % spec['graphlib'].prefix,
            "--with-stackwalker=%s" % spec['dyninst'].prefix,
            "--with-python=%s"      % spec['python'].command.path,
            "--with-boost=%s"       % spec['boost'].prefix,
        ]
        if '+fgfs' in spec:
            args.append('--with-fgfs=%s'
                        % spec['fast-global-file-status'].prefix)
        if '+dysect' in spec:
            args.append('--enable-dysectapi')
        if '~gui' in spec:
            args.append('--disable-gui')
        if '~examples' in spec:
            args.append('--disable-examples')
        return args
