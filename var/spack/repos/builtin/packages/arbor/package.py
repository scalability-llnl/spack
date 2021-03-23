# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arbor(CMakePackage, CudaPackage):
    """Arbor is a high-performance library for computational neuroscience
    simulations."""

    homepage = "https://github.com/arbor-sim/arbor/"
    git      = "https://github.com/arbor-sim/arbor.git"
    url      = "https://github.com/arbor-sim/arbor/releases/download/v0.5/arbor-v0.5-full.tar.gz"
    maintainers = ['bcumming', 'halfflat']

    version('master', branch='master', submodules=True)
    version('0.5', 'd0c8a4c7f97565d7c30493c66249be794d1dc424de266fc79cecbbf0e313df59')

    variant('assertions', default=False, description='Enable arb_assert() assertions in code.')
    variant('doc', default=False, description='Build documentation.')
    variant('mpi', default=False, description='Enable MPI support')
    variant('neuroml', default=True, description='Build NeuroML support library.')
    variant('python', default=True, description='Enable Python frontend support')
    variant('vectorize', default=False, description='Enable vectorization of computational kernels')

    # https://arbor.readthedocs.io/en/latest/install/build_install.html?highlight=requirements#compilers
    conflicts('%gcc@:8.3')
    conflicts('%clang@:8.0')
    # Cray compiler v9.2 and later is Clang-based.
    conflicts('%cce@:9.1')
    conflicts('%intel')

    depends_on('cmake@3.12:', type='build')

    # misc dependencies
    depends_on('nlohmann-json')
    depends_on('cuda@10:', when='+cuda')
    depends_on('libxml2', when='+neuroml')

    # mpi
    depends_on('mpi', when='+mpi')
    depends_on('py-mpi4py', when='+mpi+python', type=('build', 'run'))

    # python (bindings)
    extends('python', when='+python')
    depends_on('python@3.6:', when="+python", type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-pybind11', when='+python', type=('build', 'run'))

    # sphinx based documentation
    depends_on('python@3.6:', when="+doc", type='build')
    depends_on('py-sphinx', when="+doc", type='build')
    depends_on('py-svgwrite', when='+doc', type='build')

    @property
    def build_targets(self):
        return ['all', 'html'] if '+doc' in self.spec else ['all']

    def cmake_args(self):
        args = [
            self.define_from_variant('ARB_WITH_ASSERTIONS', 'assertions'),
            self.define_from_variant('ARB_WITH_MPI', 'mpi'),
            self.define_from_variant('ARB_WITH_NEUROML', 'neuroml'),
            self.define_from_variant('ARB_WITH_PYTHON', 'python'),
            self.define_from_variant('ARB_VECTORIZE', 'vectorize'),
        ]

        if '+cuda' in self.spec:
            args.append('-DARB_GPU=cuda')

        # rely on spack's compiler wrapper to set architecture
        args.append('-DARB_ARCH=')

        return args
