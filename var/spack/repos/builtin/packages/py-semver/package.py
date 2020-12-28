# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySemver(PythonPackage):
    """A Python module for semantic versioning.
    Simplifies comparing versions."""

    homepage = "https://semver.org/"
    url      = "https://pypi.io/packages/source/s/semver/semver-2.8.1.tar.gz"

    version('2.8.1', sha256='5b09010a66d9a3837211bb7ae5a20d10ba88f8cb49e92cb139a69ef90d5060d8')

    depends_on('py-setuptools', type='build')
