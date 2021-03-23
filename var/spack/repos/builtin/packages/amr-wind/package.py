# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import itertools


def process_amrex_constraints():
    """Map constraints when building with external AMReX"""
    a1 = ['+', '~']
    a2 = ['mpi', 'hypre', 'cuda']
    a3 = [[x + y for x in a1] for y in a2]
    for k in itertools.product(*a3):
        if '+cuda' in k:
            for arch in CudaPackage.cuda_arch_values:
                yield ''.join(k) + " cuda_arch=%s" % arch
        else:
            yield ''.join(k)


class AmrWind(CMakePackage, CudaPackage):
    """AMR-Wind is a massively parallel, block-structured adaptive-mesh,
    incompressible flow sover for wind turbine and wind farm simulations. """

    homepage = "https://github.com/Exawind/amr-wind"
    git      = "https://github.com/exawind/amr-wind.git"

    maintainers = ['sayerhs', 'jrood-nrel', 'michaeljbrazell']

    tags = ['ecp', 'ecp-apps']

    version('main', branch='main', submodules=True)

    variant('shared', default=True,
            description='Build shared libraries')
    variant('unit', default=True,
            description='Build unit tests')
    variant('tests', default=True,
            description='Activate regression tests')
    variant('mpi', default=True,
            description='Enable MPI support')
    variant('openmp', default=False,
            description='Enable OpenMP for CPU builds')
    variant('netcdf', default=True,
            description='Enable NetCDF support')
    variant('hypre', default=True,
            description='Enable Hypre integration')
    variant('masa', default=False,
            description='Enable MASA integration')
    variant('openfast', default=False,
            description='Enable OpenFAST integration')
    variant('internal-amrex', default=True,
            description='Use AMRex submodule to build')
    variant('fortran', default=False,
            description='Build fortran interfaces')

    conflicts('+openmp', when='+cuda')

    depends_on('mpi', when='+mpi')

    for opt in process_amrex_constraints():
        dopt = '+particles' + opt
        if '+hypre' in dopt:
            dopt = "+fortran" + dopt
        depends_on('amrex@develop' + dopt, when='~internal-amrex' + opt)

    depends_on('hypre+mpi+int64~cuda@2.20.0:', when='+mpi~cuda+hypre')
    depends_on('hypre~mpi+int64~cuda@2.20.0:', when='~mpi~cuda+hypre')
    for arch in CudaPackage.cuda_arch_values:
        depends_on('hypre+mpi~int64+cuda cuda_arch=%s @2.20.0:' % arch,
                   when='+mpi+cuda+hypre cuda_arch=%s' % arch)
        depends_on('hypre~mpi~int64+cuda cuda_arch=%s @2.20.0:' % arch,
                   when='~mpi+cuda+hypre cuda_arch=%s' % arch)
    depends_on('netcdf-c', when='+netcdf')
    depends_on('masa', when='+masa')
    depends_on('openfast+cxx', when='+openfast')

    def cmake_args(self):
        define = CMakePackage.define

        vs = ["mpi", "cuda", "openmp", "netcdf", "hypre", "masa",
              "openfast", "tests", "fortran"]
        args = [
            self.define_from_variant("AMR_WIND_ENABLE_%s" % v.upper(), v)
            for v in vs
        ]

        args += [
            define('CMAKE_EXPORT_COMPILE_COMMANDS', True),
            define('AMR_WIND_ENABLE_ALL_WARNINGS', True),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define_from_variant('AMR_WIND_TEST_WITH_FCOMPARE', 'tests'),
        ]

        if '+cuda' in self.spec:
            amrex_arch = ['{0:.1f}'.format(float(i) / 10.0)
                          for i in self.spec.variants['cuda_arch'].value]
            if amrex_arch:
                args.append(define('AMReX_CUDA_ARCH', amrex_arch))

        if '+internal-amrex' in self.spec:
            args.append(self.define('AMR_WIND_USE_INTERNAL_AMREX', True))
        else:
            args += [
                self.define('AMR_WIND_USE_INTERNAL_AMREX', False),
                self.define('AMReX_ROOT', self.spec['amrex'].prefix)
            ]

        return args
