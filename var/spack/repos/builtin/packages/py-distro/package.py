# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyDistro(PythonPackage):
    """Distro - an OS platform information API."""

    homepage = "https://github.com/nir0s/distro"
    url      = "https://pypi.io/packages/source/d/distro/distro-1.5.0.tar.gz"

    version('1.5.0', sha256='0e58756ae38fbd8fc3020d54badb8eae17c5b9dcbed388b17bb55b8a5928df92')

    depends_on('py-setuptools', type='build')
