# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestresources(PythonPackage):
    """Testresources, a pyunit extension for managing expensive test resources.
    """

    homepage = "https://launchpad.net/testresources"
    url      = "https://pypi.io/packages/source/t/testresources/testresources-2.0.1.tar.gz"

    version('2.0.1', sha256='ee9d1982154a1e212d4e4bac6b610800bfb558e4fb853572a827bc14a96e4417')

    depends_on('py-setuptools', type='build')
