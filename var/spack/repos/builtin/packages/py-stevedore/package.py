# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStevedore(PythonPackage):
    """Manage Dynamic Plugins for Python Applications."""

    homepage = "https://docs.openstack.org/stevedore/latest/"
    url      = "https://pypi.io/packages/source/s/stevedore/stevedore-1.28.0.tar.gz"

    version('1.28.0', sha256='f1c7518e7b160336040fee272174f1f7b29a46febb3632502a8f2055f973d60b')

    depends_on('python@2.6:')

    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pbr@2.0.0:2.1.0', type=('build', 'run'))
