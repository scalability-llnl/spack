# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlabaster(PythonPackage):
    """Alabaster is a visually (c)lean, responsive, configurable theme
    for the Sphinx documentation system."""

    homepage = "https://alabaster.readthedocs.io/"
    url      = "https://pypi.io/packages/source/a/alabaster/alabaster-0.7.10.tar.gz"

    version('0.7.12', sha256='a661d72d58e6ea8a57f7a86e37d86716863ee5e92788398526d58b26a4e4dc02')
    version('0.7.10', sha256='37cdcb9e9954ed60912ebc1ca12a9d12178c26637abdf124e3cde2341c257fe0')
    version('0.7.9',  sha256='47afd43b08a4ecaa45e3496e139a193ce364571e7e10c6a87ca1a4c57eb7ea08')

    depends_on('py-setuptools', type='build')
