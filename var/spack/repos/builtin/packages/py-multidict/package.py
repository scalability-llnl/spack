# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyMultidict(PythonPackage):
    """Multidict is dict-like collection of key-value pairs where key
    might be occurred more than once in the container."""

    homepage = "https://github.com/aio-libs/multidict"
    url      = "https://github.com/aio-libs/multidict/archive/v4.7.6.tar.gz"

    version('4.7.6', sha256='449035f89a12f189579ff83811424c71e4a39e335bcb8045145ad084b7bde2dc')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5:', type=('build', 'run'))
