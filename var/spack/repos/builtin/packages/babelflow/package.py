# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Babelflow(CMakePackage):
    """BabelFlow is an Embedded Domain Specific Language to describe
       algorithms using a task graph abstraction which allows them to be
       executed on top of one of several available runtime systems."""

    homepage = "https://github.com/sci-visus/BabelFlow"
    git      = 'https://github.com/sci-visus/BabelFlow.git'

    maintainers = ['spetruzza']

    version('develop',
            branch='ascent',
            submodules=True)

    depends_on('mpi')

    variant("shared", default=True, description="Build Babelflow as shared libs")

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF')]
        return args
