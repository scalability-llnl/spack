# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Parallelmergetree(CMakePackage):
    """A multi-runtime implementation of a distributed merge tree
    segmentation algorithm. The implementation relies on the framework
    BabelFlow, which allows to execute the algorithm on different runtime
    systems."""

    homepage = "https://bitbucket.org/cedmav/parallelmergetree"
    git      = "https://bitbucket.org/cedmav/parallelmergetree.git"

    maintainers = ['spetruzza']

    version('1.0.2',
            git='https://bitbucket.org/cedmav/parallelmergetree.git',
            tag='v1.0.2',
            submodules=True)

    version('1.0.0',
            git='https://bitbucket.org/cedmav/parallelmergetree.git',
            tag='v1.0.0',
            submodules=True)

    depends_on('babelflow')

    variant("shared", default=True, description="Build ParallelMergeTree as shared libs")

    def cmake_args(self):
        args = []

        if "+shared" in self.spec:
            args.append('-DBUILD_SHARED_LIBS=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS=OFF')

        args.append('-DLIBRARY_ONLY=ON')
        args.append('-DBabelFlow_DIR={0}'.format(
                    self.spec['babelflow'].prefix))

        return args
