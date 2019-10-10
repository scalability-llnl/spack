# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonOauth2(PythonPackage):
    """python-oauth2 is a framework that aims at making it easy to
    provide authentication via OAuth 2.0 within an application stack."""

    homepage = "https://pypi.org/project/python-oauth2/"
    url      = "https://pypi.io/packages/source/p/python-oauth2/python-oauth2-1.1.1.tar.gz"

    version('1.1.1', sha256='d7a8544927ac18215ba5317edd8f640a5f1f0593921bcf3ce862178312c8c9a4')

    depends_on('py-setuptools', type='build')
    depends_on('py-python-memcached', type=('build', 'run'))
    depends_on('py-pymongo', type=('build', 'run'))
    depends_on('py-redis', type=('build', 'run'))
