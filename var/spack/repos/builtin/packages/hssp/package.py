# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hssp(AutotoolsPackage):
    """The source code for building the mkhssp and hsspconv programs is bundled
       in the hssp project.

       The mkhssp executable creates stockholm files with hssp annotations in
       them. The hsspconv executable converts stockholm to the original hssp
       format.
    """

    homepage = "https://github.com/cmbi/hssp"
    url      = "https://github.com/cmbi/hssp/archive/3.0.10.tar.gz"

    version('3.0.10', sha256='b475d6fa62098df0e54c8dbdaa0b32de93bf5a393335f73f9b5a7e95f3090d2a')
    version('3.0.9',  sha256='42a9a93c48d22478212dcaf6ceb3feb64443e4cb2e8cccdd402b47a595d16658')
    version('3.0.8',  sha256='45e316ff2c700f09971027f9e813cf3139d36ab5951d337948fafab53e00d821')
    version('3.0.7',  sha256='eb6c3276eeb1261c55568ebfae301033904fe619d84b380313dbf137a2b06cd1')
    version('3.0.6',  sha256='b868e0077270361276c1c256e2f137ad95f7e84deeb61ae267f7559ebaab7d59')
    version('3.0.5',  sha256='fded09f08cfb12e578e4823295dc0d0aaeff6559d5e099df23c5bcc911597ccd')
    version('3.0.4',  sha256='fe786c3a75dafe93bb6a97c2840c3edb0d0e81446874082dc053e136dd3b7f68')
    version('3.0.3',  sha256='c4826ed74a74e3238f45104cb21ca4ad9e5b49498891e991a3a3a7a3b9bdbe1d')
    version('3.0.2',  sha256='edb43dc7407a5e91d68d27b732887c6e70a1988e8ddbba03d430713c40c40139')
    version('3.0.1',  sha256='8f56bc51d7b5f035442c189dd7096f0dd25528303722507365f5e746d5ad9a73')

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
