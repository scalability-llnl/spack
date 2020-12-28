# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Paradiseo(CMakePackage):
    """A C++ white-box object-oriented framework dedicated to the reusable
       design of metaheuristics."""

    homepage = "http://paradiseo.gforge.inria.fr/"
    git      = "https://gforge.inria.fr/git/paradiseo/paradiseo.git"

    # Installing from the development version is a better option at this
    # point than using the very old supplied packages
    version('head')

    # This is a version that the package formula author has tested
    # successfully.  However, the clone is very large (~1Gb git
    # history). The history in the head version has been trimmed
    # significantly.
    version('dev-safe', commit='dbb8fbe9a786efd4d1c26408ac1883442e7643a6')

    variant('mpi',      default=True,
            description='Compile with parallel and distributed '
                        'metaheuristics module')
    variant('smp',      default=True,
            description='Compile with symmetric multi-processing module ')
    variant('edo',      default=True,
            description='Compile with (Experimental) EDO module')

    # variant('doc', default=False, description='Compile with documentation')
    variant('openmp',   default=False, description='Enable OpenMP support')
    variant('gnuplot',  default=False, description='Enable GnuPlot support')

    # Required dependencies
    depends_on("cmake@2.8:", type='build')

    # Optional dependencies
    depends_on("mpi", when="+mpi")
    depends_on("doxygen", when='+doc', type='build')
    depends_on("gnuplot", when='+gnuplot')
    depends_on("eigen", when='+edo', type='build')
    depends_on("boost~mpi", when='+edo~mpi')
    depends_on("boost+mpi", when='+edo+mpi')

    # Patches
    patch('enable_eoserial.patch')
    patch('fix_osx_detection.patch')
    patch('fix_tests.patch')
    patch('fix_tutorials.patch')

    def cmake_args(self):
        spec = self.spec

        return [
            '-DINSTALL_TYPE:STRING=MIN',
            '-DMPI:BOOL=%s' % ('TRUE' if '+mpi' in spec else 'FALSE'),
            # Note: This requires a C++11 compatible compiler
            '-DSMP:BOOL=%s' % ('TRUE' if '+smp' in spec else 'FALSE'),
            '-DEDO:BOOL=%s' % ('TRUE' if '+edo' in spec else 'FALSE'),
            '-DENABLE_CMAKE_TESTING:BOOL=%s' % (
                'TRUE' if self.run_tests else 'FALSE'),
            '-DENABLE_OPENMP:BOOL=%s' % (
                'TRUE' if '+openmp' in spec else 'FALSE'),
            '-DENABLE_GNUPLOT:BOOL=%s' % (
                'TRUE' if '+gnuplot' in spec else 'FALSE')
        ]
