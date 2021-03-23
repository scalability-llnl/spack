# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Flecsph(CMakePackage):
    """FleCSPH is a multi-physics compact application that exercises FleCSI
    parallel data structures for tree-based particle methods. In particular,
    FleCSPH implements a smoothed-particle hydrodynamics (SPH) solver for
    the solution of Lagrangian problems in astrophysics and cosmology. FleCSPH
    includes support for gravitational forces using the fast multipole method
    (FMM)."""

    homepage = "http://flecsi.lanl.com"
    git      = "https://github.com/laristra/flecsph.git"

    version('master', branch='master', submodules=True, preferred=True)

    variant('test', default=True, description='Adding tests')

    depends_on('cmake@3.15:', type='build')
    depends_on('boost@1.70.0: cxxstd=14 +program_options')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('mpi')
    depends_on('hdf5+hl@1.8:')
    depends_on('flecsi@1 +cinch backend=mpi')
    depends_on('gsl')
    depends_on('googletest', when='+test')
    depends_on("pkgconfig", type='build')

    def setup_run_environment(self, env):
        env.set('HDF5_ROOT', self.spec['hdf5'].prefix)

    def cmake_args(self):
        options = ['-DCMAKE_BUILD_TYPE=debug']
        options.append('-DENABLE_UNIT_TESTS=ON')
        options.append('-DENABLE_DEBUG=OFF')
        options.append('-DLOG_STRIP_LEVEL=1')
        options.append('-DENABLE_UNIT_TESTS=ON')
        options.append('-DENABLE_DEBUG_TREE=OFF')
        # add option to build the tests
        return options
