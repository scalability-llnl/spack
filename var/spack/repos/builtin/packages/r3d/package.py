# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class R3d(MakefilePackage):
    """Fast, robust polyhedral intersections, analytic integration, and
    conservative voxelization."""

    homepage = "https://github.com/devonmpowell/r3d"
    git      = "https://github.com/devonmpowell/r3d.git"

    version('2019-04-24', commit='86cea79c124c6a8edd8c8cdea61e3e923acb0b22')
    version('2018-12-19', commit='47308f68c782ed3227d3dab1eff24d41f6421f21')
    version('2018-01-07', commit='d6799a582256a120ef3bd7e18959e96cba0e5495')

    variant("test",  default=False, description="Build R3D regression tests")

    def build(self, spec, prefix):

        make_args = [
            'CC={0}'.format(spack_cc),
        ]

        make('libr3d.a', *make_args)

        if '+test' in spec:
            with working_dir('tests'):
                make('all', *make_args)

    def install(self, spec, prefix):

        # R3D does not have an install target so create our own here.
        mkdirp(prefix.include)
        my_headers = find('.', '*.h', recursive=False)
        for my_header in my_headers:
            install(my_header, prefix.include)
        mkdirp(prefix.lib)
        install('libr3d.a', prefix.lib)

        if '+test' in spec:
            with working_dir('tests'):

                # R3D does not have an install target so create our own here.
                mkdirp(prefix.test)
                install('r2d_unit_tests', prefix.test)
                install('r3d_unit_tests', prefix.test)
                install('rNd_unit_tests', prefix.test)
