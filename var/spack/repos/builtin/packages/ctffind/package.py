# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ctffind(AutotoolsPackage):
    """Fast and accurate defocus estimation from electron micrographs."""

    homepage = "http://grigoriefflab.janelia.org/ctffind4"
    url      = "http://grigoriefflab.janelia.org/sites/default/files/ctffind-4.1.8.tar.gz"

    version('4.1.8', sha256='bec43c0b8d32878c740d6284ef6d9d22718c80dc62270be18d1d44e8b84b2729')

    depends_on('wxwidgets')
    depends_on('fftw@3:')
