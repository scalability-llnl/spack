# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dssp(AutotoolsPackage):
    """'mkdssp' utility. (dictionary of protein secondary structure)"""

    homepage = "https://github.com/cmbi/dssp"
    url      = "https://github.com/cmbi/dssp/archive/3.1.4.tar.gz"

    version('3.1.4', sha256='496282b4b5defc55d111190ab9f1b615a9574a2f090e7cf5444521c747b272d4')
    version('2.3.0', sha256='4c95976d86dc64949cb0807fbd58c7bee5393df0001999405863dc90f05846c6')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('boost@1.48:')

    def configure_args(self):
        args = [
            "--with-boost=%s" % self.spec['boost'].prefix]
        return args

    @run_after('configure')
    def edit(self):
        makefile = FileFilter(join_path(self.stage.source_path, 'Makefile'))
        makefile.filter('.*-Werror .*', '                    -Wno-error \\')
