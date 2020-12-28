# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiopython(PythonPackage):
    """A distributed collaborative effort to develop Python libraries and
       applications which address the needs of current and future work in
       bioinformatics.

    """
    homepage = "http://biopython.org/wiki/Main_Page"
    url      = "http://biopython.org/DIST/biopython-1.65.tar.gz"

    version('1.73', sha256='70c5cc27dc61c23d18bb33b6d38d70edc4b926033aea3b7434737c731c94a5e0')
    version('1.70', sha256='4a7c5298f03d1a45523f32bae1fffcff323ea9dce007fb1241af092f5ab2e45b')
    version('1.65', sha256='463cc81db84e9bfcdfb15629511c81ed556a6c0287e670dbfe80f03c65d2a88e')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
