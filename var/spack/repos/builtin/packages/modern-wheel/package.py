# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost
import sys


class ModernWheel(CMakePackage):
    """C++ utility collection. Provides various facilities of common use in
    modern codebases like dynamic linking helpers, loadable plugins facilities
    and misc patterns."""

    homepage = "https://github.com/alalazo/modern_wheel"
    url      = "https://github.com/alalazo/modern_wheel/archive/1.2.tar.gz"
    maintainers = ['alalazo']

    version('1.2', sha256='48612f698d7159f0eb10d93ddc3e2682b06a54d3a836ff227636be3261aed15e')
    version('1.1', sha256='d8ba4891257b96108e9b9406a556f8ced3b71ce85c3fcdca6bfd9cc37bf010a3')
    version('1.0', sha256='b90a1e29af0b67dfa4c07f9c19b2d04fa78cd878b29a9c42bc766dabd6cb1b90')

    variant('shared', default=True,
            description='Enables the build of shared libraries')
    # Test implementation files cause some issues on darwin,
    # needs to be investigated.
    variant('test',   default=sys.platform != 'darwin',
            description='Enables the build of unit tests')

    # FindBoost shipped with CMake up to version 3.10.2 (latest one
    # up to now) is known to be unable to detect Boost >= 1.66.0.
    # This issue will be probably fixed in CMake >= 3.11.0:
    # https://gitlab.kitware.com/cmake/cmake/issues/17575
    # Until then, just assume that we cannot correctly configure
    # ModernWheel with Boost >= 1.66.0.
    depends_on('boost           +system +filesystem', when='@:1.1.999')
    depends_on('boost@:1.65.999 +system +filesystem', when='@1.2:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # add virtual destructor to BaseMultiParms class.
    patch('add_virtual_destructor.patch')

    def cmake_args(self):
        spec = self.spec
        return [
            '-DBUILD_UNIT_TEST:BOOL={0}'.format(
                'ON' if '+test' in spec else 'OFF'),
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
        ]
