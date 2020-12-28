# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Harminv(AutotoolsPackage):
    """Harminv is a free program (and accompanying library) to solve the
    problem of harmonic inversion - given a discrete-time, finite-length
    signal that consists of a sum of finitely-many sinusoids (possibly
    exponentially decaying) in a given bandwidth, it determines the
    frequencies, decay constants, amplitudes, and phases of those sinusoids."""

    homepage = "http://ab-initio.mit.edu/wiki/index.php/Harminv"
    url      = "http://ab-initio.mit.edu/harminv/harminv-1.4.tar.gz"
    list_url = "http://ab-initio.mit.edu/harminv/old"

    version('1.4', sha256='e1b923c508a565f230aac04e3feea23b888b47d8e19b08816a97ee4444233670')

    depends_on('blas')
    depends_on('lapack')

    def configure_args(self):
        spec = self.spec

        return [
            '--enable-shared',
            '--with-blas={0}'.format(spec['blas'].prefix.lib),
            '--with-lapack={0}'.format(spec['lapack'].prefix.lib),
        ]
