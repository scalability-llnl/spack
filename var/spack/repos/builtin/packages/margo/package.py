# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Margo(AutotoolsPackage):
    """Argobots bindings to the Mercury RPC API"""

    homepage = "https://xgitlab.cels.anl.gov/sds/margo"
    url      = "https://xgitlab.cels.anl.gov/sds/margo/-/archive/v0.4.3/margo-v0.4.3.tar.gz"
    git      = "https://xgitlab.cels.anl.gov/sds/margo.git"

    maintainers = ['fbudin69500', 'chuckatkins', 'carns']

    version('develop', branch='master')
    version('0.4.3', sha256='61a634d6983bee2ffa06e1e2da4c541cb8f56ddd9dd9f8e04e8044fb38657475')

    variant('shared', default=True,
            description='Build shared libraries instead of static libraries')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')
    depends_on('pkgconfig', type='build')

    depends_on('mercury')
    depends_on('argobots@1.0:')

    build_directory = 'spack-build'

    def configure_args(self):
        spec = self.spec
        args = []

        if '+shared' in spec:
            args.append('--enable-shared')
            args.append('--disable-static')
        else:
            args.append('--enable-static')
            args.append('--disable-shared')

        return args

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('./prepare.sh')
