# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiopandas(PythonPackage):
    """Working with molecular structures in pandas DataFrames"""

    homepage = "http://rasbt.github.io/biopandas"
    url      = "https://pypi.io/packages/source/b/biopandas/biopandas-0.2.5.tar.gz"
    git      = "https://github.com/rasbt/biopandas.git"

    # Note that the source package on PyPi is broken as it
    # is missing the requirements.txt so we have to download
    # from github

    version('0.2.5', branch="v0.2.5")

    depends_on('python@3.5:',       type=('build', 'run'))
    depends_on('py-pandas@0.24.2:', type=('build', 'run'))
    depends_on('py-numpy@1.16.2:',  type=('build', 'run'))
