# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMethylcode(PythonPackage):
    """MethylCoder is a single program that takes of bisulfite-treated
       reads and outputs per-base methylation data. """

    homepage = "https://github.com/brentp/methylcode"
    git      = "https://github.com/brentp/methylcode.git"

    version('master', branch='master')

    depends_on('python@2.6:2.8', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy')
    depends_on('py-pyfasta')
    depends_on('py-bsddb3')
    depends_on('bowtie')
