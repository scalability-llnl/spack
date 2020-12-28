# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysolar(PythonPackage):
    """Pysolar is a collection of Python libraries for simulating the
       irradiation of any point on earth by the sun. It includes code
       for extremely precise ephemeris calculations, and more."""

    homepage = "http://pysolar.readthedocs.io"
    url      = "https://pypi.io/packages/source/p/pysolar/pysolar-0.8.tar.gz"

    version('0.8', sha256='548c05177acd2845143d9624e670635cd3e5c3a63782449ca35e090ca755c617')

    depends_on('py-setuptools', type='build')
    depends_on('python@3:', type=('build', 'run'), when='@0.8:')
    depends_on('py-numpy',  type=('build', 'run'))
    depends_on('py-pytz',  type=('build', 'run'))
