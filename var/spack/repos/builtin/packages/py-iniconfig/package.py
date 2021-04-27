# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyIniconfig(PythonPackage):
    """
    iniconfig: brain-dead simple parsing of ini files
    """

    pypi     = "iniconfig/iniconfig-1.1.1.tar.gz"

    version('1.1.1', sha256='bc3af051d7d14b2ee5ef9969666def0cd1a000e121eaea580d4a313df4b37f32')

    depends_on('py-setuptools', type='build')
