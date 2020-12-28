# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cget(PythonPackage):
    """Cmake package retrieval."""

    homepage = "https://github.com/pfultz2/cget"
    url      = "https://pypi.io/packages/source/c/cget/cget-0.1.9.tar.gz"

    version('0.1.9', sha256='2a7913b601bec615208585eda7e69998a43cc17080d36c2ff2ce8742c9794bf6')

    depends_on("py-setuptools", type='build')
    depends_on("py-six@1.10:", type=('build', 'run'))
    depends_on("py-click@6.6:", type=('build', 'run'))
    depends_on('py-subprocess32', when='^python@:2', type=('build', 'run'))
