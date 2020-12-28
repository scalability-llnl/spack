# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrad(PythonPackage):
    """RADseq for phylogenetics & introgression analyses"""

    homepage = "http://dereneaton.com/software/pyrad/"
    url      = "https://github.com/dereneaton/pyrad/archive/3.0.66.tar.gz"

    version('3.0.66', sha256='7dbd67e532058f7b7de76d14cf631fd3e3c841cd80fac4e55fbce8bb52ac6537')

    depends_on('python@:2.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('vsearch')
    depends_on('muscle')
