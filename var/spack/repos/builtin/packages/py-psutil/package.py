# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPsutil(PythonPackage):
    """psutil is a cross-platform library for retrieving information on
    running processes and system utilization (CPU, memory, disks, network)
    in Python."""

    homepage = "https://pypi.python.org/pypi/psutil"
    url      = "https://pypi.io/packages/source/p/psutil/psutil-5.6.3.tar.gz"

    version('5.7.2', sha256='90990af1c3c67195c44c9a889184f84f5b2320dce3ee3acbd054e3ba0b4a7beb')
    version('5.6.3', sha256='863a85c1c0a5103a12c05a35e59d336e1d665747e531256e061213e2e90f63f3')
    version('5.6.2', sha256='828e1c3ca6756c54ac00f1427fdac8b12e21b8a068c3bb9b631a1734cada25ed')
    version('5.5.1', sha256='72cebfaa422b7978a1d3632b65ff734a34c6b34f4578b68a5c204d633756b810')
    version('5.4.5', sha256='ebe293be36bb24b95cdefc5131635496e88b17fabbcf1e4bc9b5c01f5e489cfe')
    version('5.0.1', sha256='9d8b7f8353a2b2eb6eb7271d42ec99d0d264a9338a37be46424d56b4e473b39e')

    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
