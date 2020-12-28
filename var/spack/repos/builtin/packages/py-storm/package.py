# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStorm(PythonPackage):
    """Storm is an object-relational mapper (ORM) for Python"""
    homepage = "https://storm.canonical.com/"
    url      = "https://launchpad.net/storm/trunk/0.20/+download/storm-0.20.tar.bz2"

    version('0.23', sha256='01c59f1c898fb9891333abd65519ba2dd5f68623ac8e67b54932e99ce52593d3')
    version('0.20', sha256='1fe016c9ec40520eafc3cf359f1ec2b7fa86be91e45c9279bfb0ea3b06390a82')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', when='@0.23:')
    depends_on('python@2.7:2.8', when='@:0.20')
    depends_on('python@2.7:2.8,3.5:', when='@0.21:')
