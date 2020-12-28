# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppcheck(MakefilePackage):
    """A tool for static C/C++ code analysis."""
    homepage = "http://cppcheck.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/cppcheck/cppcheck/1.78/cppcheck-1.78.tar.bz2"

    version('2.1', sha256='ab26eeef039e5b58aac01efb8cb664f2cc16bf9879c61bc93cd00c95be89a5f7')
    version('1.87', sha256='e3b0a46747822471df275417d4b74b56ecac88367433e7428f39288a32c581ca')
    version('1.81', sha256='bb694f37ae0b5fed48c6cdc2fb5e528daf32cefc64e16b1a520c5411323cf27e')
    version('1.78', sha256='e42696f7d6321b98cb479ad9728d051effe543b26aca8102428f60b9850786b1')
    version('1.72', sha256='9460b184ff2d8dd15344f3e2f42f634c86e4dd3303e1e9b3f13dc67536aab420')
    version('1.68', sha256='add6e5e12b05ca02b356cd0ec7420ae0dcafddeaef183b4dfbdef59c617349b1')

    variant('htmlreport', default=False, description="Install cppcheck-htmlreport")

    depends_on('py-pygments', when='+htmlreport', type='run')

    def build(self, spec, prefix):
        make('CFGDIR={0}'.format(prefix.cfg))

    def install(self, spec, prefix):
        # Manually install the final cppcheck binary
        mkdirp(prefix.bin)
        install('cppcheck', prefix.bin)
        install_tree('cfg', prefix.cfg)
        if spec.satisfies('+htmlreport'):
            install('htmlreport/cppcheck-htmlreport', prefix.bin)
