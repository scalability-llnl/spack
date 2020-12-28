# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH2(PythonPackage):
    """HTTP/2 State-Machine based protocol implementation"""

    homepage = "https://github.com/python-hyper/hyper-h2"
    url      = "https://pypi.io/packages/source/h/h2/h2-4.0.0.tar.gz"

    version('4.0.0', sha256='bb7ac7099dd67a857ed52c815a6192b6b1f5ba6b516237fc24a085341340593d')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-hyperframe')
    depends_on('py-hpack')
