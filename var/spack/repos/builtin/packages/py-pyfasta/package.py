# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyfasta(PythonPackage):
    """Pyfasta: fast, memory-efficient, pythonic (and command-line)
       access to fasta sequence files"""

    homepage = "https://pypi.python.org/pypi/pyfasta/"
    url      = "https://pypi.io/packages/source/p/pyfasta/pyfasta-0.5.2.tar.gz"

    version('0.5.2', sha256='ab08d75fa90253bc91933d10567d5d9cca2718f4796ef3bdc36b68df0e45b258')

    depends_on('python@2.6:')
    depends_on('py-setuptools')
    depends_on('py-numpy')
