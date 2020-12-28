# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCdsapi(PythonPackage):
    """The Climate Data Store Application Program Interface is a service providing programmatic access to CDS data. Get your UID and API key from the CDS portal at the address https://cds.climate.copernicus.eu/user and write it into the configuration file. Look at https://pypi.org/project/cdsapi/ for an example"""

    homepage = "https://cds.climate.copernicus.eu"
    url      = "https://pypi.io/packages/source/c/cdsapi/cdsapi-0.2.3.tar.gz"

    version('0.2.3', sha256='333b31ec263224399635db9b21a2e1a50cd73451f5179f8d967437e7c9161d9b')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.5.0:', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
