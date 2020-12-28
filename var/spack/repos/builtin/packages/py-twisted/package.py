# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTwisted(PythonPackage):
    """An asynchronous networking framework written in Python"""
    homepage = "https://twistedmatrix.com/"
    url      = "https://pypi.io/packages/source/T/Twisted/Twisted-15.3.0.tar.bz2"

    version('15.4.0', sha256='78862662fa9ae29654bc2b9d349c3f1d887e6b2ed978512c4442d53ea861f05c')
    version('15.3.0', sha256='025729751cf898842262375a40f70ae1d246daea88369eab9f6bb96e528bf285')

    depends_on('py-setuptools', type='build')
