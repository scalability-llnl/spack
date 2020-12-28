# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAgateDbf(PythonPackage):
    """agate-dbf adds read support for dbf files to agate."""

    homepage = "https://agate-dbf.readthedocs.io/en/latest/"
    url      = "https://pypi.io/packages/source/a/agate-dbf/agate-dbf-0.2.1.tar.gz"

    version('0.2.1', sha256='00c93c498ec9a04cc587bf63dd7340e67e2541f0df4c9a7259d7cb3dd4ce372f')

    depends_on('py-setuptools',     type='build')
    depends_on('py-agate@1.5.0:',   type=('build', 'run'))
    depends_on('py-dbfread@2.0.5:', type=('build', 'run'))
