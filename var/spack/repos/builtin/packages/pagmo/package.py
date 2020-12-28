# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pagmo(CMakePackage):
    """Parallel Global Multiobjective Optimizer (and its Python alter ego
    PyGMO) is a C++ / Python platform to perform parallel computations of
    optimisation tasks (global and local) via the asynchronous generalized
    island model."""

    # Multiple homepages:
    # C++    interface: https://esa.github.io/pagmo/
    # Python interface: https://esa.github.io/pygmo/

    homepage = "https://esa.github.io/pagmo/"
    url      = "https://github.com/esa/pagmo/archive/1.1.7.tar.gz"

    version('1.1.7', sha256='6d8fab89ef9d5d5f30f148225bf9b84b2e5a38997f3d68b85547840e9fd95172')

    variant('examples', default=False, description='Build examples')
    variant('cxx',      default=True,  description='Build the C++ interface')
    variant('python',   default=True,  description='Build Python bindings')
    variant('gsl',      default=True,  description='Enable support for GSL minimisers')
    variant('gtop',     default=False, description='Build GTOP database problems')
    variant('ipopt',    default=False, description='Enable support for IPOPT minimiser')
    variant('mpi',      default=True,  description='Enable support for MPI')
    variant('nlopt',    default=False, description='Enable support for NLopt minimisers')
    variant('snopt',    default=False, description='Enable support for SNOPT minimiser')
    variant('worhp',    default=False, description='Enable support for WORHP minimiser')
    variant('headers',  default=True,  description='Installs the header files')
    variant('blas',     default=True,  description='Enable support for BLAS')
    variant('scipy',    default=True,  description='Enable support for scipy')
    variant('networkx', default=False, description='Enable support for networkx')
    variant('vpython',  default=False, description='Enable support for vpython')
    variant('pykep',    default=False, description='Enable support for pykep')

    extends('python', when='+python')

    # Concretization in Spack is currently broken
    # depends_on('boost+system+serialization+thread')
    # depends_on('boost+python',    when='+python')
    # depends_on('boost+date_time', when='+gtop')

    # Workaround for now
    depends_on('boost+system+serialization+thread',                  when='~python~gtop')
    depends_on('boost+system+serialization+thread+python',           when='+python~gtop')
    depends_on('boost+system+serialization+thread+date_time',        when='~python+gtop')
    depends_on('boost+system+serialization+thread+python+date_time', when='+python+gtop')

    depends_on('gsl@1.15:',       when='+gsl')
    depends_on('ipopt',           when='+ipopt')
    depends_on('mpi@1.2:',        when='+mpi')
    depends_on('blas',            when='+blas')
    depends_on('py-scipy',    type=('build', 'run'), when='+scipy')
    depends_on('py-networkx', type=('build', 'run'), when='+networkx')

    # TODO: Add packages for missing dependencies
    # depends_on('nlopt+cxx', when='+nlopt')
    # depends_on('snopt',     when='+snopt')
    # depends_on('py-vpython',     type=('build', 'run'), when='+vpython')
    # depends_on('py-pykep@1.15:', type=('build', 'run'), when='+gtop')
    # depends_on('py-pykep@1.15:', type=('build', 'run'), when='+pykep')

    depends_on('cmake@2.8:', type='build')

    def variant_to_bool(self, variant):
        return 'ON' if variant in self.spec else 'OFF'

    def cmake_args(self):
        spec = self.spec

        args = [
            '-DBUILD_EXAMPLES={0}'.format(self.variant_to_bool('+examples')),
            '-DBUILD_MAIN={0}'.format(self.variant_to_bool('+cxx')),
            '-DBUILD_PYGMO={0}'.format(self.variant_to_bool('+python')),
            '-DENABLE_GSL={0}'.format(self.variant_to_bool('+gsl')),
            '-DENABLE_GTOP_DATABASE={0}'.format(self.variant_to_bool('+gtop')),
            '-DENABLE_IPOPT={0}'.format(self.variant_to_bool('+ipopt')),
            '-DENABLE_MPI={0}'.format(self.variant_to_bool('+mpi')),
            '-DENABLE_NLOPT={0}'.format(self.variant_to_bool('+nlopt')),
            '-DENABLE_SNOPT={0}'.format(self.variant_to_bool('+snopt')),
            '-DENABLE_WORHP={0}'.format(self.variant_to_bool('+worhp')),
            '-DINSTALL_HEADERS={0}'.format(self.variant_to_bool('+headers')),
            '-DENABLE_TESTS={0}'.format('ON' if self.run_tests else 'OFF'),
        ]

        if '+python' in spec:
            args.extend([
                # By default picks up the system python not the Spack build
                '-DPYTHON_EXECUTABLE={0}'.format(spec['python'].command.path),
                # By default installs to the python prefix not the pagmo prefix
                '-DPYTHON_MODULES_DIR={0}'.format(site_packages_dir),
            ])

        return args
