# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parallelmergetree(CMakePackage):
    """A multi-runtime implementation of a distributed merge tree
    segmentation algorithm. The implementation relies on the framework
    BabelFlow, which allows to execute the algorithm on different runtime
    systems."""

    homepage = "https://bitbucket.org/cedmav/parallelmergetree"
    git      = "https://bitbucket.org/cedmav/parallelmergetree.git"

    maintainers = ['spetruzza']

    version('develop',
            commit='6774ed74fd13b9747ac792978a676ce6e8b05cab',
            submodules=True)

    depends_on('babelflow@develop')

    variant("shared", default=True, description="Build ParallelMergeTree as shared libs")

    def cmake_args(self):
        args = [
            '-DBUILD_SHARED_LIBS:BOOL={0}'.format(
                'ON' if '+shared' in spec else 'OFF'),
            '-DLIBRARY_ONLY=ON'
        ]
        return args
