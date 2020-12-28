# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Icarus(AutotoolsPackage):
    """Icarus Verilog is a Verilog simulation and synthesis tool."""

    homepage = "http://www.iverilog.icarus.com"

    version('v10_3', git='https://github.com/steveicarus/iverilog.git',
            commit='453c5465895eaca4a792d18b75e9ec14db6ea50e')

    depends_on('autoconf', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('gperf @3.0:', type='build')
    depends_on('readline @4.2:', type=('build', 'link'))
    depends_on('zlib', type=('build', 'link'))

    patch('fix-gcc-10.patch', when='@v10_3')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autoconf.sh')

    @run_before('install')
    def create_install_folders(self):
        mkdirp(prefix.bin)
        mkdirp(join_path(prefix.include, 'iverilog'))
        mkdirp(join_path(prefix.lib, 'ivl'))
        mkdirp(join_path(prefix.lib, 'ivl', 'include'))
        mkdirp(join_path(prefix.share, 'man'))
        mkdirp(join_path(prefix.share, 'man', 'man1'))
