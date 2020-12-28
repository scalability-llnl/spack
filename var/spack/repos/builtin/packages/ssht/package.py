# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ssht(Package):
    """ssht: Spin spherical harmonic transforms

    The SSHT code provides functionality to perform fast and exact
    spin spherical harmonic transforms based on the sampling theorem
    on the sphere derived in our paper: A novel sampling theorem on
    the sphere <http://dx.doi.org/10.1109/TSP.2011.2166394>.
    """

    homepage = "https://astro-informatics.github.io/ssht/"
    git      = "https://github.com/astro-informatics/ssht.git"

    maintainers = ['eschnett']

    version('1.2b1', commit='7378ce8853897cbd1b08adebf7ec088c1e40f860')

    depends_on('fftw')

    patch('float_conversion.patch')

    def install(self, spec, prefix):
        make('default', 'SSHTDIR=.')
        mkdirp(join_path(prefix, 'include', 'ssht'))
        install('src/c/ssht.h',
                join_path(prefix, 'include', 'ssht', 'ssht.h'))
        install('src/c/ssht_adjoint.h',
                join_path(prefix, 'include', 'ssht', 'ssht_adjoint.h'))
        install('src/c/ssht_core.h',
                join_path(prefix, 'include', 'ssht', 'ssht_core.h'))
        install('src/c/ssht_dl.h',
                join_path(prefix, 'include', 'ssht', 'ssht_dl.h'))
        install('src/c/ssht_error.h',
                join_path(prefix, 'include', 'ssht', 'ssht_error.h'))
        install('src/c/ssht_sampling.h',
                join_path(prefix, 'include', 'ssht', 'ssht_sampling.h'))
        install('src/c/ssht_types.h',
                join_path(prefix, 'include', 'ssht', 'ssht_types.h'))
        install_tree('doc/c', join_path(prefix, 'doc'))
        install_tree('lib/c', join_path(prefix, 'lib'))
