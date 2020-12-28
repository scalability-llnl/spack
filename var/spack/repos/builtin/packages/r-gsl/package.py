# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsl(RPackage):
    """An R wrapper for some of the functionality of the Gnu Scientific
    Library."""

    homepage = "https://github.com/RobinHankin/gsl.git"
    url      = "https://cloud.r-project.org/src/contrib/gsl_2.1-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gsl"

    version('2.1-6', sha256='f5d463239693f146617018987687db31b163653708cbae0b730b9b7bed81995c')

    depends_on('r@3.1.0:', type=('build', 'run'))

    depends_on('gsl@2.1:')
