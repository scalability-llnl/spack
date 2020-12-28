# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
import sys

from spack.package import *


class Mvapich2Gdr(AutotoolsPackage):
    """MVAPICH2-GDR is an optimized version of the MVAPICH2 MPI library for
    GPU-enabled HPC and Deep Learning Applications. MVAPICH2-GDR is not
    installable from source and is only available through a binary mirror.
    If you do not find the binary you're looking for, send us an email at
    mvapich@cse.ohio-state.edu. The binary mirror url is:
    http://mvapich.cse.ohio-state.edu/download/mvapich/spack-mirror/mvapich2-gdr/
    """

    homepage = 'http://mvapich.cse.ohio-state.edu'
    url      = 'http://mvapich.cse.ohio-state.edu/download/mvapich/spack-mirror/mvapich2-gdr/mvapich2-gdr-2.3.4.tar.gz'

    maintainers = ['nithintsk', 'harisubramoni']

    version('2.3.4', sha256='ed78101e6bb807e979213006ee5f20ff466369b01f96b6d1cf0c471baf7e35aa')
    version('2.3.3', sha256='9b7b5dd235dbf85099fba3b6f1ccb49bb755923efed66ddc335921f44cb1b8a8')

    provides('mpi')
    provides('mpi@:3.1')

    variant(
        'process_managers',
        description='The process manager to activate.',
        default='mpirun',
        values=('slurm', 'mpirun', 'pbs', 'jsrun'),
        multi=False
    )

    variant(
        'distribution',
        description='The type of fabric distribution.',
        default='stock-ofed',
        values=('stock-ofed', 'mofed4.5', 'mofed4.6', 'mofed4.7', 'mofed5.0'),
        multi=False
    )

    variant(
        'pmi_version',
        description='The pmi version to be used with slurm. '
                    'Is ignored if set for mpirun or jsrun. '
                    'jsrun uses pmix regardless of chosen option.',
        default='pmi1',
        values=('pmi1', 'pmi2', 'pmix'),
        multi=False
    )

    variant(
        'mcast',
        description='Enable/Disable support for mcast',
        default=True
    )

    variant(
        'openacc',
        description='Enable/Disable support for openacc',
        default=False
    )

    variant(
        'core_direct',
        description='Enable/Disable support for core_direct',
        default=False
    )

    depends_on('bison@3.4.2', type='build')
    depends_on('libpciaccess@0.13.5', when=(sys.platform != 'darwin'))
    depends_on('libxml2@2.9.10')
    depends_on('cuda@9.2.88:10.2.89')
    depends_on('pmix@3.1.3', when='pmi_version=pmix')

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpifort', relative_root='bin'
    )

    @property
    def libs(self):
        query_parameters = self.spec.last_query.extra_parameters
        libraries = ['libmpi']

        if 'cxx' in query_parameters:
            libraries = ['libmpicxx'] + libraries

        return find_libraries(
            libraries, root=self.prefix, shared=True, recursive=True
        )

    @property
    def process_manager_options(self):
        spec = self.spec

        opts = []

        if '~mcast' in spec:
            opts.append('--disable-mcast')

        if '+core_direct' in spec:
            opts.append('--with-core-direct')

        if '+openacc' in spec:
            opts.append('--enable-openacc')

        # See: http://slurm.schedmd.com/mpi_guide.html#mvapich2
        if 'process_managers=slurm' in spec:
            opts.append('--with-pm=slurm')
            if 'pmi_version=pmi1' in spec:
                opts.append('--with-pmi=pmi1')
            if 'pmi_version=pmi2' in spec:
                opts.append('--with-pmi=pmi2')
            if 'pmi_version=pmix' in spec:
                opts.append('--with-pmi=pmix')
                opts.append('--with-pmix={0}'.format(spec['pmix'].prefix))

        elif 'process_managers=pbs' in spec:
            opts.append([
                '--with-pm=hydra',
                '--with-pbs=/opt/pbs'
            ])
            if '~mcast' in spec:
                opts.append('--disable-mcast')
            if '+core_direct' in spec:
                opts.append('--with-core-direct')
            if '+openacc' in spec:
                opts.append('--enable-openacc')

        elif 'process_managers=jsrun' in spec:
            opts.append([
                '--with-pmi=pmix',
                '--with-pmix={0}'.format(spec['pmix'].prefix),
                '--with-pm=jsm'
            ])

        return opts

    def setup_build_environment(self, env):
        # mvapich2 configure fails when F90 and F90FLAGS are set
        env.unset('F90')
        env.unset('F90FLAGS')

    def setup_run_environment(self, env):
        if 'pmi_version=pmi1' in self.spec:
            env.set('SLURM_MPI_TYPE', 'pmi1')
        if 'pmi_version=pmi2' in self.spec:
            env.set('SLURM_MPI_TYPE', 'pmi2')
        if 'pmi_version=pmix' in self.spec:
            env.set('SLURM_MPI_TYPE', 'pmix')

        # Because MPI functions as a compiler, we need to treat it as one and
        # add its compiler paths to the run environment.
        self.setup_compiler_environment(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_compiler_environment(env)

        # use the Spack compiler wrappers under MPI
        env.set('MPICH_CC', spack_cc)
        env.set('MPICH_CXX', spack_cxx)
        env.set('MPICH_F77', spack_f77)
        env.set('MPICH_F90', spack_fc)
        env.set('MPICH_FC', spack_fc)

    def setup_compiler_environment(self, env):
        env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        env.set('MPICXX', join_path(self.prefix.bin, 'mpicxx'))
        env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc  = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
        self.spec.mpifc  = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
        self.spec.mpicxx_shared_libs = [
            os.path.join(self.prefix.lib, 'libmpicxx.{0}'.format(dso_suffix)),
            os.path.join(self.prefix.lib, 'libmpi.{0}'.format(dso_suffix))
        ]

    def configure_args(self):
        args = ['--enable-cuda',
                '--disable-hybrid',
                '--with-ch3-rank-bits=32',
                '--disable-gl',
                '--without-hydra-ckpointlib',
                '--disable-static',
                '--enable-shared',
                '--disable-rdma-cm'
                ]
        args.extend(self.process_manager_options)
        return args
