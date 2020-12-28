# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDiscover(PythonPackage):
    """Test discovery for unittest."""

    homepage = "https://pypi.python.org/pypi/discover"
    url      = "https://pypi.io/packages/source/d/discover/discover-0.4.0.tar.gz"

    version('0.4.0', sha256='05c3fa9199e57d4b16fb653e02d65713adc1f89ef55324fb0c252b1cf9070d79')
