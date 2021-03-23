# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Aspcud(CMakePackage):
    """Aspcud: Package dependency solver

       Aspcud is a solver for package dependencies. A package universe
       and a request to install, remove, or upgrade packages have to
       be encoded in the CUDF format. Such a CUDF document can then be
       passed to aspcud along with an optimization criteria to obtain
       a solution to the given package problem."""

    homepage = "https://potassco.org/aspcud"
    url      = "https://github.com/potassco/aspcud/archive/v1.9.4.tar.gz"

    version('1.9.5', sha256='9cd3a9490d377163d87b16fa1a10cc7254bc2dbb9f60e846961ac8233f3835cf')
    version('1.9.4', sha256='3645f08b079e1cc80e24cd2d7ae5172a52476d84e3ec5e6a6c0034492a6ea885')

    depends_on('boost@1.74:', type=('build'), when='@1.9.5:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=('build'), when='@1.9.5:')
    depends_on('cmake', type=('build'))
    depends_on('re2c', type=('build'))
    depends_on('clingo')

    def cmake_args(self):
        spec = self.spec
        gringo_path = join_path(spec['clingo'].prefix.bin, 'gringo')
        clasp_path = join_path(spec['clingo'].prefix.bin, 'clasp')
        args = ['-DASPCUD_GRINGO_PATH={0}'.format(gringo_path),
                '-DASPCUD_CLASP_PATH={0}'.format(clasp_path)]
        return args
