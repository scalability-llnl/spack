# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBcbioGff(PythonPackage):
    """Read and write Generic Feature Format (GFF) with Biopython
    integration."""

    homepage = "https://pypi.python.org/pypi/bcbio-gff/0.6.2"
    url      = "https://pypi.io/packages/source/b/bcbio-gff/bcbio-gff-0.6.2.tar.gz"

    version('0.6.2', sha256='c682dc46a90e9fdb124ab5723797a5f71b2e3534542ceff9f6572b64b9814e68')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
    depends_on('py-biopython',  type=('build', 'run'))
