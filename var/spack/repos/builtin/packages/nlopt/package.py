# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Nlopt(CMakePackage):
    """NLopt is a free/open-source library for nonlinear optimization,
    providing a common interface for a number of different free optimization
    routines available online as well as original implementations of various
    other algorithms."""

    homepage = "https://nlopt.readthedocs.io"
    url      = "https://github.com/stevengj/nlopt/archive/v2.5.0.tar.gz"
    git      = "https://github.com/stevengj/nlopt.git"

    version('master', branch='master')
    version('2.6.1', sha256='66d63a505187fb6f98642703bd0ef006fedcae2f9a6d1efa4f362ea919a02650')
    version('2.5.0', sha256='c6dd7a5701fff8ad5ebb45a3dc8e757e61d52658de3918e38bab233e7fd3b4ae')

    variant('shared', default=True, description='Enables the build of shared libraries')
    variant('python', default=True, description='Build python wrappers')
    variant('guile',  default=False, description='Enable Guile support')
    variant('octave', default=False, description='Enable GNU Octave support')
    variant('cxx',    default=False,  description='Build the C++ routines')

    # Note: matlab is licenced - spack does not download automatically
    variant("matlab", default=False, description="Build the Matlab bindings.")

    depends_on('cmake@3.0:', type='build', when='@master')
    depends_on('python', when='+python', type=('build', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('swig', when='+python')
    depends_on('guile', when='+guile')
    depends_on('octave', when='+octave')
    depends_on('matlab', when='+matlab')
    extends('python', when='+python')

    def cmake_args(self):
        # Add arguments other than
        # CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        spec = self.spec
        args = []

        # Specify on command line to alter defaults:
        # eg: spack install nlopt@master +guile -octave +cxx

        # Spack should locate python by default - but to point to a build
        if '+python' in spec:
            args.append("-DPYTHON_EXECUTABLE=%s" % spec['python'].command.path)

        # On is default
        if '-shared' in spec:
            args.append('-DBUILD_SHARED_LIBS:Bool=OFF')

        # On is default
        if '-octave' in spec:
            args.append('-DNLOPT_OCTAVE:Bool=OFF')

        if '+cxx' in spec:
            args.append('-DNLOPT_CXX:BOOL=ON')

        if '+matlab' in spec:
            args.append("-DMatlab_ROOT_DIR=%s" % spec['matlab'].command.path)

        return args
