# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gpi2(AutotoolsPackage):
    """GPI-2 is an API for the development of scalable, asynchronous and fault
    tolerant parallel applications. It implements the GASPI specification
    (www.gaspi.de)"""

    homepage = "http://www.gpi-site.com"
    url      = "https://github.com/cc-hpc-itwm/GPI-2/archive/v1.4.0.tar.gz"
    git      = "https://github.com/cc-hpc-itwm/GPI-2.git"
    maintainers = ['robert-mijakovic']

    version('develop', branch='next')
    version('master', branch='master')
    version('1.4.0', sha256='3b8ffb45346b2fe56aaa7ba15a515e62f9dff45a28e6a014248e20094bbe50a1')

    variant('mpi', default=False, description='Enable MPI support')
    variant('fortran', default=True, description='Enable Fortran modules')
    variant(
        'fabrics',
        values=disjoint_sets(
            ('auto',), ('verbs',), ('ethernet',),
        ).with_non_feature_values('auto', 'none'),
        description="List of fabrics that are enabled; "
        "'auto' lets gpi-2 determine",
    )

    variant(
        'schedulers',
        values=disjoint_sets(
            ('auto',), ('loadleveler',), ('pbs',), ('slurm',)
        ).with_non_feature_values('auto', 'none'),
        description="List of schedulers for which support is enabled; "
        "'auto' lets gpi-2 determine",
    )

    depends_on('autoconf', type='build')  # autogen.sh - autoreconf
    depends_on('automake', type='build')  # autogen.sh - automake
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('mpi', when='+mpi')

    depends_on('rdma-core', when='fabrics=verbs')

    depends_on('slurm', when='schedulers=slurm')

    def with_or_without_verbs(self, activated):
        opt = 'infiniband'
        # If the option has not been activated return
        # --without-infiniband
        if not activated:
            return '--without-{0}'.format(opt)
        return '--with-{0}={1}'.format(opt, self.spec['rdma-core'].prefix)

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        spec = self.spec
        config_args = []
        config_args.extend(self.with_or_without('mpi'))
        config_args.extend(self.with_or_without('fortran'))

        # Fabrics
        if 'fabrics=auto' not in spec:
            config_args.extend(self.with_or_without('fabrics'))
        # Schedulers
        if 'schedulers=auto' not in spec:
            config_args.extend(self.with_or_without('schedulers'))

        return config_args
