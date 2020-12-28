# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuncsigs(PythonPackage):
    """Python function signatures from PEP362 for Python 2.6, 2.7 and 3.2."""

    homepage = "https://pypi.python.org/pypi/funcsigs"
    url      = "https://pypi.io/packages/source/f/funcsigs/funcsigs-1.0.2.tar.gz"

    version('1.0.2', sha256='a7bb0f2cf3a3fd1ab2732cb49eba4252c2af4240442415b4abce3b87022a8f50')
    version('0.4',   sha256='d83ce6df0b0ea6618700fe1db353526391a8a3ada1b7aba52fed7a61da772033')

    depends_on('py-setuptools@17.1:', type='build')
