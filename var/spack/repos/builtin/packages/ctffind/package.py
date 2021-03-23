# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ctffind(AutotoolsPackage):
    """Fast and accurate defocus estimation from electron micrographs."""

    homepage = "https://grigoriefflab.umassmed.edu/ctf_estimation_ctffind_ctftilt"
    url      = "https://grigoriefflab.umassmed.edu/system/tdf?path=ctffind-4.1.8.tar.gz&file=1&type=node&id=26"

    version('4.1.8', sha256='bec43c0b8d32878c740d6284ef6d9d22718c80dc62270be18d1d44e8b84b2729', extension='tar.gz')

    depends_on('wxwidgets')
    depends_on('fftw@3:')
